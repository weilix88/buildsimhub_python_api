from .numeric_value_parser import NumericValueParser


def save_html(content, dir):
    text_file = open(dir,'w')
    text_file.write(content)
    text_file.close()


def extract_value_from_table(content, report, table, column_name, row_name, reportFor = "EntireFacility"):
    parser = NumericValueParser(report, table, column_name, row_name, reportFor)
    parser.feed(content)
    return {'value':parser.data, 'unit':parser.unit}

###############LOCAL TEST########################
#tableReader = NumericValueParser('Climatic Data Summary','Sizing Period Design Day','Maximum Dry Bulb','CHICAGO ANN HTG 99.6% CONDNS DB')
#file = open('testTable.html', 'r') 
#tableReader.feed(file.read())
#print(tableReader.data)
#print(tableReader.unit)
