import urllib
import zipfile
import os
import re
import shutil
import arcpy

import settings



def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


def download_wdpa():

    sets = settings.get_settings()

    url = "http://wcmc.io/wdpa_current_release"  # pull out
    path = sets["paths"]["scratch_workspace"]

    zip_name = "wdpa_current_release.zip"
    zip_path = os.path.join(path, zip_name)
    path_gdb = os.path.join(path, "wdpa_current_release.gdb")
    temp_folder = os.path.join(path, "temp")


    try:
        shutil.rmtree(path_gdb)
    except:
        pass

    urllib.urlretrieve(url, zip_path)

    unzip(zip_path, temp_folder)

    path_gdb = os.path.join(path, "wdpa_current_release.gdb")

    sub_folders = [x[0] for x in os.walk(temp_folder)]


    for f in sub_folders:
        if re.findall("\W+WDPA\w+\.gdb", f):
            shutil.move(f, path_gdb)
            break

    os.remove(zip_path)
    shutil.rmtree(temp_folder)

    arcpy.env.workspace = path_gdb
    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:
        desc = arcpy.Describe(fc)
        if desc.shapeType == 'Polygon':
            arcpy.Rename_management(fc, 'wdpa_poly', "FeatureClass")
        elif desc.shapeType == 'Point' or desc.shapeType == 'Multipoint':
            arcpy.Rename_management(fc, 'wdpa_point', "FeatureClass")


def get_wdpaid_row(in_feature_class, id, fields):
    sets = settings.get_settings()

    with arcpy.da.SearchCursor(in_feature_class, fields, '"OBJECTID" = %i' % id, sets["spatial_references"]["default_srs"]) as cursor:
        for row in cursor:
            return row


def update_features(in_feature_class, out_feature_class):
    arcpy.MakeFeatureLayer_management(in_feature_class, "in_layer")
    arcpy.MakeFeatureLayer_management(out_feature_class, "out_layer")
    arcpy.AddJoin_management("out_layer", "WDPAID", "in_layer", "WDPAID", "KEEP_COMMON")
    arcpy.SelectLayerByAttribute_management("in_layer", "NEW_SELECTION")
    arcpy.RemoveJoin_management("in_layer", "out_layer")

    fields = ["OID@",
              "WDPAID",
              "WDPA_PID",
              "PA_DEF",
              "NAME",
              "ORIG_NAME",
              "DESIG",
              "DESIG_ENG",
              "DESIG_TYPE",
              "IUCN_CAT",
              "INT_CRIT",
              "MARINE",
              "REP_M_AREA",
              "GIS_M_AREA",
              "REP_AREA",
              "GIS_AREA",
              "NO_TAKE",
              "NO_TK_AREA",
              "STATUS",
              "STATUS_YR",
              "GOV_TYPE",
              "OWN_TYPE",
              "MANG_AUTH",
              "MANG_PLAN",
              "VERIF",
              "METADATAID",
              "SUB_LOC",
              "PARENT_ISO3",
              "ISO3",
              "SHAPE@"]

    sets = settings.get_settings()

    with arcpy.da.UpdateCursor("out_layer", fields, "", sets["spatial_references"]["gdb_srs"]) as cursor:
        for row in cursor:
            row = get_wdpaid_row(in_feature_class, row[0], fields)
            cursor.updateRow(row)


def add_features(in_feature_class, out_feature_class):
    arcpy.MakeFeatureLayer_management(in_feature_class, "in_layer")
    arcpy.MakeFeatureLayer_management(out_feature_class, "out_layer")
    arcpy.AddJoin_management("in_layer", "WDPAID", "out_layer", "WDPAID", "KEEP_ALL")
    arcpy.SelectLayerByAttribute_management("in_layer", "NEW_SELECTION", "out_layer.WDPAID IS null")
    arcpy.RemoveJoin_management("in_layer", "out_layer")
    arcpy.Append_management("in_layer", out_feature_class, "TEST")


def remove_features(in_feature_class, out_feature_class):
    arcpy.MakeFeatureLayer_management(in_feature_class, "in_layer")
    arcpy.MakeFeatureLayer_management(out_feature_class, "out_layer")
    arcpy.AddJoin_management("out_layer", "WDPAID", "in_layer", "WDPAID", "KEEP_ALL")
    arcpy.SelectLayerByAttribute_management("out_layer", "NEW_SELECTION", "in_layer.WDPAID IS null")
    arcpy.RemoveJoin_management("out_layer", "in_layer")
    arcpy.DeleteFeatures_management("out_layer")


download_wdpa()
