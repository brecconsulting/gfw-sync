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


def download_wdpa(url, wdpa, path):

	sets = settings.get_settings()

	zip_name = "%s.zip" % wdpa
	zip_path = os.path.join(path, zip_name)
	gdb = os.path.join(path, "%s.gdb")
	if arcpy.Exists(gdb):
		arcpy.Delete_management(gdb)
 
	urllib.urlretrieve(url, zip_path)

	unzip(zip_path, path)
	os.remove(zip_path)
	
	return path
	

def replace_wdpa_data(src_gdb, dst_gdb, wdpa_fc, sde_gdb):
	
    arcpy.env.workspace = src_gdb
    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:
		print fc
		desc = arcpy.Describe(fc)
		if desc.shapeType == 'Polygon':
			##delete all features
			
			src_fc = os.path.join(src_gdb, fc)
			dst_fc = os.path.join(dst_gdb, wdpa_fc)

			arcpy.DeleteFeatures_management(dst_fc)
			arcpy.Compress_management(sde_gdb)

			
			##load new data
			arcpy.Append_management (src_fc, dst_fc, "NO_TEST")
			



sets = settings.get_settings()			
			
url = "http://wcmc.io/wdpa_current_release"
wdpa = "wdpa_current_release"
path = sets["paths"]["scratch_workspace"]			
			
print "download"
src_gdb = os.path.join(path,"%s.gdb" % wdpa) #download_wdpa(url, wdpa, path)
dst_gdb = r"D:\scripts\connections\test (gfw).sde\conservation"
sde_gdb = r"D:\scripts\connections\test (sde).sde"

wdpa_fc = "wdpa_protected_areas"

print "upload data"
replace_wdpa_data(src_gdb, dst_gdb, wdpa_fc, sde_gdb)
			
			
			
########## old / kick out
			
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



