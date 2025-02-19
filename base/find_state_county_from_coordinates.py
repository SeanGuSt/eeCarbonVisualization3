import geopandas, shapely
import numpy as np

# Define file paths for GeoJSON files containing county and state geometries
COUNTY_FILEPATH = "Replace this with the filepath for counties.geojson"
STATE_FILEPATH = "Replace this with the filepath for states.geojson"

# Load GeoJSON data into GeoDataFrames for counties and states
counties = geopandas.read_file(COUNTY_FILEPATH)
states = geopandas.read_file(STATE_FILEPATH)

def findPointInPolygon(lat: float, long: float) -> tuple[str, str, str, str]:
    """
    Given a latitude and longitude, this function determines which state and county 
    the point lies within using geometric containment tests.
    
    Args:
    lat (float): The latitude of the point.
    long (float): The longitude of the point.
    
    Returns:
    tuple: A tuple containing state name, county name, state ID, and county ID.
    """
    
    # Create a Point object using the provided latitude and longitude
    geom = np.array([shapely.Point(long, lat)])  # Format the latitude and longitude as done in geojson.

    # Iterate through each state to check if the point is inside the state's geometry
    for state_name, state in zip(states["name"], states["geometry"]):
        if shapely.contains(state, geom)[0]:  # Check if the point is inside the state's geometry
            # If the point is in the state, find the counties that belong to this state
            state_counties = counties[counties["state"] == state_name]
            # Retrieve the state ID (used later for returning as a result)
            state_id = counties["STATEFP"][0]
            
            # Iterate through each county in the state to check if the point is inside any county's geometry
            for county_name, county, county_id in zip(state_counties["name"], state_counties["geometry"], state_counties["COUNTYFP"]):
                if shapely.contains(county, geom)[0]:  # Check if the point is inside the county's geometry
                    # If point is in the county, return the state and county names, along with their IDs
                    return state_name, county_name, state_id, county_id
    
    # Return empty strings if the point is not inside any state or county
    return "", "", "", ""

# Example usage: Find the state and county for a specific latitude and longitude
state_name, county_name, state_id, county_id = findPointInPolygon(32.7357, 97.1081)

# Print the result (county and state names)
print(f"{county_name}, {state_name}")
