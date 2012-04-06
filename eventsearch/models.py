from django.db import models

class Location(models.Model):
    street = models.CharField(max_length="200")
    address = models.CharField(max_length="200")
    city = models.CharField(max_length="200")
    zipCode = models.CharField(max_length="10")
    name = models.CharField(max_length="200")

class Event(models.Model):
    date_start = models.DateTimeField('start date')
    date_end = models.DateTimeField('end date')
    name = models.CharField(max_length="200")
    location = models.ForeignKey(Location)
    
    class Meta:
        ordering = ["date_start"]
