from django.db import models
from django_google_maps import fields as map_fields
from geopy import geocoders

class Location(models.Model):
    name = models.CharField(max_length="200")
    city = models.CharField(max_length="200", null=True)
    address = models.CharField(max_length="200",null=True)
    latitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True,editable=False)

    longitude = models.DecimalField(max_digits=30,decimal_places=26,blank=True,editable=False)
    
    def save(self):
        
        g  = geocoders.Google(domain='maps.google.de') 
        place, (self.latitude, self.longitude) = g.geocode( self.address + ' ' + self.city )
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
