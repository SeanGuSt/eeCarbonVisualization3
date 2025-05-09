from django.db.models import Model, CharField, BooleanField, ForeignKey, ManyToManyField, URLField, TextField, FloatField, JSONField, CASCADE
from django.db import connections
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
# from django.contrib.gis.db import models as gis_models
from django.apps import apps
import requests
from io import StringIO
import numpy as np
import pyodbc
from.constant import PEDON_NAM, PEDON_ID, SITE_NAM, SITE_ID, LAT_LONG_NAME
from.static.scripts.python.other import intersection, unique
from eeCarbonVisualization3.settings import BASE_DIR
import pandas as pd
MAX_DELIM_LENGTH = 1
MAX_STR_LENGTH = 255

class Source(Model):
    name = CharField(max_length=MAX_STR_LENGTH, unique=True)
    type = CharField(max_length=MAX_STR_LENGTH, default = "SQL")
    # please_visit = URLField(max_length=MAX_STR_LENGTH, default = "")
    def __str__(self):
        return self.name
    

class Standard(Model):
    name = CharField(max_length=MAX_STR_LENGTH, unique=True)#This is the unifying name for the variables
    summary = BooleanField(default = False)#Should this variable be shown on the initial display, or only when downloading the data?
    isSoil = BooleanField(default = False)
    isTime = BooleanField(default = False)
    canSpline = BooleanField(default = False)
    naltID = URLField(max_length=MAX_STR_LENGTH, default = "")
    def __str__(self):
        return self.name
    
class Dataset(Model):
    #This model's purpose is to account for the possibility that a source may store all its data in multiple files
    name = CharField(max_length=MAX_STR_LENGTH, unique=True)
    hasSoil = BooleanField(default = False)#Soil data
    hasTime = BooleanField(default = False)#Temporal data
    source = ForeignKey(Source, on_delete = CASCADE)#Source of Dataset
    merge_on = ForeignKey(Standard, on_delete = CASCADE)
    file = URLField(max_length=MAX_STR_LENGTH, default = "")#Set as empty if this is a Database
    delimiter = CharField(max_length=MAX_DELIM_LENGTH, default = ",")#Set as empty if this is a Database
    def __str__(self):
        return self.name
    
class Synonym(Model):
    name = CharField(max_length=MAX_STR_LENGTH, default = "")
    dataset = ManyToManyField(Dataset)#Just in case 2 places actually do use the same variable to mean the same thing
    standard = ForeignKey(Standard, on_delete=CASCADE)
    class Meta:
        order_with_respect_to = "name"
        unique_together = ["name", "standard"]
    def __str__(self):
        return self.name
    
class Site(Model):
    name = CharField(default = "", max_length=MAX_STR_LENGTH)
    site_id = CharField(default = "", max_length=MAX_STR_LENGTH)
    # location = gis_models.PointField() 
    latitude = FloatField(default = 0)
    longitude = FloatField(default = 0)
    county = CharField(default = "", max_length=MAX_STR_LENGTH)
    county_id = CharField(default = "", max_length=MAX_STR_LENGTH)
    state = CharField(default = "", max_length=MAX_STR_LENGTH)
    state_id = CharField(default = "", max_length=MAX_STR_LENGTH)
    source = ForeignKey(Source, on_delete=CASCADE, default = 1)
    class Meta:
        order_with_respect_to = "name"
        unique_together = ["name", "site_id", "source"]
    def __str__(self):
        return self.name
    
class Pedon(Model):
    name = CharField(default = "", max_length=MAX_STR_LENGTH)#Some sources may have sites with the same name.
    pedon_id = CharField(default = "", max_length=MAX_STR_LENGTH)
    x = JSONField(default = list)
    splineCoeffs = JSONField(default = dict)
    site = ForeignKey(Site, on_delete=CASCADE, default = 1)#All Pedons come from a Site
    interpolation_warning = BooleanField(default = False)
    interpolation_type = TextField(default = "")
    class Meta:
        order_with_respect_to = "name"
        unique_together = ["name", "pedon_id", "site"]
    def __str__(self):
        return self.name
#End goal, deduce which of the splinable standards are available from the given pedons.    
#pedon.site.source
    

# Function to fetch data from a source and process it into a pandas DataFrame
def fetch_data(source: Source, include: list = [], exclude: list = [], need: list = [], where: QuerySet = Site.objects.none()) -> pd.DataFrame:
    """
    Fetches data from the specified source and processes it into a DataFrame. It validates the input and handles 
    different types of data sources (CSV, Excel, or databases). Data can be filtered using include, exclude, 
    and need lists.

    Args:
        source (Source): The source from which the data is being fetched.
        include (list): List of columns to include in the data.
        exclude (list): List of columns to exclude from the data.
        need (list): List of required columns that must be present in the dataset.
        where (QuerySet): Additional filtering conditions to apply on the data.

    Returns:
        pd.DataFrame: The processed data in a DataFrame format.
    """
    # Ensure that the 'need' list is a sublist of 'include' (if 'include' isn't empty) and that 'include' and 'exclude' are disjoint
    if intersection(need, include) != need and include != []:
        raise Exception("need must be a sublist of include.")
    if intersection(include, exclude):
        raise Exception("include and exclude must be disjoint.")

    datasets = Dataset.objects.filter(source=source)  # Filter datasets by the source
    df = pd.DataFrame(columns = need)  # Initialize an empty DataFrame
    suffix = "_x"  # Suffix for columns to distinguish duplicates during merges
    
    # Loop through each dataset related to the source
    for dataset in datasets:
        synonyms = Synonym.objects.filter(dataset=dataset)  # Get synonyms related to this dataset
        merge_on = dataset.merge_on.name  # Select the standard variable for merging
        print(f"merge on for {dataset.name}: {merge_on}")
        synList = unique(synonyms.values_list("name", flat=True))  # Create a list of unique synonyms
        # Ensure the 'need' columns are present in the synonyms list
        if not have_all_needed(need, synonyms, synList):
            continue  # Skip this dataset if 'need' columns are not available
        # Apply 'include' filter on the synonyms list if provided
        synList = only_include(include, synonyms, synList)
        # Remove synonyms from 'exclude' list from the synonyms list
        synList = remove_exclude(exclude, synonyms, synList)
        print(f"List of synonyms: {synList}")
        # Skip datasets with insufficient columns
        if (len(synList) < 2 and not df.empty) or len(synList) == 0:
            continue
        # If the dataset uses a single delimiter, fetch data from a CSV or Excel file
        if len(dataset.delimiter) == 1:
            dfNew = fetch_data_by_download(dataset, synList)
        else:
            # If the dataset points to a database, fetch data from the database
            dfNew = fetch_data_using_SQL(dataset, df, synonyms, synList, where, merge_on)

        dfNew = rename_columns_Synonym_to_Standard(dfNew, synonyms, synList)    
        print(f"df has columns {df.columns} while dfNew has columns {dfNew.columns}")
        # Merge the new DataFrame with the main DataFrame
        if df.empty:
            df = dfNew
            #if source.name == "RaCA": df = df.rename(columns = {LAT_LONG_NAME : SITE_NAM})#Comment out this line when refilling RaCA
        else:
            df[merge_on] = df[merge_on].astype(str)
            print(df[merge_on])
            dfNew[merge_on] = dfNew[merge_on].astype(str)
            print(dfNew[merge_on])
            df = df.merge(dfNew, on=merge_on, suffixes=[suffix, None])
        #print(f'And now, df is {df}')
    # Call the function to combine like columns before returning the final DataFrame
    return combine_like_columns(df, suffix)

def have_all_needed(need: list, synonyms: QuerySet[Synonym], synList: list) -> bool:
    return len(intersection(synList, list(synonyms.filter(standard__name__in=need).values_list("name", flat=True)))) == len(need)


def only_include(include: list, synonyms: QuerySet[Synonym], synList: list) -> list:
    if include:
        return intersection(synList, list(synonyms.filter(standard__name__in=include).values_list("name", flat=True)))
    return synList


def remove_exclude(exclude: list, synonyms: QuerySet[Synonym], synList: list) -> list:
    for syn in list(synonyms.filter(standard__name__in=exclude).values_list("name", flat=True)):
        if syn in synList:
            synList.remove(syn)
    return synList


def fetch_data_by_download(dataset: Dataset, synList: list) -> pd.DataFrame:
    response = requests.get(dataset.file)  # Make an HTTP request to fetch the file
    if response.status_code == 200:
        file_received = StringIO(response.text)  # Convert the response text to a StringIO object
        # Read the CSV file into a DataFrame, using only the necessary columns
        dfNew = pd.read_csv(file_received, delimiter=dataset.delimiter, low_memory=False, usecols=synList, on_bad_lines='warn').fillna("")
    else:
        print("Warning! File not obtained")  # Handle errors if the file isn't obtained
        dfNew = pd.DataFrame(columns = synList)
    return dfNew

    
def fetch_data_using_SQL(dataset: Dataset, df: pd.DataFrame, synonyms: QuerySet[Synonym], synList: list, where: QuerySet, merge_on: str) -> pd.DataFrame:
    def fetch_data_using_SQL_cursor(cursor):
        quoted_columns = ['"{}"'.format(col) for col in synList]

        # Create the query string
        query = "SELECT " + ", ".join(quoted_columns) + " FROM " + db_and_table[1]
        print(f"{dataset.source.name}, {quoted_columns}")
        # Apply 'where' filter if provided
        if where:
            #print(f"The synonyms are {synonyms}")
            #print(f"And their standards are {[syn.standard.name for syn in synonyms]}")
            if df.empty:
                samp_name = Synonym.objects.get(dataset=dataset, standard__name=SITE_ID if SITE_ID in list(synonyms.values_list("standard__name", flat=True)) else SITE_NAM).name
                samp_list = list(where.filter(source=dataset.source).values_list("name", flat=True))
            else:
                samp_name = Synonym.objects.get(dataset=dataset, standard__name=merge_on).name
                samp_list = [str(x) if x is not str else "'" + x + "'" for x in unique(df[merge_on])]
            #print(f"They'll merge using the variable {samp_name}")
            #print(f"While looking for {samp_list}")
            query = query + " WHERE " + samp_name + " IN ('" + "', '".join(samp_list) + "')"
        cursor.execute(query)  # Execute the database query
        # Fetch results from the query and load them into a DataFrame
        x = cursor.fetchall()
        dfNew = pd.DataFrame(np.asarray(x), columns=synList)
        return dfNew
    
    db_and_table = dataset.file.split(" ,TABLE, ")  # Split to get the database and table name
    if dataset.source.type == "ACCESS":
        print( r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_and_table[0] + ';')
        conn = pyodbc.connect(
                 r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(BASE_DIR) + '/' + db_and_table[0] + ';'
                )
        cur = conn.cursor()
        dfNew = fetch_data_using_SQL_cursor(cur)
        cur.close()
        conn.close()
    else:
        with connections[db_and_table[0]].cursor() as cursor:
            dfNew = fetch_data_using_SQL_cursor(cursor)
    print(dfNew.shape)
    return dfNew
    
def rename_columns_Synonym_to_Standard(dfNew: pd.DataFrame, synonyms: QuerySet[Synonym], synList: list) -> pd.DataFrame:
    # Rename the columns based on the standard name for each synonym
    new_column_names = {syn: list(synonyms.filter(name=syn).values_list("standard__name", flat=True))[0] for syn in synList}
    for syn in synList:
        stanList = list(synonyms.filter(name=syn).values_list("standard__name", flat=True))
        if len(stanList) > 1:
            for stan in stanList:
                if stan not in new_column_names.values():
                    dfNew[stan] = dfNew[syn]

    dfNew = dfNew.rename(columns=new_column_names)
    return dfNew

# Function to combine like columns (those with similar names but different suffixes)
def combine_like_columns(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    for column in set(df.columns):  # Iterate through each unique column name
        column_count = df.columns.to_list().count(column)  # Count occurrences of the column
        if column + suffix in df.columns:  # If a column with the suffix exists, rename it
            df = df.rename(columns={column + suffix: column})
            column_count = df.columns.to_list().count(column)
        if column_count > 1:  # If there are now multiple columns with the same name, combine them
            x = df[column].dropna(axis=1, how='all').bfill(axis=1).iloc[:, 0]  # Backfill missing values and get the first non-NaN value
            df = df.drop(columns=[column])  # Drop the original column
            df[column] = x  # Assign the combined values back to the column
    return df
