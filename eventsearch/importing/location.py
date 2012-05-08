import logging
from googleplaces import GooglePlaces, types

from django.utils.encoding import smart_str
from decimal import Decimal

YOUR_API_KEY = 'AIzaSyDsaRhBz8WhZICkiElokU9XitMWRkIFxL8'

class GooglePlacesLookup():

    @classmethod
    def find_geo_data_for_venue(self, name, city):
	query_result = ''
	
#	address = smart_str(address)
	name = smart_str(name)
	city = smart_str(city)


	query_result = GooglePlaces(YOUR_API_KEY).query(
	    location=city +', Germany', keyword=name,
	    radius=20000)

        latitude = None
        longitude = None

	if query_result.has_attributions:
	    place = query_result.places[0]
	    
	    # replace the data with the one found from
	    # google places
	    name = place.name
	    latitude = Decimal(str(place.geo_location['lat']))
	    longitude = Decimal(str(place.geo_location['lng']))

        
        return {"name":name, 'lat':latitude, 'lon':longitude}
	

