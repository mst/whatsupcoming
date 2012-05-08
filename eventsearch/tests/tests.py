from eventsearch.importing.importers import *
from resources import SPIELPLAN_HTML
import unittest
from lxml import etree

class TestStaatstheaterKarlsruheDeImporter(unittest.TestCase):

    def setUp(self):
	self.importer = StaatstheaterKarlsruheDeImporter()
	self.importer._get_html = (lambda url:  SPIELPLAN_HTML)

    def test_import(self):
	tree = self.importer.import_month(1)
	self.assertTrue(SPIELPLAN_HTML > 0)
