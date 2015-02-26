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

from dbnav.jsonable import Jsonable, from_json
from dbnav import utils


def to_dto(model):
    if type(model) is dict:
        return dict(map(lambda (k, v): (k, to_dto(v)), model.iteritems()))
    if type(model) in (tuple, list, set):
        return map(to_dto, model)
    from dbnav.model.baseitem import BaseItem
    if isinstance(model, BaseItem):
        return Item(
            title=model.title(),
            subtitle=model.subtitle(),
            autocomplete=model.autocomplete(),
            validity=model.validity(),
            icon=model.icon(),
            value=model.value(),
            uid=model.uid(),
            format=model.format()
        )
    return model


class Item(Jsonable):
    def __init__(
            self,
            title=None,
            subtitle=None,
            autocomplete=None,
            uid=None,
            icon=None,
            value=None,
            validity=None,
            format=None):
        self.title_ = title
        self.subtitle_ = subtitle
        self.autocomplete_ = autocomplete
        self.uid_ = uid
        self.icon_ = icon
        self.value_ = value
        self.validity_ = validity
        self.format_ = format

    def __hash__(self):
        return hash(utils.freeze(self.__dict__))

    def __eq__(self, o):
        return hash(self) == hash(o)

    def autocomplete(self):
        return self.autocomplete_

    def title(self):
        return self.title_

    def subtitle(self):
        return self.subtitle_

    def value(self):
        return self.value_

    def validity(self):
        return self.validity_

    def uid(self):
        if self.uid_ is not None:
            return self.uid_
        return utils.hash(self.autocomplete())

    def icon(self):  # pragma: no cover
        if self.icon_ is not None:
            return self.icon_
        return 'images/icon.png'

    def format(self):
        return self.format_

    @staticmethod
    def from_json(d):
        return Item(
            title=from_json(d['title']),
            subtitle=from_json(d['subtitle']),
            autocomplete=from_json(d['autocomplete']),
            uid=from_json(d['uid']),
            icon=from_json(d['icon']),
            value=from_json(d['value']),
            validity=from_json(d['validity']),
            format=from_json(d['format'])
        )