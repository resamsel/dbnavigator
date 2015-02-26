# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, AutocompleteFormatter
from dbnav.formatter import JsonFormatter, SimpleFormatter, SimplifiedFormatter


class SimplifiedWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}\n')
        Formatter.set(SimplifiedFormatter())


class JsonWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(
            self,
            u"""[
{0}
]""", item_separator=u""",
""",)
        Formatter.set(JsonFormatter())


class AutocompleteWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'{autocomplete}')
        Formatter.set(AutocompleteFormatter())


class SimpleWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(
            self,
            u"""Id\tTitle\tSubtitle\tAutocomplete
{0}
""")
        Formatter.set(SimpleFormatter())