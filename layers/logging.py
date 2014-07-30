#!/usr/bin/env python2.7

import datetime

def target():
    target_ws = "D:\\GIS Data\\GFW\\GFW_data_wm.gdb"
    target_fc_name = "logging"
    scratch_folder = "D:\\GIS Data\\GFW\\temp"
    s3_bucket = "gfw2_download"

    return [target_ws, target_fc_name, scratch_folder, s3_bucket]

def layers():

    now = datetime.datetime.now()

    #Define layer specific parameters
    #Follow the same schema to add new layers
    #Don't forget to add layer in return list at the end of the function

    cmr_fmu = {
        'input_ws': "D:\\GIS Data\\CMR\\CMR_data_wm.gdb",
        'input_ds': "",
        'input_fc_name': "CMR_ufa",
        'where_clause': "",
        'transformation': None,
        'public_url': 'http://candan.org/download',
        'create_zip': yes,
        'fields': {
            'country': ["value", "CMR"],
            'year': ["value", now.year],
            'type': ["value", "FMU"],
            'name': ["field", "NAME"],
            'company': ["field", "ATTRIBUTAI"],
            'group_company': ["field", "GROUPE_PAR"],
            'group_country': None,
            'province': ["field", "PROVINCE"],
            'status': ["field", "STATUS"],
            'area_ha': ["field", "SUP_SIG"],
            'source': ["value", "MINFOF"],
            'shape_length': ["field", "Shape_Length"],
            'shape_area': ["field", "Shape_Area"]
        }
    }

    cmr_fc = {
        'input_ws': "D:\\GIS Data\\CMR\\CMR_data_wm.gdb",
        'input_ds': "",
        'input_fc_name': "CMR_FC",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'country': ["value", "CMR"],
            'year': ["value", now.year],
            'type': ["value", "Council Forest"],
            'name': ["field", "TOPONYME"],
            'company': None,
            'group_company': None,
            'group_country': None,
            'province': None,
            'status': ["field", "STATUT"],
            'area_ha': ["field", "SUP_SIG"],
            'source': ["value", "MINFOF"],
            'shape_length': ["field", "Shape_Length"],
            'shape_area': ["field", "Shape_Area"]
        }
    }

    gab_cfad = {
        'input_ws': "D:\\GIS Data\\GAB\\GAB_data_wm.gdb",
        'input_ds': "amenagement_forestier",
        'input_fc_name': "gab_CFAD",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "GAB"],
            'year': ["value", now.year],
            'type': ["value", "CFAD"],
            'name': ["field", "nom_ste_s"],
            'company': ["field", "nom_ste"],
            'group_company': ["field", "grp_ste"],
            'group_country': ["field", "orig_capit"],
            'province': None,
            'status': None,
            'area_ha': ["field", "sup_sig"],
            'source': ["value", "MINEF"],
            'shape_length': ["field", "Shape_Length"],
            'shape_area': ["field", "Shape_Area"]
        }
    }

    gab_cpaet= {
        'input_ws': "D:\\GIS Data\\GAB\\GAB_data_wm.gdb",
        'input_ds': "amenagement_forestier",
        'input_fc_name': "gab_CPAET",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "GAB"],
            'year': ["value", now.year],
            'type': ["value", "CPAET"],
            'name': ["field", "nom_ste_s"],
            'company': ["field", "nom_ste"],
            'group_company': ["field", "grp_ste"],
            'group_country': ["field", "orig_capit"],
            'province': None,
            'status': None,
            'area_ha': ["field", "sup_sig"],
            'source': ["value", "MINEF"],
            'shape_length': ["field", "Shape_Length"],
            'shape_area': ["field", "Shape_Area"]
        }
    }



    #return layer list
    return [cmr_fmu, cmr_fc, gab_cfad, gab_cpaet]
