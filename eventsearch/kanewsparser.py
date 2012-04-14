from urllib import URLopener
import urllib
from models import Event
from models import Category
from models import Location
from datetime import datetime
from lxml import etree
from lxml.html.soupparser import fromstring
import time

class KaNewsParser:
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
        return urllib.urlopen(self._url, urllib.urlencode(params)).read()

    def _events_for_html(self, html):
	tree = fromstring(html)
	return self.parse_tree(tree)
	
    def parse_tree(self, tree):
	context  = tree.xpath("//div[@class='Content']/div[contains(@class,'Row')]")
	events = list()

	for node in context:
	    event = Event()
	    event.name = node.xpath("./div[contains(@class, 'first ')]/a/text()")[0].strip()


            br_divided_div_text = "./div[@class='%s']/text()[%s-sibling::br]"
	    loc_name = node.xpath(br_divided_div_text % ("second", "following"))[0].strip()
	    loc_city = node.xpath(br_divided_div_text % ("second", "preceding"))[0].strip()
	    location, created = Location.objects.get_or_create(name=loc_name, city=loc_city)

            event.location = location


	    date = node.xpath(br_divided_div_text % ("third", "following"))[0].strip()
	    time = node.xpath(br_divided_div_text % ("third", "preceding"))[0].strip()
	    event.date_start =  datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M Uhr")

            event.save()
            category_name = node.xpath("./div[@class='fourth']")[0].text_content().strip()
            cat, created = Category.objects.get_or_create(name=category_name)
            event.categories.add(cat)
            event.save()
	    events.append(event)

        return events
	    
