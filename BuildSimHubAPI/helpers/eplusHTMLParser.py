import re
from HTMLParser import HTMLParser

class EplusHTMLParser(HTMLParser):


    def readANumericValueFromTable(report, table, item, colmnTitle):


    def readSingleTextValueFromTable(report, table, item, columnTitle):
        tableId = re.sub('\W+','',report) + ":EntireFacility:" + re.sub('\W+','',table)
        tag = 'table'

        