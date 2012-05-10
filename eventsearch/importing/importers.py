import logging
import urllib
from urllib import URLopener
from eventsearch.models import *
from datetime import datetime
from lxml import etree
from lxml.html.soupparser import fromstring
from eventsearch.importing.location import GooglePlacesLookup
from eventsearch.importing.helper import *
import time
import locale
import re
import calendar

logging.basicConfig()
_logger = logging.getLogger('ka-news-parser')
_logger.setLevel(logging.INFO)

class KaNewsImporter(EventImportHelper):
    """ parses a page in on kanews.de's events page. """
    """ The events page is paginated, starting from page 0, call  """
    """ events = parser.events_for_page(0) to retrieve the events objects """

    _url = "http://www.ka-news.de/kultur/events/"
    
    def import_events_from_page(self, page):
         content = self._html_for_page_nr(page)
         return self._events_for_html(content)

    def _html_for_page_nr(self, page):
        params = { 'event[suche][pager][page]': page,
                   'event[suche][kalender-tag]' : int(time.time() ) }
        return self._read_url(self._url, params)

    def _read_url(self, url, params):
        return urllib.urlopen(url, urllib.urlencode(params)).read()

    def _events_for_html(self, html):
	tree = fromstring(html)
	return self.parse_tree(tree)
	
    def parse_tree(self, tree):
	context  = tree.xpath("//div[@class='Content']/div[contains(@class,'Row')]")
	events = []

	for node in context:
	    try:
                event = Event()
                event.name = node.xpath("./div[contains(@class, 'first ')]/a/text()")[0].strip()
                
                br_divided_div_text = "./div[@class='%s']/text()[%s-sibling::br]"
                loc_name = node.xpath(br_divided_div_text % ("second", "following"))[0].strip()
                loc_city = node.xpath(br_divided_div_text % ("second", "preceding"))[0].strip()
                _logger.info('found event %s at location %s, %s' % (event.name, loc_name, loc_city))

                geodata = GooglePlacesLookup.find_geo_data_for_venue(loc_name, loc_city)
                loc_name = geodata['name']
                lat = geodata['lat']
                lon = geodata['lon']
                location, created = Location.objects.get_or_create(name=loc_name, city=loc_city, latitude=lat, longitude=lon)
                
                if created:
                    _logger.info("created new location %s" % location.__unicode__())

                event.location = location
                
                date = node.xpath(br_divided_div_text % ("third", "following"))[0].strip()
                time = node.xpath(br_divided_div_text % ("third", "preceding"))[0].strip()
                event.date_start =  datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M Uhr")
                if not self.is_duplicate_event(event):
                    event.save()
                    category_name = node.xpath("./div[@class='fourth']")[0].text_content().strip()
                    cat, created = Category.objects.get_or_create(name=category_name)
                    event.categories.add(cat)
                    cat.save()
                    event.save()
                    events.append(event)

            except Exception, err:
		_logger.exception("error importing node: %s" % etree.tostring(node))
        return events
    

class StaatstheaterKarlsruheDeImporter(EventImportHelper):

    _base_url = "http://www.staatstheater.karlsruhe.de/spielplan/"
    monthnames = ['januar', 'februar', 'maerz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember']
    _months = [month.replace('\xc3\xa4', 'ae').lower() for month in monthnames]

    LOCATION = Location()

    def _get_html(self, url):
	return urllib.urlopen(url).read()        


    def __init__(self):
        geodata = GooglePlacesLookup.find_geo_data_for_venue("Badisches Staatsthater", "Karlsruhe")
        loc_name = geodata['name']
        lat = geodata['lat']
        lon = geodata['lon']
        self.LOCATION, created = Location.objects.get_or_create(name=loc_name, city="Karlsruhe", latitude=lat, longitude=lon)

    def import_month(self, month=1):
        html = self._get_html(self._base_url + self._months[month])
	tree = fromstring(html)
	boxes = self._find_contentboxes(tree)
        current_day = None

        for node in boxes:
            day_node = node.xpath("div[@class ='spielplan_day']")
            event = Event()

            if len(day_node) > 0:
                _current_day = day_node[0].text_content().split(", ")[1] + str(datetime.now().year)
            
            time = node.xpath("div[@class ='spielplan_date']")
            if len(time) > 0:
                try:
                    p = re.compile(u"\xa0?-")
                    (start, end) = p.split(time[0].text_content())
                    print _current_day, start, end
                    event.date_end = datetime.strptime(_current_day + " " + end, "%d.%m.%Y %H:%M")
                except ValueError, err:
                    start = time[0].text_content()

                event.date_start = datetime.strptime(_current_day + " " + start, "%d.%m.%Y %H:%M")
                

            title = node.xpath("div[@class='spielplan_content']/*/a[contains(@href,'programm')]")
            if (len(title) > 0):
                _title = title[0].text_content()
                event.name = " ".join([word.capitalize().strip() for word in _title.split(" ")])

            house = node.xpath("*/span[@class='ort']") 
            if len(house) > 0:
                _house = house[0].text_content()

            event.location = self.LOCATION
                
            if event.name != None and not self.is_duplicate_event(event):
                _logger.info("Found event %s" % str(event))
                event.save()

    def _find_contentboxes(self, tree):
	day_context = tree.xpath("//div[@class = 'spielplan contentBox']")
	return day_context
