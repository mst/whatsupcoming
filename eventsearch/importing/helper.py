from eventsearch.models import *
from django.db.models import fields
import unittest

class EventImportHelper:

    def is_duplicate_event(self, event1):
	excludes = ['date_start', 'date_end']
	for event2 in Event.objects.filter(name=event1.name, date_start=event1.date_start):
            venue1 = event1.location
            venue2 = event2.location 
            if (self.is_same_venue(venue1,venue2)):
                event1.name = event2.name
                event1.date_start = event2.date_start
                return True

	return False

    def is_same_venue(self, venue1, venue2):
        equals_conditions = [(lambda v1, v2: (abs(v1.latitude - v2.latitude) < 0.00001)),
                             (lambda v1, v2: (abs(v1.longitude - v2.longitude) < 0.00001)),
                             (lambda v1, v2: (v1.name == v2.name)),
                             (lambda v1, v2: (v1.city == v2.city))]

        for equal in equals_conditions:
            try: 
                if not equal(venue1, venue2): return False
            except Exception, err:
                pass

        return True

        
