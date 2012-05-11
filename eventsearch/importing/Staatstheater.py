import locale
import calendar
from eventsearch.importing.helper import *
from lxml.html.soupparser import fromstring
from lxml import etree
from datetime import datetime
import urllib

class StaatstheaterImport(EventParserHelper):
    _base_url = "http://www.staatstheater.karlsruhe.de/spielplan/"

    locale.setlocale(locale.LC_ALL, "de_DE")
    _months = [month.replace('\xc3\xa4', 'ae').lower() for month in calendar.month_name]

    def import_month(self, month=1):
	html = urllib.urlopen(self._base_url + _months[month]).read()
	tree = fromstring(html)
	return self._find_day_containers(tree)
	

    def _find_day_containers(self, tree):
	day_context = tree.xpath("//div[@class = 'spielplan_day']::parent::*")
	return day_context
	
