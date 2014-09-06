#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from dbnav.writer import *
from dbnav.item import *
from dbnav.querybuilder import QueryFilter

AND_OPERATOR = '&'
OPERATORS = ['>=','<=','!=','=','~','*','>','<']

logger = logging.getLogger(__name__)

def parse_loglevel(level):
    return getattr(logging, level.upper(), None)

def parse_filter(s):
    filter = []
    for term in s.split(AND_OPERATOR):
        found = False
        for operator in OPERATORS:
            if operator in term:
                f = term.split(operator, 1)
                lhs = f[0]
                rhs = f[1] if len(f) > 1 else None
                filter.append(QueryFilter(lhs, operator, rhs))
                found = True
                break
        if not found:
            filter.append(QueryFilter(term))
    return filter

class Filter:
    def __init__(self, lhs, operator, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

class Options:
    parser = {}

    def __init__(self, argv, parser):
        logger.info('Called with params: %s', argv)

        self.opts = {}
        self.argv = argv
        self.uri = None
        self.logfile = None
        self.loglevel = None
        self.database = None
        self.table = None
        self.column = ''
        self.operator = None
        self.filter = None
        self.show = 'connections'
        self.simplify = False
        self.default = False
        self.simple = False
        self.json = False
        self.xml = False
        self.autocomplete = False
        self.test = False
        self.infile = None
        self.separator = None
        self.include_driver = False
        self.include_connection = False
        self.include_database = False
        self.include_columns = False

        args = parser.parse_args(argv[1:])

        if args.loglevel:
            args.loglevel = parse_loglevel(args.loglevel)
        if hasattr(args, 'include'):
            args.include = args.include.split(',') if args.include else []
        if hasattr(args, 'exclude'):
            args.exclude = args.exclude.split(',') if args.exclude else []

        self.__dict__.update(args.__dict__)
        
        Writer.from_options(self)

        for k in Options.parser:
            self.opts[k] = Options.parser[k].parse(self)

    def get(self, parser):
        return self.opts[parser]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if self.opts:
            for k in self.opts.keys():
                self.opts[k].__dict__[name] = value

    def __repr__(self):
        return self.__dict__.__repr__()
