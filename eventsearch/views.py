from django.http import Http404
from datetime import datetime
from eventsearch.models import Event
from django.shortcuts import render_to_response
from datetime import datetime

def upcoming(request):
    try:
        events = Event.objects.filter(date_start__gt=datetime.now())
	for event in events:
	    event.remaining = event.date_start.replace(tzinfo=None) - datetime.utcnow().replace(tzinfo=None)
	    event.days = event.remaining.days	    
	    event.minutes = event.remaining.seconds/60
    except Event.DoesNotExist:
        raise Http404
    return render_to_response('eventsearch/upcoming.html', {'events': events})
