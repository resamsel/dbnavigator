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

import logging

from plistlib import readPlist
from os.path import isfile

from dbnav.sources import Source

logger = logging.getLogger(__name__)


class NavicatSource(Source):
    def __init__(self, uri, file, key, con_creator):
        Source.__init__(self)
        self.uri = uri
        self.file = file
        self.key = key
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            plist = readPlist(self.file)

            # Note: only works with SQLite ATM - passwords are encrypted within
            # Navicat config files
            for k, v in plist[self.key]['servers'].items():
                connection = self.con_creator(
                    self.uri,
                    None,
                    None,
                    v['dbfilename'],
                    None,
                    None)
                self.connections.append(connection)

        return self.connections