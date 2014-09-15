#!/usr/bin/env python2.7

import datetime



def layers():

    now = datetime.datetime.now()

    #Define layer specific parameters
    #Follow the same schema to add new layers
    #Don't forget to add layer in return list at the end of the function



    LBR_Logging = {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/5c3ce80d80df4d7f9f6a39a19f15b90d_0.geojson",
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
  
    canada_forest_tenures_2013_final = {
        'location': "server",
        'full_path': "C:\\Users\\Thomas.Maschler\\Documents\\Canada_forest_tenures_2013\\canada_forest_tenures_2013_final.shp",
        'where_clause': None, #make sure to escape quotes (\")
        'transformation': "NAD_1927_To_WGS_1984_33",
        'fields': {
            'country': ["value", "CAN"],
            'year': ["value", "2014"],
            'type': ["field", "TYPE"],
            'name': ["field", "NAME"],
            'company': ["field", "COMPANY"],
            'group_company': None,
            'group_country': None,
            'province': ["field", "PROVINCE"],
            'status': None,
            'area_ha': None,
            'source': ["value", "Global Forest Watch Canada"]
            }
        }
  
    cmr_fmu = {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/832f104b888c40c88491ce405d1cd896_7.geojson",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'country': ["value", "CMR"],
            'year': ["value", now.year],
            'type': ["value", "FMU"],
            'name': ["field", "NAME"],
            'company': ["field", "ATTRIBUTAI"],
            'group_company': ["field", "GROUPE_PAR"],
            'group_country': None,
            'province': None,
            'status': ["field", "STATUS"],
            'area_ha': ["field", "SUP_SIG"],
            'source': ["value", "MINFOF 2013"],
            }
        }

    cmr_fc = {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/416a39b7eb344abea60fab4b79a03e51_9.geojson",
        'where_clause': "",
        'transformation': None,
        'fields': {
            'country': ["value", "CMR"],
            'year': ["value", now.year],
            'type': ["value", "Council Forest"],
            'name': ["field", "NAME"],
            'company': None,
            'group_company': None,
            'group_country': None,
            'province': None,
            'status': ["field", "CLASSE"],
            'area_ha': ["field", "SUP_SIG"],
            'source': ["value", "MINFOF 2013"],
            }
        }

    gab_cfad = {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/bc4b1dcc97a44c849de947365087dc64_14.geojson",
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
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/d9caac62192249c99d0dfa836cdb0664_15.geojson",
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

    CAR_Logging= {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/d3587de764f941d89484507b0595e872_7.geojson",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "CAF"],
            'year': ["value", now.year],
            'type': ["value", "Logging Concession"],
            'name': ["field", "Permit_number"],
            'company': ["field", "PEA_NOM"],
            'group_company': None,
            'group_country': ["field", "orig_cap_e"],
            'province': None,
            'status': ["field", "Situation_"],
            'area_ha': ["field", "Surface_Ha"],
            'source': ["value", "MEFCP 2013"],
        }
    }

    DRC_FC= {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/2d56b275452f4eef94088dee3451153e_3.geojson",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "DRC"],
            'year': ["value", now.year],
            'type': ["value", "Logging Concession"],
            'name': ["field", "num_ga"],
            'company': ["field", "nom_ste_a"],
            'group_company': None,
            'group_country': ["field", "orig_cap"],
            'province': None,
            'status': ["field", "statut_tf"],
            'area_ha': ["field", "sup_sig"],
            'source': ["value", "MECAT 2013"],
        }
    }

    GNQ_NF= {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/dc2f57573ae14a6f934872785fecc1b2_5.geojson",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "GNQ"],
            'year': ["value", now.year],
            'type': ["value", "National Forest"],
            'name': ["field", "Localizaci"],
            'company': ["field", "Empr_explt"],
            'group_company': ["field", "Empresa"],
            'group_country': ["field", "Procd_empr"],
            'province': None,
            'status': ["field", "Estado"],
            'area_ha': ["field", "sup_sig_ha"],
            'source': ["value", "MAF 2013"],
        }
    }

    COG_LC= {
        'location': "geojson_url",
        'full_path': "http://globalforestwatch.gfw.opendata.arcgis.com/datasets/f55797d780444c64a7121fe1f8296206_5.geojson",
        'where_clause': "",
        'transformation': "",
        'fields': {
            'country': ["value", "COG"],
            'year': ["value", now.year],
            'type': ["value", "Logging Concessions"],
            'name': ["field", "Nom_Code_C"],
            'company': ["field", "Ste_att_en"],
            'group_company': None,
            'group_country': ["field", "Origine_ca"],
            'province': None,
            'status': ["field", "SIT_ENG"],
            'area_ha': ["field", "Hectares"],
            'source': ["value", "MEFDD 2013"],
        }
    }
    #return layer list
    return [cmr_fmu, cmr_fc, gab_cfad, gab_cpaet, LBR_Logging, canada_forest_tenures_2013_final, DRC_FC, GNQ_NF, COG_LC]
