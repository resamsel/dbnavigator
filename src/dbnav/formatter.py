#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultFormatter:
    def __init__(self):
        pass
    def format(self, item):
        return str(item)
    def format_item(self, item):
        return self.format(item)
    def format_row(self, item):
        return u', '.join(map(str, item))
    def format_column(self, item):
        return self.format(item)
    def format_node(self, item):
        return self.format(item)
    def format_column_node(self, item):
        return self.format(item)
    def format_name_node(self, item):
        return self.format(item)
    def format_table_node(self, item):
        return self.format(item)
    def format_foreign_key_node(self, item):
        return self.format(item)

class SimplifiedFormatter(DefaultFormatter):
    def __init__(self,
            default_format=u'{title}\t{subtitle}\t{autocomplete}',
            item_format=u'{title}\t{subtitle}\t{autocomplete}'):
        self.default_format = default_format
        self.item_format = item_format
    def format(self, item):
        return self.default_format.format(
            title=item.title(),
            subtitle=item.subtitle(),
            autocomplete=item.autocomplete(),
            uid=item.uid(),
            validity=item.validity(),
            icon=item.icon(),
            value=item.value())
    def format_item(self, item):
        return self.item_format.format(
            title=item.title,
            subtitle=item.subtitle,
            autocomplete=item.autocomplete,
            uid=item.uid,
            validity=item.valid,
            icon=item.icon,
            value=item.value)
    def format_row(self, item):
        return self.format(item)

class TestFormatter(SimplifiedFormatter):
    def format(self, item):
        return u'{title}\t{autocomplete}'.format(
            title=item.title(),
            autocomplete=item.autocomplete())
    def format_item(self, item):
        return u'{title}\t{autocomplete}'.format(
            title=item.title,
            autocomplete=item.autocomplete)

class GraphvizFormatter(DefaultFormatter):
    def format(self, item):
        return str(item)
    def format_name_node(self, item):
        return u'  root={0};'.format(item)
    def format_foreign_key_node(self, item):
        return u'  {fk.a.table.name} -> {fk.b.table.name} [xlabel="{fk.a.name} -> {fk.b.name}"];'.format(fk=item)

class XmlFormatter(SimplifiedFormatter):
    def __init__(self):
        SimplifiedFormatter.__init__(self, default_format=u"""   <item uid="{uid}" arg="{value}" autocomplete="{autocomplete}" valid="{validity}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>""", item_format=u"""   <item uid="{uid}" arg="{value}" autocomplete="{autocomplete}" valid="{validity}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>""")

class Formatter:
    formatter = DefaultFormatter()

    @staticmethod
    def set(arg):
        Formatter.formatter = arg

    @staticmethod
    def format(item):
        return Formatter.formatter.format(item)

    @staticmethod
    def format_item(item):
        return Formatter.formatter.format_item(item)

    @staticmethod
    def format_row(item):
        return Formatter.formatter.format_row(item)

    @staticmethod
    def format_column(item):
        return Formatter.formatter.format_column(item)

    @staticmethod
    def format_node(item):
        return Formatter.formatter.format_node(item)

    @staticmethod
    def format_column_node(item):
        return Formatter.formatter.format_column_node(item)

    @staticmethod
    def format_table_node(item):
        return Formatter.formatter.format_table_node(item)

    @staticmethod
    def format_name_node(item):
        return Formatter.formatter.format_name_node(item)

    @staticmethod
    def format_foreign_key_node(item):
        return Formatter.formatter.format_foreign_key_node(item)