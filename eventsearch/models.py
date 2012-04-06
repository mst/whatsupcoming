from django.db import models
from django_google_maps import fields as map_fields

class Location(models.Model):
    name = models.CharField(max_length="200")
    address = models.CharField(max_length="200",null=True)
    
    def __unicode__(self):
	return self.name

class Event(models.Model):
    name = models.CharField(max_length="200")
    date_start = models.DateTimeField('start date')
    date_end = models.DateTimeField('end date', null=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)    

    def __unicode__(self):
	return self.name + " at " + self.address

    class Meta:
        ordering = ["date_start"]
