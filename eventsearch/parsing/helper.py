from eventsearch.models import Event
from eventsearch.models import Category
from eventsearch.models import Location
from django.db.models import fields

class EventParserHelper:

    def is_duplicate_event(self, event1):
	excludes = ['date_start', 'date_end']
	for event2 in Event.objects.filter(name=event1.name, date_start=event1.date_start):
	    difference = {}
	    for field in event1._meta.fields:
		if not (isinstance(field, (fields.AutoField, fields.related.RelatedField)) 
			or field.name in excludes):
		    if field.value_from_object(event1) != field.value_from_object(event2):
			difference[field.verbose_name] = (field.value_from_object(event1),
							  field.value_from_object(event2))
		if not difference == {}:
		    return False
	
	return True
