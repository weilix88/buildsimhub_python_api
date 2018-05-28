import re

try:
    from html.parser import HTMLParser
except ImportError:
    # python 2
    from HTMLParser import HTMLParser


class NumericValueParser(HTMLParser):
    def __init__(self, report, table, column_name, row_name, report_for="EntireFacility"):
        HTMLParser.__init__(self)

        r = re.sub('\W', '', report)
        t = re.sub('\W', '', table)
        rf = re.sub('\W', '', report_for)

        self._tableId = r + ":" + rf + ":" + t
        self._column = column_name
        self._row = row_name
        self._in_table = False
        self._in_header = False
        self._in_row = False
        self._correct_row = False

        self._col_index = 0
        self._current_col_index = 0
        self._unit = ''
        self._data = ''

    @property
    def data(self):
        return self._data

    def get_data(self):
        return self._data

    @property
    def unit(self):
        return self._unit

    def get_unit(self):
        return self._unit

    def handle_starttag(self, tag, attributes):
        # this means if we are processing table
        # but we met another start tag table,
        # we then are out of the target table, should skip
        if self._in_table & (tag == 'table'):
            self._in_table = False
            return
        # search for matching table
        if tag == 'table':
            for name, value in attributes:
                if name == 'tableid' and value == self._tableId:
                    self._in_table = True
                    self._in_header = True
                    break
        # if we are in a row - reset the row specs
        elif tag == 'tr':
            self._current_col_index = 0
            self._in_row = True

    def handle_endtag(self, tag):
        if self._in_header & (tag == 'td'):
            # in header, any td is one column
            self._col_index += 1
        elif tag == 'tr':
            # this is the end of a row
            self._in_header = False
            self._in_row = False

            # we are outside of correct row now,
            # turn the flag off
            if self._correct_row:
                self._correct_row = False
        elif tag == 'table':
            # didn't find the value, return
            self._in_table = False

    def handle_data(self, data):
        data = data.strip()

        # if it is empty data, return
        if data == '':
            return

        # if not in this table, return
        if not self._in_table:
            return

        # check whether the data has unit
        index = data.find('[')
        unit = ''
        # reform the string & separate the unit
        if index > -1:
            unit = data[index+1:-1]
            data = data[:index - 1]

        if self._in_header & (data == self._column):
            self._in_header = False
            self._unit = unit
        elif self._correct_row & (self._current_col_index == self._col_index):
            # turn off the flag
            self._correct_row = False
            self._data = data

        elif self._in_row:
            # means we find the correct row
            if data == self._row:
                self._correct_row = True

            self._current_col_index += 1
