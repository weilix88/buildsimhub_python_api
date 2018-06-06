from .numeric_value_parser import NumericValueParser


def save_html(content, directory):
    text_file = open(directory, 'w+')
    text_file.write(content)
    text_file.close()


def extract_value_from_table(content, report, table, column_name, row_name, report_for="EntireFacility"):
    parser = NumericValueParser(report, table, column_name, row_name, report_for)
    parser.feed(content)
    return {'value': parser.data, 'unit': parser.unit}
