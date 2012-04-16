from django.db import models
from django_google_maps import fields as map_fields
from geopy import geocoders
from googlemaps import GoogleMaps
from googleplaces import GooglePlaces, types

YOUR_API_KEY = 'AIzaSyDsaRhBz8WhZICkiElokU9XitMWRkIFxL8'


class Location(models.Model):
    name = models.CharField(max_length="200")
    city = models.CharField(max_length="200", null=True)
    address = models.CharField(max_length="200",null=True)
    latitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    longitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True)
    
    def save(self):
        query_result = ''
        query_result = GooglePlaces(YOUR_API_KEY).query(
        location=self.city +', Germany', keyword=self.name,
        radius=20000)
        if query_result.has_attributions:
            
            
            place = query_result.places[0]
        
    # Returned places from a query are place summaries.
            self.name = place.name
            self.latitude =  place.geo_location['lat']
            self.longitude = place.geo_location['lng']
            
           

    # The following method has to make a further API call
        super(Location, self).save()
    

    def __unicode__(self):
	return self.name + ", " + self.city


        

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
