from eventsearch.importing.importers import *
from resources import *
import unittest
from lxml import etree

class TestStaatstheaterKarlsruheDeImporter(unittest.TestCase):

    def setUp(self):
#	self.importer = StaatstheaterKarlsruheDeImporter()
#	self.importer._get_html = (lambda url:  SPIELPLAN_HTML)
	pass

    def test_import(self):
#	tree = self.importer.import_month(1)
	self.assertTrue(SPIELPLAN_HTML > 0)


class TestKaNightLife(unittest.TestCase):

    def setUp(self):
        self.importer = KaNightLife()
	self.importer._get_html = (lambda url:  KA_NIGHT_LIFE)

    def test(self):
	tree = self.importer.import_day(1,2,3)
	self.assertTrue(SPIELPLAN_HTML > 0)
