
from django.db.utils import IntegrityError
from django.conf import settings
import warnings, time, os, geopandas, shapely
from .models import Source, Site, Standard, Dataset, Synonym, Model, Pedon, fetch_data
from global_land_mask import globe
import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator
from django.http import HttpResponse, HttpRequest
from .constant import DATABASE, DATASET_TYPE, SITE_ID, PEDON_ID, URL, LAT, LONG, LAT_LONG_NAME, SITE_NAM, TOP, BOTTOM, PEDON_NAM, LAYER_NAM
filepath = os.path.join(settings.BASE_DIR, "base\SynonymBook.xlsx")
df_syn = pd.read_excel(filepath).sort_values(by = "Merger", ascending = False)
df_std = pd.read_excel(filepath, sheet_name="Glossary")
df_seg = pd.read_excel(filepath, sheet_name="Variable Segregation")
counties = geopandas.read_file(os.path.join(settings.BASE_DIR, "base\static\scripts\geoJSON\counties.geojson"))
states = geopandas.read_file(os.path.join(settings.BASE_DIR, "base\static\scripts\geoJSON\states.geojson"))


def catchRepeat(modl: Model, Dict: dict[str, ]) -> Model | bool:
    #We want each instance of a model to have a unique name.
    #Returns the model created (or that had already been created)
    try:
        modl(**Dict).save()
    except IntegrityError as e:#Raise warning if instance with this name already exists
        print(f'{Dict["name"]} is already represented.')
    except ValueError:
        return False
    if Dict["name"] == "None" or not Dict["name"]:
        return False
    if modl == Synonym:
        return modl.objects.get(name = Dict["name"], standard = Dict["standard"])
    if modl == Site:
        return modl.objects.get(name = Dict["name"], source = Dict["source"], site_id = Dict["site_id"])
    if modl == Pedon:
        return modl.objects.get(name = Dict["name"], site = Dict["site"], pedon_id = Dict["pedon_id"])
            
    return modl.objects.get(name = Dict["name"])


def standardMaker():
    for _, std in df_std.iterrows():
        stdDict = {"name" : std["Standard"],
                   "summary" : std["Summary"],
                   "canSpline" : std["Splinable"],
                   }
        catchRepeat(Standard, stdDict)


def sourceMaker(Dict: dict[str, str]) -> tuple[Model | bool, pd.Series, pd.Series, pd.Series]:
    mSource = catchRepeat(Source, Dict)
    keys = df_syn.loc[df_syn[DATABASE] == mSource.name].dropna(axis=1)
    return mSource, keys["Standard"], keys["Synonym"], keys["Table"]


def synMaker(mSource: Source, standards: pd.Series, synonyms: pd.Series):
        print(f'Storing {mSource.name} synonyms...')
        t0 = time.time()
        for standard_name, synonym_name in zip(standards, synonyms):
            standard = Standard.objects.get(name = standard_name)
            synDict = {"name" : synonym_name,
                    "standard" : standard}
            catchRepeat(Synonym, synDict)
        t1 = time.time()
        print(f'Synonyms stored! Time to store: {round(t1 - t0, 3)} seconds.')


def datasetMaker(mSource: Source, standards: pd.Series, synonyms: pd.Series, tables: pd.Series):
    print("Creating Dataset memory")
    for _, row in df_seg.loc[df_seg[DATABASE] == mSource.name].iterrows():
        dtstDict = {
            "name" : row["Name"],
            "source" : mSource,
            "file" : row[URL],
            "delimiter" : row["Delimiter"]
        }
        dtst = catchRepeat(Dataset, dtstDict)
        for synonym_name, std, tbl in zip(synonyms, standards, tables):
            if tbl != row["Name"]:
                continue
            #Get each of the Synonyms found in this file and associate them with this Dataset
            standard = Standard.objects.get(name = std)
            Synonym.objects.get(name = synonym_name, standard = standard).dataset.add(dtst)


def siteMaker(mSource: Source):
    """
    Given a data source, this function extracts the individual sites from its databases.
    
    Args:
    mSource (Source): The source of the data we're looking at.
    
    Returns:
    Nothing
    """
    # Print a message indicating the source and that location data is being fetched
    print(f"Fetching {mSource.name} location data...")
    
    # Record the time to measure how long the data fetching takes
    t0 = time.time()

    # Fetch location data from the provided source, including latitude, longitude, site ID, etc.
    df = fetch_data(mSource, [LAT, LONG, LAT_LONG_NAME, SITE_ID, SITE_NAM])

    # Remove duplicate rows from the dataframe (if any)
    dfSite = df.drop_duplicates()

    # Record the time after fetching the data
    t1 = time.time()

    # Print the time taken to fetch the data
    print(f'Data fetched! Time to fetch: {round(t1-t0, 3)} seconds.')

    # Print a message indicating that the data is being stored
    print(f'Storing {mSource.name} sites...')

    # Initialize a counter to track how many sites are skipped due to invalid data
    invalid_sites_skipped = 0
    invalid_sites_tolerance = 100000

    # Check if the "site_id" column exists in the dataframe
    site_id_unique = SITE_ID in dfSite.columns

    # Iterate through each row of the dataframe
    for _, site in dfSite.iterrows():
        try:
            # Try to extract latitude and longitude values, and convert them to floats
            lat = float(site[LAT])
            long = float(site[LONG])

            # Check if the coordinates are valid (NaN check)
            if lat != lat or long != long:  # This checks for NaN
                raise Exception()
        except:
            # If there's an issue with the coordinates, increment the counter and skip the site
            invalid_sites_skipped += 1
            print(f"Something is wrong with {site[LAT_LONG_NAME]}'s coordinates of {lat} and {long}. Omitting from database.")
            continue

        # If more than invalid_sites_tolerance sites have been skipped, break the loop
        if  invalid_sites_skipped > invalid_sites_tolerance:
            break
        
        # Check if the site is on land 
        if globe.is_land(lat, long):
            try:
                # Try to find the state and county information based on the coordinates
                state, county, state_id, id = findPointInPolygon(lat, long)
            except shapely.errors.GEOSException:
                # If there's an error with the geospatial query, skip this site
                print(f"Something is wrong with {site[LAT_LONG_NAME]}'s coordinates of lat. {lat} and lon. {long}. Omitting from database.")
                invalid_sites_skipped += 1
                continue
            
            # Create a dictionary to store the site data
            siteDict = {
                "name" : site[LAT_LONG_NAME],  # Name of the site
                "latitude" : lat,  # Latitude of the site
                "longitude" : long,  # Longitude of the site
                "source" : mSource,  # Source of the data
                "state" : state,  # State the site is located in
                "county" : county,  # County the site is located in
                "site_id" : site[LAT_LONG_NAME],  # Use the name as the site_id by default
                "state_id": state_id,  # State ID
                "county_id" : id  # County ID
            }

            # If the dataframe contains unique site IDs, use the ID from the dataframe
            if site_id_unique:
                siteDict["site_id"] = site[SITE_ID]

            # If the source is "KSSL", adjust the name and site ID by removing the last two characters
            # This is done to avoid using floats for names
            if mSource.name == "KSSL":
                siteDict["name"] = str(siteDict["name"])[:-2]
                siteDict["site_id"] = str(siteDict["site_id"])[:-2]
            
            # Call the catchRepeat function to store the site data, avoiding duplicates
            catchRepeat(Site, siteDict)

    # Record the time after storing the sites
    t2 = time.time()
    print(f'Sites stored! Time to store: {round(t2-t1, 3)} seconds with {invalid_sites_skipped} sites skipped.')


def pedonMaker(mSource: Source):
    # Print a message indicating that spline coefficients are being calculated for the given source
    print(f"Calculating {mSource.name} spline coefficients...")
    
    # Record the start time for performance measurement
    t0 = time.time()

    # Fetch data using the source, columns specified, and return a pandas DataFrame
    datasets = Dataset.objects.filter(source=mSource)
    var_names = []
    for dataset in datasets:
        merge_on = dataset.synonym_set.all().filter(standard__canSpline = True)
        var_names.extend(list(set(merge_on.values_list("standard__name", flat = True))))
    print(var_names)
    standard_names = [SITE_NAM, SITE_ID, PEDON_ID, PEDON_NAM, LAYER_NAM, TOP, BOTTOM]
    standard_names.extend(var_names)
    df = fetch_data(mSource, standard_names)  # Returns a pandas dataframe

    # Function to calculate cubic spline coefficients for given x, y values
    def spliner(x: np.ndarray, y: np.ndarray) -> dict[str, list]:
        # Create a CubicSpline object to calculate the coefficients
        cs = PchipInterpolator(x, y)
        
        # Initialize an empty list to store interpolated values
        y1 = []
        i = 5
        # Interpolate and calculate values from 5 to the maximum value in x, with a step of 10
        while i <= x[-1]: 
            y1.append(np.round(cs(i), 2).item())  # Interpolate at each point and round to 2 decimal places
            i += 10
        
        # Shorten coefficients to 5 decimals in scientific notation to reduce storage
        c = [[float(f"{p:.7e}") for p in f] for f in cs.c.tolist()]
        
        return {"c": c, "y": y1}
    
    # Loop through all Sites in the database that match the given source
    for site in Site.objects.filter(source=mSource):
        # Select rows from the dataframe where the site name matches the current site
        dfSite = df.loc[df[SITE_NAM].astype(str) == str(site.name)]
        
        # Get unique pedon names for this site
        pedons = dfSite[PEDON_NAM].drop_duplicates().to_list()
        
        coeffBulk = {}  # Placeholder for bulk coefficients
        coeffSOC = {}   # Placeholder for SOC coefficients
        
        pedon_id_unique = PEDON_ID in dfSite.columns  # Check if PEDON_ID exists in the dataframe columns
        
        # Initialize a dictionary to store the spline coefficients
        sv_dict = {var: '{}' for var in var_names}

        # Loop through each pedon for the current site
        for pedon in pedons:
            # Initialize a dictionary to store the pedon information
            pedonDict = {
                "name": pedon,        # Pedon name
                "pedon_id": pedon,    # Use the Pedon's name by default
                "splineCoeffs": sv_dict,  # Placeholder for spline coefficients
                "site": site           # The site associated with this pedon
            }

            # Get layers of data specific to the current pedon
            dfLayers = dfSite.loc[dfSite[PEDON_NAM] == pedon]
            
            # If pedon_id is unique, assign it to the dictionary from the dataframe
            if pedon_id_unique:
                pedonDict["pedon_id"] = dfLayers[PEDON_ID].iloc[0]

            # Get the layer depth values (TOP and BOTTOM) and append the last bottom depth value
            points = dfLayers[TOP].to_list()
            points.append(dfLayers[BOTTOM].iloc[-1])

            # Skip if any depth is missing or overlaps
            if "" in points:
                print(f"Skipping {pedon}. A layer depth measurement is empty: {points}")
            elif any([points[i] > points[i + 1] for i in range(len(points) - 1)]):
                print(f"Skipping {pedon}. The layers should not overlap: {points}")
            else:
                # If there are more than two points, prepare the 'x' values for interpolation
                if len(points) > 2:
                    points.insert(1, 1)  # Insert a 1 cm layer at start to ensure the surface data isn't exaggerated
                    if points[-1] == points[-2]:
                        points[-1] += 10  # Ensure the last two points are distinct
                    x = np.array([(points[i] + points[i+1])/2 for i in range(len(points) - 1)])  # Midpoint for interpolation
                    if np.any(np.isnan(x)):
                        continue
                    pedonDict["x"] = x.tolist()

                # Loop through each variable and calculate the spline coefficients if possible
                for var in var_names:
                    var_isna = dfLayers[var].isna()  # Check if the variable has missing values
                    if var_isna.any():
                        print(f"Skipping {var} spline coefficients for {pedon}. {dfLayers[var].tolist()} cannot be used.")
                    else:
                        try:
                            if len(points) == 2:
                                # If there are only two points, apply spline to those
                                sv_dict[var] = spliner(points, np.array([dfLayers[var][0], dfLayers[var][0]]))
                            else:
                                # Otherwise, apply spline to the actual data points
                                y = dfLayers[var].tolist()
                                y.insert(1, y[0])  # Insert a copy of the first value (for a better interpolation fit)
                                sv_dict[var] = spliner(x, y)
                        except:
                            # Handle any exceptions during spline calculation
                            print(f"Skipping {var} spline coefficients for {pedon}. For some unknown reason.")

            # Save the final pedon dictionary (with computed spline coefficients)
            pedonDict["splineCoeffs"] = sv_dict
            # Call the catchRepeat function to handle saving or avoiding duplicates
            catchRepeat(Pedon, pedonDict)

    Site.objects.filter(source = mSource, pedon__isnull=True).delete()
    # Record the time after storing the sites
    t1 = time.time()
    print(f'Pedons stored! Time to store: {round(t1-t0, 3)} seconds.')

    

def findPointInPolygon(lat: float, long: float) -> tuple[str, str, str, str]:
    geom = np.array([shapely.Point(long, lat)])#Format the latitude and longitude as done in geojson.
    for state_name, state in zip(states["name"], states["geometry"]):
        if shapely.contains(state, geom)[0]:#geom's point is inside the geometry of state.
            state_counties = counties[counties["state"] == state_name]#If it is, we check for which county from that state it's in. 
            state_id = counties["STATEFP"][0]
            for county_name, county, county_id in zip(state_counties["name"], state_counties["geometry"], state_counties["COUNTYFP"]):
                if shapely.contains(county, geom)[0]:
                    return state_name, county_name, state_id, county_id
    return "", "", "", ""


def maker_reset():
    Source.objects.all().delete(), Dataset.objects.all().delete(), Standard.objects.all().delete(), Synonym.objects.all().delete()
    Site.objects.all().delete(), Pedon.objects.all().delete()
    standardMaker()
    
def maker(Dict: dict):
    Source.objects.filter(name = Dict["name"]).delete()
    mSource, standards, synonyms, tables = sourceMaker(Dict)
    synMaker(mSource, standards, synonyms)
    datasetMaker(mSource, standards, synonyms, tables)
    siteMaker(mSource)
    pedonMaker(mSource)