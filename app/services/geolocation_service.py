import math
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
from app.settings.config import API_KEY


def get_centroid(coordinates: list[tuple]) -> tuple:
    x = 0
    y = 0
    z = 0
    for lat, lon in coordinates:
        latitude = math.radians(lat)
        longitude = math.radians(lon)
        x += math.cos(latitude) * math.cos(longitude)
        y += math.cos(latitude) * math.sin(longitude)
        z += math.sin(latitude)

    total = len(coordinates)
    x /= total
    y /= total
    z /= total

    central_longitude = math.degrees(math.atan2(y, x))
    central_square_root = math.sqrt(x * x + y * y)
    central_latitude = math.degrees(math.atan2(z, central_square_root))

    return central_latitude, central_longitude




def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place_name)
    if location:
        print(f"Location found: {place_name}")
        return location.latitude, location.longitude
    else:
        return None





def get_country_coordinates(place_name, api_key):
    geocoder = OpenCageGeocode(api_key)

    results = geocoder.geocode(place_name)

    if results and len(results) > 0:
        location = results[0]['geometry']
        return location['lat'], location['lng']
    else:
        return None, None








if __name__ == '__main__':
    country = 'Dominican Republic'
    latitude, longitude = get_country_coordinates(country, API_KEY)
    if latitude is not None and longitude is not None:
        print(f"Coordinates of {country}: Latitude = {latitude}, Longitude = {longitude}")
    else:
        print(f"Could not find coordinates for {country}.")
