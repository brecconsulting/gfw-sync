# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# merge_layers.py
# Created on: 2014-05-21 09:48:06.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import archiver
import glob
import sys
import traceback
import string
import urllib

from config import settings

arcpy.ImportToolbox(settings.get_geojson_toolbox())


def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def create_field_map(input_name, layer, field):
    fm = arcpy.FieldMap()
    fm.addInputField(input_name, layer['fields'][field][1])
    output_field = fm.outputField
    output_field.name = field
    fm.outputField = output_field

    return fm


def empty_strings2null(fclass):
    desc = arcpy.Describe(fclass)
    if desc.dataType == 'FeatureClass':
        string_fields = [f.name for f in arcpy.ListFields(fclass, None, 'String')]
        for string_field in string_fields:
            arcpy.MakeFeatureLayer_management(fclass,
                                              "update_layer",
                                              '"%s" = \'\'' % string_field,
                                              "",
                                              "")
            arcpy.CalculateField_management("update_layer", string_field, "None", "PYTHON", "")

def get_bucket_name(s3_path):
    if len(string.split(s3_path,'\\'))>1:
        return string.split(s3_path,'\\')[0]
    elif len(string.split(s3_path,'/'))>1:
        return string.split(s3_path,'/')[0]
    else:
        return None


def get_json_name(json_url):

    url_list = json_url.split("/")
    json = url_list[len(url_list)-1].split("?")
    json_name = json[0]
    return json_name


def merge(mlayer):
    # import layer file given in system argument
    global input_fc

    try:
        import_layers = import_module('layers.' + mlayer)
    except ImportError:
        return "Warning: Layer %s is not defined" % mlayer

    # get layer settings
    target_ws = settings.get_target_gdb()
    target_fc_name = mlayer
    scratch_folder = settings.get_scratch_folder()
    scratch_gdb =  settings.get_scratch_gdb()
    s3_bucket = settings.get_download_bucket()
    bucket_drives = settings.get_bucket_drive()

    layers = import_layers.layers()

    #define name for target feature class and target feature layer
    target_fc = os.path.join(target_ws, target_fc_name)
    target_layer = '%s_layer' % target_fc_name

    # set environment parameters
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 Web Mercator (auxiliary sphere)")

    # Deletes all features in target feature class
    arcpy.DeleteFeatures_management(target_fc)

    # Compact target file-geodatabase to avoid running out of ObjectIDs
    arcpy.Compact_management(target_ws)

    #Add features, one layer at a time
    for layer in layers:

        #Set output coordinate system to Web Mercator
        #All ESRI web services are published using this projection

        print "Adding " + os.path.basename(layer['full_path'])

        # define transformation
        if layer['transformation']:
            arcpy.env.geographicTransformations = layer['transformation']

        # create feature layer from feature class

        if layer['location'].lower() == 'server':
            input_fc = layer['full_path']
        elif layer['location'].lower() == 's3':

            s3_bucket_drive = bucket_drives[get_bucket_name(layer['full_path'])]
            s3_path = layer['full_path'][len(get_bucket_name(layer['full_path'])):]

            input_fc = os.path.join(s3_bucket_drive, s3_path)

        elif layer['location'].lower() == 'geojson_url':

            json_name = get_json_name(layer['full_path'])
            json = os.path.join(scratch_folder, json_name)
            #urllib.urlretrieve(layer['full_path'], os.path.join(scratch_folder, json_name))
            input_fc = os.path.join(scratch_gdb, "geojson_" + json_name[:-8])
            arcpy.ImportGeoJSONFromURL_geojsonconversion(layer['full_path'], input_fc)
            #geojson_to_features(json,input_fc)
            #arcpy.JSONToFeatures_conversion(json, input_fc)



        input_layer = os.path.basename('%s_layer') % input_fc

        arcpy.MakeFeatureLayer_management(input_fc,
                                          input_layer,
                                          layer['where_clause'],
                                          "",
                                          "")

        # map fields
        fms = arcpy.FieldMappings()

        for field in layer['fields']:
            if layer['fields'][field]:
                if layer['fields'][field][0] == 'field':
                    fms.addFieldMap(create_field_map(input_layer, layer, field))

        # append layer to target feature class
        arcpy.Append_management(input_layer,
                                target_fc,
                                "NO_TEST",
                                fms,
                                "")

        # Update field values, for un-mapped fields

        arcpy.MakeFeatureLayer_management(target_fc,
                                          target_layer,
                                          "country IS NULL OR country = '%s'" % layer['fields']['country'][1],
                                          "",
                                          "")
        for field in layer['fields']:
            if layer['fields'][field]:

                if layer['fields'][field][0] == 'value':
                    arcpy.CalculateField_management(target_layer, field, "'%s'" % layer['fields'][field][1], "PYTHON", "")

                elif layer['fields'][field][0] == 'expression':
                    arcpy.CalculateField_management(target_layer, field, "%s" % layer['fields'][field][1], "PYTHON", "")

        #convert empty strings ('') to NULL
        empty_strings2null(input_fc)

        # reset transformation
        arcpy.env.geographicTransformations = ""

        #except:
        #   print "Failed to add " + layer['input_fc_name']
        #  traceback.print_exc()

    #Set Output coordinate System to WGS 1984 for S3 Archive
    #Vizzuality will download from here and needs the date in Lat/Lon

    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")

    # Export FeatureClass to Shapefile
    arcpy.FeatureClassToShapefile_conversion([target_fc], scratch_folder)

    # zip shapefile and push to Amazon S3 using archiver.py script
    target_shp = os.path.join(scratch_folder, "%s.shp" % target_fc_name)
    target_zip = os.path.join(scratch_folder, "%s.zip" % target_fc_name)
    #s3_zip = os.path.join("data", "%s.zip" % target_fc_name)
    s3_zip = "%s.zip" % target_fc_name

    archiver.main(target_shp, target_zip, s3_zip, s3_bucket)

    # clean up, delete shapefiles and zipfile
    targets_rm = os.path.join(scratch_folder, "%s.*" % target_fc_name)
    r = glob.glob(targets_rm)
    for i in r:
        os.remove(i)

