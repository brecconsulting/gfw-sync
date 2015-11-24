''' author: Sam Gibbes
Date: 11/5/15
 purpose: Start with a file of all terra i point, this script will append new terra i updates
 raster math to compare
'''
import datetime, time
import arcpy
from arcpy.sa import *
import datetime
import urllib
import os
start = datetime.datetime.now()
# set environments
arcpy.env.overwriteOutput = "TRUE"
arcpy.CheckOutExtension("Spatial")
maindir = r'D:\_sam\TerraI\testing_4'
arcpy.env.workspace = maindir
scratch = os.path.join(maindir,'scratch.gdb')
split_dir = os.path.join(maindir,"split.gdb")
split_dir_int = os.path.join(maindir,"split_int.gdb")
old_raster = os.path.join(maindir,'latin_decrease_current_proj.tif')
base_points = os.path.join(maindir,'latin_decrease_current_111715.shp')
arcpy.env.scratchWorkspace = scratch

# print "downloading latest file"
latest_raster = os.path.join(maindir,'latest_file.tif')
terrai_file = urllib.urlretrieve("http://www.terra-i.org/data/current/raster/latin_decrease_current.tif",
                                          latest_raster)
print "elapsed time: " + str(datetime.datetime.now() - start)
base_points_lyr = arcpy.MakeFeatureLayer_management(base_points,'latin_decrease_current_111715.lyr')

print "subtracting raster"
outras = Raster(old_raster)-Raster(latest_raster)
print "elapsed time: " + str(datetime.datetime.now() - start)
print "extract values from subtraction raster that are dropped or updated, where subtraction <> 0, return new raster"
latest_raster_extract = Con(outras != 0, latest_raster)
print "elapsed time: " + str(datetime.datetime.now() - start)
print "convert raster to point"
points_to_append = os.path.join(maindir,"pointstoappend.shp")
arcpy.RasterToPoint_conversion(latest_raster_extract,points_to_append,"VALUE")
print "elapsed time: " + str(datetime.datetime.now() - start)
points_to_append_lyr = "pointstoappend.lyr"
arcpy.MakeFeatureLayer_management(points_to_append,points_to_append_lyr)

print "select base points not identical to points to append, takes care of dropped points"
arcpy.SelectLayerByLocation_management (base_points_lyr,"ARE_IDENTICAL_TO", points_to_append_lyr, "","NEW_SELECTION")
arcpy.SelectLayerByAttribute_management(base_points_lyr,"SWITCH_SELECTION")
base_points2 = os.path.join(maindir,'latin_decrease_current_111715_2.shp')
arcpy.CopyFeatures_management(base_points_lyr,base_points2)
print "elapsed time: " + str(datetime.datetime.now() - start)
print "select points to append that are not 0, meaning they are new or updated"
where = "GRID_CODE <> 0"
arcpy.SelectLayerByAttribute_management(points_to_append_lyr,"NEW_SELECTION",where )
points_to_append2 = os.path.join(maindir,"pointstoappend_2.shp")
arcpy.CopyFeatures_management(points_to_append_lyr,points_to_append2)
print "elapsed time: " + str(datetime.datetime.now() - start)

# split points to smaller chunks
print "creating fishnet"
desc = arcpy.Describe(points_to_append2)
arcpy.CreateFishnet_management("fishnet.shp",str(desc.extent.lowerLeft),str(desc.extent.XMin) + " " + str(desc.extent.YMax + 10),"","",10,10,str(desc.extent.upperRight),"NO_LABELS","","POLYGON")
arcpy.AddField_management("fishnet.shp","split_ID","TEXT")
expression=""""ID_"+str( !FID!)"""
arcpy.CalculateField_management("fishnet.shp","split_ID",expression,"PYTHON_9.3")
print "elapsed time: " + str(datetime.datetime.now() - start)

print "splitting points into 100 chunks"
arcpy.Split_analysis(points_to_append2,"fishnet.shp","split_ID",split_dir)
print "elapsed time: " + str(datetime.datetime.now() - start)

arcpy.env.workspace = split_dir
features = arcpy.ListFeatureClasses()
country_file = r'H:\gfw_gis_team_data\gadm27_levels.gdb\adm0'
print "joining points to countries..."
for feature in features:
    points_to_append_intersect = os.path.join(split_dir_int,feature)
    print "     joining point to country file"
    arcpy.SpatialJoin_analysis(feature,country_file,points_to_append_intersect,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
    # remove extra fields
    print "     remove extra fields from " + str(feature)
    fieldstokeep = ['POINTID','GRID_CODE', 'ISO']
    fieldNameList = []
    fieldObjList = arcpy.ListFields(points_to_append_intersect)
    for field in fieldObjList:
        if not field.required:
            if not field.name in fieldstokeep:
                fieldNameList.append(field.name)
    arcpy.DeleteField_management(points_to_append_intersect, fieldNameList)
    print "elapsed time: " + str(datetime.datetime.now() - start)

print "merge all the features back into one"
arcpy.env.workspace = split_dir_int
pointstomerge = arcpy.ListFeatureClasses()
points_to_append_int_merge = os.path.join(maindir,'points_to_append_int_merge.shp')
arcpy.Merge_management(pointstomerge,points_to_append_int_merge)
arcpy.AddField_management(points_to_append_int_merge,"obs_date","TEXT")
print "elapsed time: " + str(datetime.datetime.now() - start)

print "update date field"
fields = ['GRID_CODE','obs_date']
with arcpy.da.UpdateCursor(points_to_append_int_merge,fields) as cursor:
   for row in cursor:
       gridcode = row[0]
       year = 2004+int((gridcode)/23)
       year_format = datetime.datetime.strptime(str(year) +"/01/01",'%Y/%m/%d')
       days = datetime.timedelta(days=(gridcode%23)*16)
       date_formatted= (year_format+days).strftime('%m/%d/%Y')
       row[1]=date_formatted
       cursor.updateRow(row)
       print "elapsed time: " + str(datetime.datetime.now() - start)

print "append points"
arcpy.Append_management(points_to_append_int_merge,base_points2)
print "total elapsed time: " + str(datetime.datetime.now() - start)