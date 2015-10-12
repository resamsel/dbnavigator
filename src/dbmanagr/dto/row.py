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

import six

from dbmanagr.dto import Dto
from dbmanagr.jsonable import from_json
from dbmanagr.utils import filter_keys


class Row(Dto):
    def __init__(
            self,
            table=None,
            row=None,
            autocomplete=None):
        Dto.__init__(self, autocomplete)

        self.table = table
        self.row = row

    def __getitem__(self, i):
        if i is None:
            return None
        if isinstance(i, six.string_types):
            i = i.encode('ascii')
        if type(i) is int:
            return self.row[i]
        try:
            return self.row.__dict__[i]
        except BaseException:
            return None

    @staticmethod
    def from_json(d):
        return Row(
            **from_json(filter_keys(d, 'table', 'row', 'autocomplete'))
        )