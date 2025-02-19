NRCS = {"Gen_lat": "lat", "Gen_long" : "long", "upedonid" : "loc_lvl_0", "rcasiteid" : "loc_lvl_1",}
LATITUDE = {"NRCS" : "Gen_lat", "ISCN" : "lat (dec. deg)"}
LONGITUDE = {"NRCS" : "Gen_long", "ISCN" : "long (dec. deg)"}
#Location Level 0
LOC_LVL_0 = {"NRCS" : "upedonid", "ISCN" : "site_name"}#The name of where specifically the soil comes from. No two soil samples will be from the exact same place.
TOP = {"NRCS" : "TOP", "ISCN" : "layer_top (cm)"}
BOTTOM = {"NRCS" : "BOT", "ISCN" : "layer_bot (cm)"}
LAYER_NAME = {"NRCS" : "samp", "ISCN" : "layer_name"}
WAS_BD_MODELED = {"NRCS" : "BDmeasured", "ISCN" : "bd_method"}
BD_METHOD = {"NRCS" : "BDmethod", "ISCN" : "bd_method"}
BULKDENSITY = {"NRCS" : "Bulkdensity", "ISCN" : "bd_samp (g cm-3)"}
SOC = {"NRCS" : "SOC_pred1", "ISCN" : "soc (g cm-2)"}
SAMPLE_NUM = {"NRCS" : "pedon_no", "ISCN" : "profile_name"}
#Location Level 1
LOC_LVL_1 = {"NRCS" : "rcasiteid", "ISCN" : "state (state_province)"}#A grouping of level 0 locations