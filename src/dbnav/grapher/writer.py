#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter, GraphvizFormatter
from dbnav.node import ColumnNode

class GraphWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}')
        Formatter.set(DefaultFormatter())

class GraphvizWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u"""digraph dbgraph {{
{0}
}}""")
        Formatter.set(GraphvizFormatter())
    def filter(self, items):
        # Removes duplicate items and keeps order
        return list(OrderedDict.fromkeys(
            filter(lambda i: not isinstance(i, ColumnNode), items)))

class GraphTestWriter(GraphWriter):
    pass
