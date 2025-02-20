import json
import numpy as np
# Helper function to find the intersection of two lists
def intersection(lst1: list, lst2: list) -> list:
    return [value for value in lst1 if value in lst2]

# Helper function to get unique values in a list
def unique(lst) -> list:
    return list(set(lst))
def js(dic: dict) -> str:
    #Makes variables usable with javascript. This is a last resort, and must ONLY be used if the variable won't also be used with HTML
    return json.dumps(dic)
def count_changes(lst):
    """Counts the number of times an item in a list changes."""
    if not lst:
        return 0
    mode = 1
    seq = 1
    count = 1
    prev = lst[0]
    for item in lst[1:]:
        if item != prev:
            count += 1
            prev = item
            seq = 1
        else:
            seq += 1
            if mode < seq:
                mode = seq
    return count, mode
def calculate_centroid(geolocations: list[dict]):
    #for all the stations in geolocations, calculate the centroid so the map can be properly centered.
    lat = float(0)
    lng = float(0)
    num_stations = len(geolocations)
    for station in geolocations:
        lat += float(station["lat"])
        lng += float(station["lon"])
    if num_stations == 0:
        return {"lat" : 0, "lon" : 0}
    return {"lat" : lat/num_stations, "lon" : lng/num_stations}
    
    
