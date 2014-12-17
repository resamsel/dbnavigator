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

import xml.etree.ElementTree as ET
from urlparse import urlparse
from os.path import isfile

from dbnav.sources import Source
from .databaseconnection import MySQLConnection

logger = logging.getLogger(__name__)


class MypassSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            with open(self.file) as f:
                mypass = f.readlines()

            for line in mypass:
                connection = MySQLConnection(
                    self.driver, *line.strip().split(':'))
                self.connections.append(connection)

        return self.connections


class DBExplorerMySQLSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            try:
                tree = ET.parse(self.file)
            except Exception as e:
                logger.warn(
                    'Error parsing dbExplorer config file: %s', e.message)
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:', ''))
                if url.scheme == 'mysql':
                    host = url.netloc.split(':')[0]
                    port = 3306
                    database = '*'
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = MySQLConnection(
                        self.driver, host, port, database, user, password)
                    self.connections.append(connection)

        return self.connections
