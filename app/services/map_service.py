import math
import os
import folium
from folium.plugins import HeatMap
from app.repositories.stat_repo import calc_avg_casualties
from app.services.geolocation_service import get_centroid


def create_avg_map(limit=5):
    country_avg_fatality = calc_avg_casualties(limit)

    for doc in country_avg_fatality:
        doc['attack_locations'] = get_centroid(doc['attack_locations' ])

    m = folium.Map(location=[20.0, 0.0], zoom_start=3)

    for data in country_avg_fatality:
        lat = data['attack_locations'][0]
        lng = data['attack_locations'][1]
        avg_score = data['avg_fatality_score']

        if not (math.isnan(lat) or math.isnan(lng)):
            folium.Marker(
                location=[lat, lng],
                popup=f"{data['country']}: Avg Fatality Score = {avg_score:.2f}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        else:
            print(f"Skipping country {data['country']} due to invalid location")

    maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'maps')
    os.makedirs(maps_dir, exist_ok=True)
    map_path = os.path.join(maps_dir, 'average_fatality_score_map.html')

    m.save(map_path)
    print(f"Map has been created and saved at: {map_path}")
    return map_path

def create_most_active_group_map(top_groups: list[dict]):
    m = folium.Map(location=[20.0, 0.0], zoom_start=3)
    for doc in top_groups:
        lat = doc['location'][0]
        lng = doc['location'][1]
        groups = [({'Group name':g['group'],'count': g['count']}) for g in doc['top_groups']]

        if lat is not None and lng is not None:
            if not (math.isnan(lat) or math.isnan(lng)):
                folium.Marker(
                    location=[lat, lng],
                    popup=f"{groups}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
            else:
                print(f"Skipping country {doc['_id']} due to invalid location")

    maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'maps')
    os.makedirs(maps_dir, exist_ok=True)
    map_path = os.path.join(maps_dir, 'top_groups.html')

    m.save(map_path)
    print(f"Map has been created and saved at: {map_path}")
    return map_path


def create_geo_heat_map(docs):
    m = folium.Map(location=[20.0, 0.0], zoom_start=3)
    lat = []
    lng = []
    for doc in docs:
        if doc and 'latitude' in doc and 'longitude' in doc:
            if not (math.isnan(doc['latitude']) or math.isnan(doc['longitude'])):
                lat.append(doc['latitude'])
                lng.append(doc['longitude'])
    HeatMap(list(zip(lat, lng))).add_to(m)
    maps_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'maps')
    os.makedirs(maps_dir, exist_ok=True)
    map_path = os.path.join(maps_dir, 'geo_heat_map.html')
    m.save(map_path)
    print(f"Map has been created and saved at: {map_path}")
    return map_path




if __name__ == '__main__':
    create_avg_map()