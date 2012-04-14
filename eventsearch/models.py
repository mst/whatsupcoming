from django.db import models
from django_google_maps import fields as map_fields

class Location(models.Model):
    name = models.CharField(max_length="200")
    city = models.CharField(max_length="200", null=True)
    address = models.CharField(max_length="200",null=True)

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
