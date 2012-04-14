import unittest
from eventsearch.kanewsparser import KaNewsParser
from lxml import etree
from lxml.html.soupparser import parse

class TestKaNewsParser(unittest.TestCase):

    filename = 'kanews.html'
    
    def setUp(self):
	self.parser = KaNewsParser()
	self.html = open(self.filename).read()

    def test_should_find_all_entries(self):
	events = self.parser._events_for_html(self.html)
        self.assertEquals(25, len(events))
        

    def test_page_fetch(self):
        """ reads the url and parses the events """
        events = self.parser.events_for_page(1)
        self.assertEquals(25, len(events))
