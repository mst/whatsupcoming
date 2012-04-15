from eventsearch.models import *
from django.contrib import admin
from django_google_maps import fields as map_fields
from django_google_maps import widgets as map_widgets

class LocationInline(admin.TabularInline):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
	map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},    
	}

admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
