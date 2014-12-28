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

from os import path

from tests.testcase import ParentTestCase
from dbnav.sqlite import sources

DIR = path.dirname(__file__)
RESOURCES = path.join(DIR, '../resources')
NAVICAT_CONFIG = path.join(RESOURCES, 'navicat.plist')
NAVICAT_CONFIG_404 = path.join(RESOURCES, 'navicat-404.plist')


class SourcesTestCase(ParentTestCase):
    def test_navicat_list(self):
        """Tests the sqlite.NavicatSQLiteSource.list class"""

        self.assertEqual(
            ['me@xyz.com.sqlite/', 'dbnav.sqlite/', 'dbnav-c.sqlite/'],
            map(str, sources.NavicatSQLiteSource(
                '', NAVICAT_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.NavicatSQLiteSource(
                '', NAVICAT_CONFIG_404).list()))
