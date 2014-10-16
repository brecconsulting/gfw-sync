#!/usr/bin/env python2.7

import datetime



def layers():

    now = datetime.datetime.now()

    #Define layer specific parameters
    #Follow the same schema to add new layers
    #Don't forget to add layer in return list at the end of the function



    Canada_Land_Rights = {
        'location': "server",
        'full_path': "D:\\GIS Data\\CAN\\Canada Land Rights\\Canada_Land_Rights.shp",
        'where_clause': "",
        'transformation': "NAD_1983_To_WGS_1984_33",
        'fields': {
            'Name': ["field", "NAME"],
            'Country': ["field", "Country"],
            'Area_HA': ["field", "Area_Ha"],
            'National_Legal_Term': ["field", "Nat_Leg_Te"],
            'Legal_Recognition': ["field", "Leg_Rec"]
            }
        }

    NZL_Land_Rights = {
        'location': "server",
        'full_path': "D:\\GIS Data\\NZL\\New Zealand Land Rights\\NZL_Land_Rights.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'Name': ["field", "Name"],
            'Country': ["field", "Country"],
            'Area_HA': ["field", "Area_ha"],
            'National_Legal_Term': ["field", "National_L"],
            'Legal_Recognition': ["field", "Legal_Reco"],
            'Category': ["value", "Land Rights"]
            }
        }

    Brazil_Final = {
        'location': "server",
        'full_path': "D:\\GIS Data\\BRA\\Brazil Land Rights\\Brazil_Final\\Brazil_Final.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'Name': ["field", "Name"],
            'Country': ["field", "Country"],
            'Area_HA': ["field", "Area_ha"],
            'National_Legal_Term': ["field", "Nat_Leg_Te"],
            'Legal_Recognition': ["field", "Leg_Rec"],
            'Category': ["value", "Land Rights"]
            }
        }
  
    Comarcas_Final = {
        'location': "server",
        'full_path': "D:\\GIS Data\\PAN\\Panama Land Rights\\Panama_Land_Rights\\Comarcas_Final.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'Name': ["field", "Name"],
            'Country': ["field", "Country"],
            'Area_HA': ["field", "Area_Ha"],
            'National_Legal_Term': ["field", "Nat_Leg_Te"],
            'Legal_Recognition': ["field", "Leg_Rec"],
            'Category': ["value", "Land Rights"]
            }
        }

    Australia_Inalienable_Land_Rights = {
        'location': "server",
        'full_path': "D:\\GIS Data\\AUS\\Land Rights\\Australia_Inalienable_Land_Rights\\Australia_Inalienable_Land_Rights.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'Name': ["field", "Name"],
            'Country': ["field", "Country"],
            'Area_HA': ["field", "Area_Ofcl"],
            'National_Legal_Term': ["field", "Category"],
            'Legal_Recognition': ["field", "Reco"],
            'Category': ["value", "Land Rights"]
            }
        }
  
      #return layer list
    return [Canada_Land_Rights, NZL_Land_Rights, Brazil_Final, Comarcas_Final, Australia_Inalienable_Land_Rights]
