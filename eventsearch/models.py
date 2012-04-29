
import logging
from decimal import *
from django.db import models
from googleplaces import GooglePlaces, types

YOUR_API_KEY = 'AIzaSyDsaRhBz8WhZICkiElokU9XitMWRkIFxL8'
logging.basicConfig()
_logger = logging.getLogger('models')
_logger.setLevel(logging.INFO)

class Location(models.Model):

    name = models.CharField(max_length="200")
    city = models.CharField(max_length="200", null=True)
    address = models.CharField(max_length="200",null=True)
    latitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    longitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    
    def save(self, *args, **kwargs):

        query_result = ''
        query_result = GooglePlaces(YOUR_API_KEY).query(
        location=self.city +', Germany', keyword=self.name,
        radius=20000)
        if query_result.has_attributions:
            place = query_result.places[0]
        
            self.name = place.name
            self.latitude = Decimal(str(place.geo_location['lat']))
            self.longitude = Decimal(str(place.geo_location['lng']))
            
    	_logger.info("saving location %s" % self.__unicode__())
        super(Location, self).save(*args, **kwargs)
    

    def __unicode__(self):
	return "%s, %s, %f, %f" % (self.name, self.city, self.latitude, self.longitude)


class Category(models.Model):
    name = models.CharField(max_length="200")
    def __unicode__(self):
        return self.name
    

class Event(models.Model):
    name = models.CharField(max_length="200")
    date_start = models.DateTimeField('start date')
    date_end = models.DateTimeField('end date', null=True)
    categories = models.ManyToManyField(Category)
    location = models.ForeignKey(Location)

    def __unicode__(self):
	return self.name + " at " + self.location.__unicode__()

    class Meta:
        ordering = ["date_start"]
