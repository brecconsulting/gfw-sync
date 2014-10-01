#!/usr/bin/env python2.7

import datetime



def layers():

    now = datetime.datetime.now()

    #Define layer specific parameters
    #Follow the same schema to add new layers
    #Don't forget to add layer in return list at the end of the function



    can_people = {
        'location': "geojson_url",
        'full_path': "http://data.gfw.opendata.arcgis.com/datasets/5c3ce80d80df4d7f9f6a39a19f15b90d_0.geojson",
        'where_clause': "\"Status\" <> 'CANCELLED'", #make sure to escape quotes (\")
        'transformation': None,
        'fields': {
            'country': ["value", "LBR"],
            'year': ["value", "2014"],
            'type': ["field", "PERMIT_NUM"],
            'name': ["field", "NAME"],
            'company': ["field", "COMPANY"],
            'group_company': ["field", "GROUP_"],
            'group_country': ["field", "NAT_ORIGIN"],
            'province': None,
            'status': ["field", "Status"],
            'area_ha': ["field", "AREA_HA"],
            'source': ["value", "Global Witness 2014"]
        }
    }
  


    #return layer list
    return [can_people]
