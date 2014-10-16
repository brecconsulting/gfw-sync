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
            'name': ["field", "NAME"],
            'country': ["value", "CAN"],
            'area_ha': ["field", "Area_Ha"],
            'national_legal_term': ["field", "Nat_Leg_Te"],
            'legal_recognition': ["field", "Leg_Rec"]
            }
        }

    NZL_Land_Rights = {
        'location': "server",
        'full_path': "D:\\GIS Data\\NZL\\New Zealand Land Rights\\NZL_Land_Rights.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'name': ["field", "Name"],
            'country': ["value", "NZL"],
            'area_ha': ["field", "Area_ha"],
            'national_legal_term': ["field", "National_L"],
            'legal_recognition': ["field", "Legal_Reco"],
            'category': ["value", "Land Rights"]
            }
        }

    Brazil_Final = {
        'location': "server",
        'full_path': "D:\\GIS Data\\BRA\\Brazil Land Rights\\Brazil_Final\\Brazil_Final.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'name': ["field", "Name"],
            'country': ["value", "BRA"],
            'area_ha': ["field", "Area_ha"],
            'national_legal_term': ["field", "Nat_Leg_Te"],
            'legal_recognition': ["field", "Leg_Rec"],
            'category': ["value", "Land Rights"]
            }
        }
  
    Comarcas_Final = {
        'location': "server",
        'full_path': "D:\\GIS Data\\PAN\\Panama Land Rights\\Panama_Land_Rights\\Comarcas_Final.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'name': ["field", "Name"],
            'country': ["value", "PAN"],
            'area_ha': ["field", "Area_Ha"],
            'national_legal_term': ["field", "Nat_Leg_Te"],
            'legal_recognition': ["field", "Leg_Rec"],
            'category': ["value", "Land Rights"]
            }
        }

    Australia_Inalienable_Land_Rights = {
        'location': "server",
        'full_path': "D:\\GIS Data\\AUS\\Land Rights\\Australia_Inalienable_Land_Rights\\Australia_Inalienable_Land_Rights.shp",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'name': ["field", "Name"],
            'country': ["value", "AUS"],
            'area_ha': ["field", "Area_Ofcl"],
            'national_legal_term': ["field", "Category"],
            'legal_recognition': ["field", "Reco"],
            'category': ["value", "Land Rights"]
            }
        }
  
      #return layer list
    return [Canada_Land_Rights, NZL_Land_Rights, Brazil_Final, Comarcas_Final, Australia_Inalienable_Land_Rights]
