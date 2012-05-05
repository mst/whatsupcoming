from django.http import Http404
from datetime import datetime
from eventsearch.models import Event
from django.shortcuts import render_to_response,get_object_or_404
from datetime import datetime

def upcoming(request):
    try:
        events = Event.objects.all() # filter(date_start__gt=datetime.now())
	for event in events:
	    event.remaining = event.date_start.replace(tzinfo=None) - datetime.utcnow().replace(tzinfo=None)
	    event.days = event.remaining.days	    
	    event.minutes = event.remaining.seconds/60
            event.distance_view = round(event.distance(float(request.GET.get('lat')), float(request.GET.get('lon'))))
    except Event.DoesNotExist:
        raise Http404
    return render_to_response('eventsearch/upcoming.html', {'events': events})

def detail(request,event_id):
    e = get_object_or_404(Event, pk=event_id)
    return render_to_response('eventsearch/detail.html',{'event' : e})

    
    
