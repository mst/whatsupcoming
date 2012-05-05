import logging
from decimal import *
from django.db import models
from googleplaces import GooglePlaces, types
from string import Template
import math

YOUR_API_KEY = 'AIzaSyDsaRhBz8WhZICkiElokU9XitMWRkIFxL8'
logging.basicConfig()
_logger = logging.getLogger('models')
_logger.setLevel(logging.INFO)

class Location(models.Model):

    nauticalMilePerLat = 60.00721
    nauticalMilePerLongitude = 60.10793
    rad = math.pi / 180.0
    milesPerNauticalMile = 1.15078
    metersPerMile = 1609.344

    name = models.CharField(max_length="200")
    city = models.CharField(max_length="200", null=True)
    address = models.CharField(max_length="200",null=True)
    latitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    longitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    
    #
    # The following formulas are adapted from the Aviation Formulary
    # http://williams.best.vwh.net/avform.htm
    #
    def distance(self, lat2, lon2):
        """
        Caclulate distance between two lat lons in NM
        """
        lat1 = float(self.latitude)
        lon1 = float(self.longitude)
        yDistance = (lat2 - lat1) * self.nauticalMilePerLat
        xDistance = (math.cos(lat1 * self.rad) + math.cos(lat2 * self.rad)) * (lon2 -lon1 ) * (self.nauticalMilePerLongitude / 2)
        distance = math.sqrt( yDistance**2 + xDistance**2 )
        return distance * self.milesPerNauticalMile * self.metersPerMile
    
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

    def distance(self, lat, lon):
        return self.location.distance(lat, lon)

    class Meta:
        ordering = ["date_start"]

    @classmethod
    def find_closest(self, lat, lon, limit=25):
        events = Event.objects.all()
        return sorted(events, key=lambda event:event.distance(lat,lon))

