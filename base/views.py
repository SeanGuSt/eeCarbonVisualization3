from django.db.models import F, Q, Count
from django.db.models.fields.json import KT
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
import shapely
# from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.db.models.functions import Distance
#from django.contrib.gis.measure import D
from .static.scripts.python.other import js, count_changes, json
from .models import Site, Pedon, Standard, Synonym, Source, Dataset, fetch_data
from scipy.interpolate import PchipInterpolator
from scipy.integrate import quad
import numpy as np
import pandas as pd
import ast
from .constant import PEDON_NAM, SITE_NAM, TOP, BOTTOM, SITE_ID, PEDON_ID, SOC, LAT_LONG_NAME, LAT, LONG
already_loaded = []
hold_spline_for_download = []
#footer_keys are the keys to the dictionary superDict
summary_keys = list(Standard.objects.filter(summary = True).values_list("name", flat = True))
#footer_values are the values that will go in the tooltips
summary_values = summary_keys
df = pd.DataFrame(columns = summary_keys)
df_xl = pd.DataFrame(columns = summary_keys)

#These two are the main pages of the app
class IndexView(generic.ListView):
    context_object_name = "Sites"
    template_name = "searcher/stationFinder.html"
    def get_queryset(self) -> dict[str, str]:
        print("Finding geolocations...")
        initial_geocenter = {"lat" : 44.967, "lon" : -106.233}#calculate_centroid(geolocations)#Where the map should be centered
        # Annotate each county with the count of Sites in that county
        state_counts = Pedon.objects.values('site__state').annotate(count=Count('site__state')).order_by('site__state')
        county_counts = Pedon.objects.values('site__county').annotate(count=Count('site__county')).order_by('site__county')
        # Now, county_counts is a queryset where each item is a dictionary
        # with 'county' and 'count' (the number of Sites in that county)
        state_count_dict = {entry['site__state']: entry['count'] for entry in state_counts}
        county_count_dict = {entry['site__county']: entry['count'] for entry in county_counts}
        return {"initial_geocenter" : js(initial_geocenter)}#, "summary_keys" : js(summary_keys)}


class DetailedView(generic.TemplateView):
    template_name = "searcher/detailedStation.html"
    def get_context_data(self, **kwargs) -> dict:
        sites = get_sites_in_place(self.request)
        append_data_if_new(sites)
        pedons = Pedon.objects.filter(site__in = sites)
        sources = Source.objects.filter(id__in=pedons.values_list('site__source__id', flat=True))
        # Step 1: Retrieve all Dataset objects related to these sources
        datasets = Dataset.objects.filter(source__in=sources)
        # Step 2: Retrieve all Synonym objects related to these datasets
        synonyms = Synonym.objects.filter(dataset__in=datasets)
        # Step 3: Retrieve all Standard objects related to these synonyms
        standards = Standard.objects.filter(id__in=synonyms.values_list('standard__id', flat=True), canSpline = True)
        return {"pedons" : pedons, "standards" : standards}
    

def get_pedon_for_radio(request: HttpRequest):
    sites = get_sites_in_place(request)
    standard = request.GET.get("standard")
    pedons = Pedon.objects.filter(site__in = sites)
    pedons = pedons.annotate(get_standard = KT("splineCoeffs__" + standard)).exclude(get_standard = {})
    superList = {f"pedon_{pedon.name}_{pedon.pedon_id}_{pedon.site.site_id}_{pedon.site.source.name}" : pedon.name for pedon in pedons }
    json_stuff = js(superList)
    return HttpResponse(json_stuff, content_type="application/json")


def append_data_if_new(reqSites: QuerySet[Site]):
    """
    Appends new data to the global dataframe (`df`) for sites not previously loaded. 
    If the data source type is 'XL', it will be appended to a separate dataframe (`df_xl`). 
    The function checks for already loaded sources to avoid redundant loading and fetches data for new sources. 
    It returns the list of sites that were processed during this operation.

    Args:
        reqSites (QuerySet[Site]): A queryset of the sites to be processed.

    Returns:
        QuerySet[Site]: A queryset of the sites that were processed.
    """
    
    global df, df_xl  # Declare global variables for the dataframes that store the data.

    # Initialize a new empty DataFrame `df` with predefined column names from `summary_keys`.
    df = pd.DataFrame(columns=summary_keys)

    # Initialize a list to track sources that have already been loaded (temporary for this request).
    temp_already_loaded = []

    # Check if there are sites to process.
    if reqSites:
        # Iterate over each site in the request's sites.
        for site in reqSites:
            source = site.source  # Extract the source of the site.
            # Check if the source hasn't been loaded yet and its type is "XL".
            if source not in already_loaded and source.type == "XL":
                # Mark this source as loaded.
                already_loaded.append(source)
                # Fetch new data for this source and add the source name.
                dfNew = fetch_data(source)
                dfNew["Source"] = source.name
                # Concatenate the new data to the `df_xl` dataframe (which stores XL sources).
                df_xl = pd.concat([df_xl, dfNew])

            # If the source is not of type "XL" and hasn't been processed in this request.
            elif source not in temp_already_loaded and source.type != "XL":
                # Mark this source as loaded in the temporary list.
                temp_already_loaded.append(source)
                # Fetch new data for this source, limiting it to the relevant sites.
                dfNew = fetch_data(source, include = summary_keys, where=reqSites)
                dfNew["Source"] = source.name
                # Append this data to the main `df` dataframe.
                df = pd.concat([df, dfNew.dropna(axis=1, how='all')])
        # If there is data in `df_xl`, filter and append relevant data to `df`.
        if not df_xl.empty:
            df = pd.concat([df, df_xl[df_xl[SITE_NAM].isin(list(reqSites.values_list("name", flat=True)))]])
        
        # Clean the dataframe by inferring object types and filling missing values with -1.
        
        df = df.infer_objects(copy=False).fillna(-1)
        if SITE_ID in df.columns:
            if df[SITE_ID].nunique() == 1:
                df[SITE_ID] = df[SITE_NAM]
        if PEDON_ID in df.columns:
            if df[PEDON_ID].nunique() == 1:
                df[PEDON_ID] = df[PEDON_NAM]



def get_sites_in_place(request: HttpRequest) -> QuerySet[Site]:
    """
    Returns a queryset of `Site` objects filtered by the type and name specified in the request.
    The function can filter by state, county, or individual station depending on the request parameters.
    If the type and name parameters do not match expected values, it returns an empty queryset.

    Args:
        request (HttpRequest): The HTTP request containing parameters for filtering sites.

    Returns:
        QuerySet[Site]: A queryset of `Site` objects that match the filter criteria.
    """
    
    # Extract the 'type' (state, county, or individual station) and 'name' from the request parameters.
    if request.method == "GET":
        request_type = request.GET.get("type")
        place_name = request.GET.get("name")
    else:
        data = json.loads(request.body)
        request_type = data.get("type")
        place_name = data.get("name")
    print(request_type)
    # Match the place type and filter the sites accordingly.
    match request_type:
        case "State":
            # Filter by state name (distinct values to avoid duplicates).
            return Site.objects.filter(state=place_name).distinct()
        
        case "County":
            # Split the place name into county and state, then filter by both.
            county_state = place_name.split(", ")
            return Site.objects.filter(county=county_state[0], state=county_state[1]).distinct()
        
        case "Shape":
            polygon = shapely.from_geojson(json.dumps(json.loads(request.body).get("user_drawn_polygon")))
            site_names = []
            for site in Site.objects.all():
                geom = np.array([shapely.Point(site.longitude, site.latitude)])
                if shapely.contains(polygon, geom)[0]:
                    site_names.append(site.name)
            return Site.objects.filter(name__in = site_names)
            # return Site.objects.filter(location__within = polygon)
        
        case "Individual Site":
            # Extract additional identifiers for individual site filtering.
            site_id = request.GET.get("site_id")
            site_source = request.GET.get("site_source")
            # Filter by name, site_id, and source name.
            return Site.objects.filter(name=place_name, site_id=site_id, source__name=site_source)
        
        case "Request":
            pedon_ids = json.dumps(json.loads(request.body).get("user_given_pedon_list"))
            print(pedon_ids)
            pedons = Site.objects.filter(site_id__in = pedon_ids)
            return pedons #Site.objects.filter(id__in = sites)

    
    # If request_type does not match any of the above, return an empty queryset.
    return Site.objects.none()


def load_layer(request: HttpRequest) -> HttpResponse:
    """
    Loads and processes soil layer data, preparing it for visualization in a JSON format.
    The function extracts necessary data from the global dataframe (`df`) and processes it into a 
    dictionary format suitable for use in a JavaScript-based frontend.

    Args:
        request (HttpRequest): The HTTP request containing site data to process.

    Returns:
        HttpResponse: A JSON response containing the processed soil layer data.
    """

    # Retrieve the sites related to the current request and load additional data.
    reqSites = get_sites_in_place(request)
    append_data_if_new(reqSites)
    # Extract the names of the sites to include them in the response.
    sites = list(reqSites.values_list("name", flat=True))
    layers = df  # Load the global dataframe `df` that contains the layers' data.
    pedon_list = layers[PEDON_NAM].to_list()  # Extract the list of pedons (soil samples).

    # If there are no pedons, return an empty JSON response with a "layer_" key.
    if len(pedon_list) == 0:
        superDict = {"layer_": []}
        json_stuff = js(superDict)  # Convert the dictionary to JSON.
        return HttpResponse(json_stuff, content_type="application/json")

    # Count the number of samples and layers in the pedon data.
    num_samples, num_layers = count_changes(pedon_list)
    print(f'Pedon collection has {num_samples} pedons each having at most {num_layers} layers')

    # Inner function to prepare data for visualization in a box plot (used in JavaScript).
    def prep_data_4_box_js(myList: list) -> list:
        """
        Organizes the data into a 2D array format for visualization.
        Each element of the list corresponds to a pedon and each column to a layer.
        """
        layer_num = -1
        sample_num = 0
        data = [[0] * num_samples for _ in range(num_layers)]
        current_pedon = pedon_list[0]
        for i in range(len(pedon_list)):
            if current_pedon != pedon_list[i]:
                sample_num += 1
                layer_num = -1
                current_pedon = pedon_list[i]
            layer_num += 1
            data[layer_num][sample_num] = myList[i]
        return data

    # Prepare the main dictionary with site names, footer keys, and footer values.
    superDict = {"site": sites, "footer_keys": summary_keys, "footer_values": summary_values}
    for key in summary_keys:
        superDict[key] = prep_data_4_box_js(layers[key].to_list())
    
    # Calculate the layer thickness (difference between BOTTOM and TOP).
    print(layers[BOTTOM])
    print(layers[TOP])
    superDict["data"] = prep_data_4_box_js(np.subtract(layers[BOTTOM].to_list(), layers[TOP].to_list()))
    
    # Create a list of layer numbers.
    superDict["layer_"] = np.arange(1, num_layers + 1).tolist()

    # Convert the dictionary to JSON and return as an HTTP response.
    json_stuff = js(superDict)
    return HttpResponse(json_stuff, content_type="application/json")



def download_layer(request: HttpRequest) -> HttpResponse:
    """
    Generates a CSV file for downloading that contains the soil layer data stored in the global dataframe (`df`).

    Args:
        request (HttpRequest): The HTTP request that triggers the CSV download.

    Returns:
        HttpResponse: A CSV file containing the layer data.
    """
    
    # Create an HTTP response with a content type for CSV files.
    response = HttpResponse(content_type='text/csv')
    # Set the filename for the CSV download.
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # Write the global dataframe `df` to the response in CSV format (without the index).
    df.to_csv(response, index=False)
    return response

def download_spline(request: HttpRequest) -> HttpResponse:
    """
    Generates a CSV file for downloading that contains the soil layer data stored in the global dataframe (`df`).

    Args:
        request (HttpRequest): The HTTP request that triggers the CSV download.

    Returns:
        HttpResponse: A CSV file containing the layer data.
    """
    x = np.arange(len(hold_spline_for_download))
    sp_df = pd.DataFrame(data = {"x" : x, "y" : hold_spline_for_download})
    # Create an HTTP response with a content type for CSV files.
    response = HttpResponse(content_type='text/csv')
    # Set the filename for the CSV download.
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    # Write the global dataframe `df` to the response in CSV format (without the index).
    sp_df.to_csv(response, index=False)
    return response

def spline(request: HttpRequest) -> HttpResponse:
    """
    Retrieves and processes spline coefficient data for pedons from a given site. 
    It calculates the averages of specific spline variables and returns them in JSON format for frontend display.

    Args:
        request (HttpRequest): The HTTP request containing site data for which the spline data is calculated.

    Returns:
        HttpResponse: A JSON response containing the averaged spline data for the layers.
    """
    
    # Get the sites related to the current request and load necessary data.
    reqSites = get_sites_in_place(request)
    
    # Retrieve the names of spline keys that can be used for averaging.
    spline_keys = list(Standard.objects.filter(summary=True, canSpline=True).values_list("name", flat=True))
    
    # Prepare the initial structure of the response.
    superDict = {"site": ["Spline Output Average"], "footer_keys": spline_keys, "footer_values": spline_keys}

    # Inner function to get the average values for a specific spline variable.
    def get_averages(var: str, pedons: QuerySet[Pedon]) -> list:
        """
        Retrieves the spline coefficients for each pedon and calculates the averages for a given variable.
        """
        arrays = []
        for pedon in pedons:
            pedonCoeffs = pedon.splineCoeffs
            if pedonCoeffs.get(var):
                if type(pedonCoeffs[var]) is dict:
                    arrays.append(np.array(pedonCoeffs[var]["y"]))
        
        # Calculate the averages across all the arrays of the spline variable.
        averages = []
        if len(arrays) == 0:
            return averages
        max_length = max(len(arr) for arr in arrays)
        for i in range(max_length):
            column_values = [arr[i] for arr in arrays if i < len(arr)]
            averages.append([np.round(np.mean(column_values), 3)])
        return averages
    
    # Calculate the averages for each spline key.
    pedons = Pedon.objects.filter(site__in=reqSites)
    for var in spline_keys:
        superDict[var] = get_averages(var, pedons)
    
    # Ensure all spline variables have the same number of layers by adding -1 for missing layers.
    num_layers = max(len(superDict[var]) for var in spline_keys)
    for var in spline_keys:
        num_to_add = num_layers - len(superDict[var])
        if num_to_add > 0:
            superDict[var].extend([-1] * num_to_add)
    
    # Prepare the data for layers and return it in the response.
    superDict["data"] = [[10]] * num_layers
    superDict["layer_"] = np.arange(1, num_layers + 1).tolist()
    
    # Convert the dictionary to JSON and return as an HTTP response.
    json_stuff = js(superDict)
    return HttpResponse(json_stuff, content_type="application/json")
    
    
def get_spline_line(request: HttpRequest) -> HttpResponse:
    global hold_spline_for_download
    """
    This function handles the process of calculating the spline line for a given pedon based on the 
    coefficients stored in the database. It performs cubic spline interpolation for variables associated 
    with the pedon and returns the predicted values as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object containing the query parameters 'name', 'id', and 'var',
                                which are used to filter the pedons in the database.

    Returns:
        HttpResponse: A JSON response containing the predicted x and y values for the spline line, 
                       along with the observed x and y values ('y0') used in the interpolation.
    """
    
    # Initialize variables and CubicSpline object

    default_upper_bound = 201  # Default value for upper bound of x values for prediction
    x_pred = np.arange(default_upper_bound)  # x values to predict (from 0 to default_upper_bound)
    y_pred = np.zeros(default_upper_bound)  # Array to store the predicted y values (initialized to 0)
    denom = np.zeros(default_upper_bound)  # Array to track the number of predictions at each x value

    # Fetch pedons matching the name and pedon_id from the GET request parameters
    pedons = Pedon.objects.filter(name=request.GET.get("name"), pedon_id=request.GET.get("id"))
    var = request.GET.get("var")
    
    # Convert the dataframe to ensure PEDON_ID is of type string for correct indexing later
    dfTemp = df.astype({PEDON_ID: 'str'})
    dfTemp[PEDON_ID] = dfTemp[PEDON_ID].astype(str).str.replace('.0', '', regex=False)
    # Loop through all the pedons (soil samples) returned by the filter query
    for pedon in pedons:
        cs = prep_pchip(pedon, var)
        print(dfTemp)
        x_obs, y_obs, xy = prep_observed(cs, dfTemp.loc[dfTemp[PEDON_ID] == pedon.pedon_id, var])
        
        # Masking: create a mask for x_pred values that are within the range of x_obs
        mask = np.ones(len(x_pred), dtype=bool)
        mask[x_pred > x_obs[-1]] = False  # Remove points where x_pred is larger than the last observed x value

        # Add predictions to y_pred, for positions where the mask is True
        y_pred[mask] += cs(x_pred)[mask]
        denom[mask] += 1  # Keep track of the number of times a particular x_pred was predicted

        # Masking again: Remove depths that exceed the maximum observed x value
        mask = np.ones(len(denom), dtype=bool)
        mask[denom == 0] = False  # Remove values where denom is zero (i.e., points that were not predicted)

        # Apply the mask to remove depths and scale the predictions
        x_pred = x_pred[mask]
        y_pred = y_pred[mask] / denom[mask]  # Normalize the predictions by the number of times predicted
        # Exit the outer loop after processing the first pedon (break after first pedon)
        break
    hold_spline_for_download = y_pred.tolist()
    # Prepare a dictionary with the x and y values for the spline
    superDict = {"x": x_pred.tolist(), "y": y_pred.tolist(), "y0": xy}
    print(xy)
    # Convert the dictionary into JSON format
    json_stuff = js(superDict)

    # Return the JSON response with content type "application/json"
    return HttpResponse(json_stuff, content_type="application/json")

def get_spline_area_average(request: HttpRequest) -> HttpResponse:
    # Fetch pedons matching the name and pedon_id from the GET request parameters
    pedons = Pedon.objects.filter(name=request.GET.get("name"), pedon_id=request.GET.get("id"))
    var = request.GET.get("var")

    # Convert the dataframe to ensure PEDON_ID is of type string for correct indexing later
    dfTemp = df.astype({PEDON_ID: 'str'})
    dfTemp[PEDON_ID] = dfTemp[PEDON_ID].astype(str).str.replace('.0', '', regex=False)
    x_min = float(request.GET.get("x_min"))
    x_max = float(request.GET.get("x_max"))

    for pedon in pedons:
        pchip = prep_pchip(pedon, var)
        area, err =  quad(pchip, x_min, x_max)#(max_integrate - min_integrate)#/(x_max - x_min)
        x = np.arange(x_min, x_max+1)
        y = pchip(x)
        break
    area /= (x_max - x_min)
    superDict = {"area": area, "x" : x.tolist(), "y" : y.tolist()}
    
    # Convert the dictionary into JSON format
    json_stuff = js(superDict)

    # Return the JSON response with content type "application/json"
    return HttpResponse(json_stuff, content_type="application/json")


def prep_observed(pchip: PchipInterpolator, real_y_vals: pd.Series):
    # Create a new x_obs array based on the cubic spline x values
    x_obs = np.arange(pchip.x.size + 1)  # Generate initial x_obs values
    for i in range(pchip.x.size):
        x_obs[i+1] = 2 * pchip.x[i] - x_obs[i]  # Update x_obs values using a specific formula
    x_obs = np.delete(x_obs, 1)  # Delete the first element as it's the 1 cm we added
    # Get observed y values from the dataframe for the given variable and pedon
    y_obs = np.array(real_y_vals)
    # Create a list of x, y pairs for the current variable
    xy = [{"x": X, "y": Y} for X, Y in zip([(x_obs[i] + x_obs[i+1]) / 2 for i in range(len(x_obs) - 1)], y_obs)]
    print(x_obs)
    print(y_obs)
    print(xy)
    return x_obs, y_obs, xy


def prep_pchip(pedon: Pedon, var: str) -> PchipInterpolator:
    pchip = PchipInterpolator([0, 1], [0, 1])  # Initialize a pchip interpolator object (dummy with [0,1] as initial values)
    # Parse the spline coefficients and x values for the pedon from the database
    pedonCoeffs = pedon.splineCoeffs
    pchip.x = np.array(pedon.x) # Set the x values of the spline
    # Set the cubic spline coefficients for the current variable
    pchip.c = np.array(pedonCoeffs[var]["c"])  # Assign the coefficients for the spline
    return pchip