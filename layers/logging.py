#!/usr/bin/env python2.7

import datetime



def layers():

    now = datetime.datetime.now()

    #Define layer specific parameters
    #Follow the same schema to add new layers
    #Don't forget to add layer in return list at the end of the function


    LBR_Logging = {
        'location': "S3",
        'full_path': "gfw2-data/forestuse/logging/lbr/LBR_Logging.shp",
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

    cmr_fmu = {
        'location': "Server",
        'full_path': "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\CMR\\CMR_data.gdb\\Forest_management\\CMR_ufa_2013",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'country': ["value", "CMR"],
            'year': ["value", now.year],
            'type': ["value", "FMU"],
            'name': ["field", "TOPONYME"],
            'company': ["field", "ATTRIBUTAI"],
            'group_company': ["field", "GROUPE_PAR"],
            'group_country': None,
            'province': ["field", "PROVINCE"],
            'status': ["field", "STATUT"],
            'area_ha': ["field", "SUP_SIG"],
            'source': ["value", "MINFOF 2013"],
        }
    }

    cmr_fc = {
        'location': "Server",
        'full_path': "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\CMR\\CMR_data.gdb\\Forest_management\\CMR_FC_2013",
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
            'source': ["value", "MINFOF 2013"],
        }
    }

    gab_cfad = {
        'location': "Server",
        'full_path': "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\GAB\\GAB_data.gdb\\amenagement_forestier\\gab_CFAD",
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
        }
    }

    gab_cpaet= {
        'location': "Server",
        'full_path': "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\GAB\\GAB_data.gdb\\amenagement_forestier\\gab_CPAET",
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
        }
    }



    #return layer list
    return [cmr_fmu, cmr_fc, gab_cfad, gab_cpaet, LBR_Logging]
