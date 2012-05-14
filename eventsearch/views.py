from django.http import Http404
from datetime import datetime
from eventsearch.models import Event
from django.template import RequestContext
from endless_pagination.decorators import page_template
from django.shortcuts import render_to_response,get_object_or_404
from datetime import datetime

@page_template("page_upcoming.html")
def upcoming(request, 
             template="upcoming.html",
             extra_context=None):
    try:
        events = Event.objects.filter(date_start__gt=datetime.now())
	for event in events:
	    event.remaining = event.date_start.replace(tzinfo=None) - datetime.utcnow().replace(tzinfo=None)
	    event.days = event.remaining.days	    
	    event.minutes = event.remaining.seconds/60
            if ('lat' and 'lon') in request.GET.keys():
                distance = event.distance(float(request.GET.get('lat')), float(request.GET.get('lon')))
                if (distance != None):
                    event.distance_view = int(round(distance))
    except Event.DoesNotExist:
        raise Http404
    context = {
        'events': Event.objects.filter(date_start__gt=datetime.now())
       
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context,
        context_instance=RequestContext(request))
    

def detail(request,event_id):
    e = get_object_or_404(Event, pk=event_id)
    return render_to_response('detail.html',{'event' : e})

    
    
