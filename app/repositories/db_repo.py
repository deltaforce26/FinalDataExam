from app.db.mongo_db import initialize_mongo
from app.services.geolocation_service import get_country_coordinates
from app.settings.config import DB_URL, API_KEY


def add_lat_lon_based_on_city():
    attacks_col = initialize_mongo(DB_URL, "terror_attacks_db", "attacks")
    cities_col = initialize_mongo(DB_URL, "terror_attacks_db", "cities")
    docs = attacks_col.find()
    for doc in docs:
        if 'latitude' not in doc and 'longitude' not in doc:
            city_name = doc['city']
            if city_name and city_name != 'Unknown':
                city = cities_col.find_one({'city': city_name})
                if not city:
                    insert_city(city_name, cities_col)
                    city = cities_col.find_one({'city': city_name})
                if city and 'latitude' in city and 'longitude' in city:
                    lat = city['latitude']
                    lon = city['longitude']
                    if lat and lon:
                        attacks_col.update_one(
                            {"_id": doc["_id"]},
                            {"$set": {"latitude": lat, "longitude": lon}}
                        )
                        print(f"Updated {doc['_id']} with coordinates ({lat}, {lon}) for city {city_name}")
                    else:
                        print(f"Skipping {doc['_id']} due to invalid coordinates for city: {city_name}")



def insert_city(city_name, col):
    lat, lon = get_country_coordinates(city_name, API_KEY)
    if lat and lon:
        col.insert_one({"city": city_name, "latitude": lat, "longitude": lon})
        print(f"Inserted {city_name}")
    else:
        print(f"Skipping {city_name}")


if __name__ == '__main__':
    add_lat_lon_based_on_city()