from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .static.scripts.python.other import js, count_changes
from .models import Site, Pedon, Standard, Synonym, Source, fetch_data
from scipy.interpolate import CubicSpline
import numpy as np
import pandas as pd
import ast
from .constant import LAT, LONG, LAT_LONG_NAME, PEDON_NAM, SITE_NAM, TOP, BOTTOM, SOC, LAYER_NAM, SITE_ID, PEDON_ID
already_loaded = []
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
        #geolocations = [{"lat" : site.latitude, "lon" : site.longitude} for site in Pedon.objects.all()]
        #sites = [site.name for site in Pedon.objects.all()]
        initial_geocenter = {"lat" : 44.967, "lon" : -106.233}#calculate_centroid(geolocations)#Where the map should be centered
        #return {"geolocations": js(geolocations), "initial_geocenter" : js(initial_geocenter), "sites" : js(sites)}
        return {"initial_geocenter" : js(initial_geocenter)}#, "summary_keys" : js(summary_keys)}


class DetailedView(generic.TemplateView):
    template_name = "searcher/detailedStation.html"
    def get_context_data(self, **kwargs) -> dict:
        sites = get_sites_in_place(self.request)
        return {"sites" : sites}


def append_data_if_new(request: HttpRequest) -> QuerySet[Site]:
    global df, df_xl
    df = pd.DataFrame(columns = summary_keys)
    reqSites = get_sites_in_place(request)
    temp_already_loaded = []
    if reqSites:
        for site in reqSites:
            source = site.source
            if source not in already_loaded and source.type == "XL":#If the source has already been loaded, there's no point loading it again.
                already_loaded.append(source)
                dfNew = fetch_data(source, exclude = [LAT_LONG_NAME, LAT, LONG])
                dfNew["Source"] = source.name
                df_xl = pd.concat([df_xl, dfNew])
            elif source not in temp_already_loaded and source.type != "XL":
                temp_already_loaded.append(source)
                dfNew = fetch_data(source, exclude = [LAT_LONG_NAME, LAT, LONG], where = reqSites)#We don't display these three vars
                dfNew["Source"] = source.name
                df = pd.concat([df, dfNew])#Append this to the existing df     
        if not df_xl.empty:
            df = pd.concat([df, df_xl[df_xl[SITE_NAM].isin(list(reqSites.values_list("name", flat = True)))]])
        df = df.infer_objects(copy=False).fillna(-1)
    return reqSites


def get_sites_in_place(request: HttpRequest) -> QuerySet[Site]:
    #Returns a BaseManager of Sites dependent on the type (state, county, or individual station) requested,
    #and the name (the string desired).
    place_type = request.GET.get("type")
    place_name = request.GET.get("name")
    match place_type:
        case "State":
            return Site.objects.filter(state = place_name).distinct()
        case "County":
            county_state = place_name.split(", ")
            return Site.objects.filter(county = county_state[0], state = county_state[1]).distinct()
        case "Individual Station":
            site_id = request.GET.get("site_id")
            site_source = request.GET.get("site_source")
            return Site.objects.filter(name = place_name, site_id = site_id, source__name = site_source)
    #If place_type doesn't match anything, return and empty QuerySet
    return Site.objects.none()


def load_layer(request: HttpRequest) -> HttpResponse: 
    reqSites = append_data_if_new(request)
    sites = list(reqSites.values_list("name", flat=True))
    layers = df
    pedon_list = layers[PEDON_NAM].to_list()
    if len(pedon_list) == 0:
        superDict = {"layer_" : []}
        json_stuff = js(superDict)
        return HttpResponse(json_stuff, content_type ="application/json")
    num_samples, num_layers = count_changes(pedon_list)
    print(f'Pedon collection has {num_samples} pedons each having at most {num_layers} layers')

    def prep_data_4_box_js(myList: list) -> list:#sub-function of load_layer
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
    
    superDict = {"site" : sites, "footer_keys" : summary_keys, "footer_values" : summary_values}
    for key in summary_keys:
        superDict[key] = prep_data_4_box_js(layers[key].to_list())
    superDict["data"] = prep_data_4_box_js(np.subtract(layers[BOTTOM].to_list(), layers[TOP].to_list()))
    superDict["layer_"] = np.arange(1, num_layers + 1).tolist()  
    json_stuff = js(superDict)
    return HttpResponse(json_stuff, content_type ="application/json")


def download_layer(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    df.to_csv(response, index=False)
    return response


def spline(request: HttpRequest) -> HttpResponse:
    reqSites = append_data_if_new(request)
    spline_keys = list(Standard.objects.filter(summary = True, canSpline = True).values_list("name", flat = True))
    superDict = {"site" : ["Spline Output Average"], "footer_keys" : spline_keys, "footer_values" : spline_keys}
    def get_averages(var: str) -> list:
        arrays = []
        pedons = Pedon.objects.filter(site__in = reqSites)
        for pedon in pedons:
            pedonCoeffs = ast.literal_eval(pedon.splineCoeffs)#This will return either a dict or a str (if the dict is empty)
            if pedonCoeffs.get(var):
                if type(pedonCoeffs[var]) is dict:
                    arrays.append(np.array(pedonCoeffs[var]["y"]))
        averages = []
        if len(arrays) == 0:
            return averages
        max_length = max(len(arr) for arr in arrays)
        for i in range(max_length):
            column_values = [arr[i] for arr in arrays if i < len(arr)]
            averages.append([np.round(np.mean(column_values), 3)])
        return averages
    for var in spline_keys:
        superDict[var] = get_averages(var)
    num_layers = max(len(superDict[var]) for var in spline_keys)
    for var in spline_keys:
        num_to_add = num_layers - len(superDict[var])
        if num_to_add > 0:
            superDict[var].extend([-1] * num_to_add)
    superDict["data"] = [[10]] * num_layers
    superDict["layer_"] = np.arange(1, num_layers + 1).tolist()
    json_stuff = js(superDict)
    return HttpResponse(json_stuff, content_type ="application/json")


def get_pedons(request: HttpRequest):
    try:
        site = append_data_if_new(request)
        pedons = Pedon.objects.filter(site__in = site).values('name', 'pedon_id')
        synonyms = Synonym.objects.filter(dataset__in = site.first().source.dataset_set.all())
        standards = Standard.objects.filter(name__in=synonyms.values('standard__name'), canSpline=True).values('name')
        return JsonResponse({'pedons': list(pedons), 'standards' : list(standards)})
    except Site.DoesNotExist:
        return JsonResponse({'pedons': [], 'standards' : []})
    
    
def get_spline_line(request: HttpRequest) -> HttpResponse:
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
    default_upper_bound = 101  # Default value for upper bound of x values for prediction
    x_pred = np.arange(default_upper_bound)  # x values to predict (from 0 to default_upper_bound)
    y_pred = np.zeros(default_upper_bound)  # Array to store the predicted y values (initialized to 0)
    denom = np.zeros(default_upper_bound)  # Array to track the number of predictions at each x value
    cs = CubicSpline([0, 1], [0, 1], bc_type = 'natural')  # Initialize a cubic spline object (dummy with [0,1] as initial values)
    
    # Fetch pedons matching the name and pedon_id from the GET request parameters
    pedons = Pedon.objects.filter(name=request.GET.get("name"), pedon_id=request.GET.get("id"))
    #var = Standard.objects.get(request.GET.get("var"))
    var = SOC
    
    # Convert the dataframe to ensure PEDON_ID is of type string for correct indexing later
    dfTemp = df.astype({PEDON_ID: 'str'})
    
    # Loop through all the pedons (soil samples) returned by the filter query
    for pedon in pedons:
        # Parse the spline coefficients and x values for the pedon from the database
        pedonCoeffs = ast.literal_eval(pedon.splineCoeffs)
        cs.x = np.array(ast.literal_eval(pedon.x))  # Set the x values of the spline
        
        # Create a new x_obs array based on the cubic spline x values
        x_obs = np.arange(cs.x.size + 1)  # Generate initial x_obs values
        for i in range(cs.x.size):
            x_obs[i+1] = 2 * cs.x[i] - x_obs[i]  # Update x_obs values using a specific formula
        x_obs = np.delete(x_obs, 1)  # Delete the first element as it's the 1 cm we added
        
        # Set the cubic spline coefficients for the current variable
        cs.c = np.array(pedonCoeffs[var]["c"])  # Assign the coefficients for the spline

        # Get observed y values from the dataframe for the given variable and pedon
        y_obs = np.array(dfTemp.loc[dfTemp[PEDON_NAM] == pedon.name, var])

        # Create a list of x, y pairs for the current variable
        xy = [{"x": X, "y": Y} for X, Y in zip([(x_obs[i] + x_obs[i+1]) / 2 for i in range(len(x_obs) - 1)], y_obs)]
        
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
        
        # Exit the loop after processing the first variable (break after first round)
        break
        
        # Exit the outer loop after processing the first pedon (break after first pedon)
        break

    # Prepare a dictionary with the x and y values for the spline
    superDict = {"x": x_pred.tolist(), "y": y_pred.tolist(), "y0": xy}
    
    # Convert the dictionary into JSON format
    json_stuff = js(superDict)

    # Return the JSON response with content type "application/json"
    return HttpResponse(json_stuff, content_type="application/json")
