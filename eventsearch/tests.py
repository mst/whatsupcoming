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
	events = self.parser.get_events_for_html(self.html)
        self.assertEquals(25, len(events))


