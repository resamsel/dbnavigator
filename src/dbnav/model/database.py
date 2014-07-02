#!/usr/bin/env python
# -*- coding: utf-8 -*-

OPTION_URI_DATABASE_FORMAT = '%s/'

class Database:
    """The database used with the given connection"""

    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())