#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import math
import datetime

from sqlalchemy import Boolean, Float, Integer
from sqlalchemy.types import TIMESTAMP

from dbnav.queryfilter import QueryFilter, OrOp, AndOp

OR_OPERATOR = '|'
AND_OPERATOR = '&'
OPERATORS = ['>=', '<=', '!=', '=', '~', '*', '>', '<', ':']

logger = logging.getLogger(__name__)


def escape_keyword(keyword):
    if keyword in ['user', 'table', 'column']:
        return '"%s"' % keyword
    return keyword


def restriction(
        alias, column, operator, value, map_null_operator=True):
    if not column:
        raise Exception('Parameter column may not be None!')
    if operator in ['=', '!='] and (value is None or value == 'null'):
        if map_null_operator:
            operator = {
                '=': 'is',
                '!=': 'is not'
            }.get(operator)
        value = None
    if column.table and alias is not None:
        return u"{0}.{1} {2} {3}".format(
            alias,
            escape_keyword(column.name),
            operator,
            format_value(column, value))
    return u'{0} {1} {2}'.format(
        escape_keyword(column.name),
        operator,
        format_value(column, value))


def format_value(column, value):
    if value is None or (type(value) is float and math.isnan(value)):
        return 'null'
    if type(value) is list:
        return '({0})'.format(
            ','.join([format_value(column, v) for v in value]))
    if type(value) in [datetime.datetime, datetime.date, datetime.time]:
        return "'%s'" % value
    if type(value) is buffer:
        return u"'[BLOB]'"
    if column is None:
        try:
            return '%d' % int(value)
        except ValueError:
            return u"'%s'" % value
    if (isinstance(column.type, Boolean)
            and (type(value) is bool or value in ['true', 'false'])):
        return '%s' % str(value).lower()
    if isinstance(column.type, Float):
        try:
            return '%f' % float(value)
        except ValueError:
            pass
    if isinstance(column.type, Integer):
        try:
            return '%d' % int(value)
        except ValueError:
            pass
    if isinstance(column.type, TIMESTAMP):
        try:
            return '%d' % int(value)
        except ValueError:
            pass
    return u"'%s'" % value.replace('%', '%%').replace("'", "''")


def parse_filter(s):
    _or = OrOp()
    for t in s.split(OR_OPERATOR):
        _and = AndOp()
        for term in t.split(AND_OPERATOR):
            found = False
            for operator in OPERATORS:
                if operator in term:
                    f = term.split(operator, 1)
                    lhs = f[0]
                    rhs = f[1] if len(f) > 1 else None
                    if operator == ':':
                        rhs = rhs.split(',')
                    _and.append(QueryFilter(lhs, operator, rhs))
                    found = True
                    break
            if not found:
                _and.append(QueryFilter(term))
        _or.append(_and)
    return _or


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

        args = parser.parse_args(argv)

        if hasattr(args, 'include'):
            args.include = args.include.split(',') if args.include else []
        if hasattr(args, 'exclude'):
            args.exclude = args.exclude.split(',') if args.exclude else []

        self.__dict__.update(args.__dict__)

        self.update_parsers()

    def update_parsers(self):
        for k in Options.parser:
            self.opts[k] = Options.parser[k].parse(self)

    def get(self, parser):
        return self.opts[parser]

    def escape_keyword(self, keyword):
        return escape_keyword(keyword)

    def restriction(
            self, alias, column, operator, value, map_null_operator=True):
        return restriction(alias, column, operator, value, map_null_operator)

    def format_value(self, column, value):
        return format_value(column, value)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if self.opts:
            for k in self.opts.keys():
                self.opts[k].__dict__[name] = value

    def __repr__(self):
        return self.__dict__.__repr__()
