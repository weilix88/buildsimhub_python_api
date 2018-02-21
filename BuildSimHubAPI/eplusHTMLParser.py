from BuildSimHubAPI.htmlParser import numericValueParser

def extract_a_value_from_table(html, report, table, column, row, category = "EntireFacility"):
    data_reader = numericValueParser.NumericValueParser(report, table, column, row, category)
    data_reader.feed(html)
    return {'value':data_reader.data, 'unit':data_reader.unit}