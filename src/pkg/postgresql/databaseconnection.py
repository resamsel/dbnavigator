#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging
import psycopg2
import psycopg2.extras
import time

from os.path import expanduser

from ..logger import logduration
from ..model.database import Database
from ..model.table import Table
from ..model.column import Column
from ..model.foreignkey import ForeignKey

CACHE_TIME = 2*60
DATABASES_QUERY = """
select
        datname as database_name
    from
        pg_database
    where
        datistemplate = false
    order by datname
"""
FOREIGN_KEY_QUERY = """
select
        tc.table_name,
        kcu.column_name,
        ccu.table_name foreign_table_name,
        ccu.column_name foreign_column_name
    from
        information_schema.table_constraints tc
        join information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        join information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
    where
        constraint_type = 'FOREIGN KEY'
"""
TABLES_QUERY = """
select
        t.table_name as tbl, obj_description(c.oid) as comment
    from
        information_schema.tables t,
        pg_class c
    where
        table_schema = 'public'
        and t.table_name = c.relname
        and c.relkind = 'r'
    order by t.table_name
"""

class DatabaseConnection:
    """A database connection"""

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.con = None
        self.dbs = None
        self.tbls = None

    def __repr__(self):
        return '%s@%s/%s' % (self.user, self.host, self.database if self.database != '*' else '')

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __getstate__(self):
        state = dict(self.__dict__)
        logging.debug('State: %s' % state)
        if 'con' in state:
            del state['con']
        return state

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        if self.database and self.database != '*':
            return '%s@%s/%s/' % (self.user, self.host, self.database)

        return '%s@%s/' % (self.user, self.host)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'PostgreSQL Connection'

    def matches(self, s):
        return s.startswith("%s@%s" % (self.user, self.host))

    def connect(self, database):
        logging.debug('Connecting to database %s' % database)
        
        if database:
            try:
                self.con = psycopg2.connect(host=self.host, database=database, user=self.user, password=self.password)
            except psycopg2.DatabaseError, e:
                self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)
                database = None

            if database:
                d = shelve.open(expanduser('~/.dbnavigator.cache'), writeback=True)
                try:
                    uri = self.__repr__()
                    if uri in d and d['%s_time' % uri] > time.time() - CACHE_TIME:
                        # foreign key have already been saved to shelve within the last 2 minutes
                        self.table_map = d[uri]
                    else:
                        self.table_map = {t.name: t for t in self.tables(database)}
                        self.put_foreign_keys()
                        
                        d[uri] = self.table_map
                        d['%s_time' % uri] = time.time()
                finally:
                    d.close()
        else:
            self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)

    def cursor(self):
        return self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def databases(self):
        if not self.dbs:
            query = DATABASES_QUERY
            logging.debug('Query databases: %s' % query)

            cur = self.cursor()
            start = time.time()
            cur.execute(query)
            logduration('Query databases', start)
    
            def d(row): return Database(self, row[0])
    
            self.dbs = map(d, cur.fetchall())
        
        return self.dbs

    def tables(self, database):
        if not self.tbls:
            query = TABLES_QUERY
            logging.debug('Query tables: %s' % query)
    
            cur = self.cursor()
            start = time.time()
            cur.execute(query)
            logduration('Query tables', start)
    
            def t(row): return Table(self, database, row[0], row[1])
    
            self.tbls = map(t, cur.fetchall())

        return self.tbls

    def put_foreign_keys(self):
        """Retrieves the foreign keys of the table"""

        logging.debug('Retrieve foreign keys')
        query = FOREIGN_KEY_QUERY
        logging.debug('Query foreign keys: %s' % query)
        cur = self.cursor()
        start = time.time()
        cur.execute(query)
        logduration('Query foreign keys', start)
        for row in cur.fetchall():
            a = Column(self.table_map[row['table_name']], row['column_name'])
            b = Column(self.table_map[row['foreign_table_name']], row['foreign_column_name'])
            fk = ForeignKey(a, b)
            self.table_map[a.table.name].fks[a.name] = fk
            self.table_map[b.table.name].fks[str(a)] = fk