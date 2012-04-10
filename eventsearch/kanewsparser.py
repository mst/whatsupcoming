from urllib import URLopener
from models import Event
from models import Location
from datetime import datetime
from lxml import etree
from lxml.html.soupparser import fromstring

class KaNewsParser:

    def get_events_for_html(self, html):
	tree = fromstring(html)
	return self.parse_tree(tree)
	
    def get_events_for_url(self, url):
	content =  URLopener().open(url).read()
	return self.get_events_for_html(content)
	
    def parse_tree(self, tree):
	context  = tree.xpath("//div[@class='Content']/div[contains(@class,'Row')]")
	events = list()

	for node in context:
	    name = node.xpath("./div[contains(@class, 'first ')]/a/text()")[0].strip()
	    location_name = node.xpath("./div[@class='second']/text()[following-sibling::br]")[0].strip()
	    location_town = node.xpath("./div[@class='second']/text()[preceding-sibling::br]")[0].strip()
	    date = node.xpath("./div[@class='third']/text()[(following-sibling::br)]")[0].strip()
	    time = node.xpath("./div[@class='third']/text()[(preceding-sibling::br)]")[0].strip()
	    category = node.xpath("./div[@class='fourth']")[0].text_content().strip()
	    
	    event = Event()
	    event.name = name
	    event.date_start =  datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M Uhr")
	    location = Location()
	    location.name = location_name
	    event.location = location
	    events.append(event)

	return events
	    
