''' author: Sam Gibbes
Date: 11/5/15
 purpose: Start with a file of all terra i point, this script will append new terra i updates
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
maindir = r'D:\_sam\terraI\testing'
arcpy.env.workspace = maindir
arcpy.env.scratchWorkspace = os.path.join(maindir,'scratch.gdb')

# set input files
print "downloading latest file"
latest_raster = os.path.join(maindir,'latest_file.tif')
if not os.path.exists(latest_raster):
    terrai_file = urllib.urlretrieve("http://www.terra-i.org/data/current/raster/latin_decrease_current.tif",
                                              latest_raster)
else:
    pass

base_points = os.path.join(maindir,'latin_decrease_current_111715.shp')
country_file = r'H:\gfw_gis_team_data\gadm27_levels.gdb\adm0'


arcpy.CheckOutExtension("Spatial")
points_to_append = os.path.join(maindir,"pointstoappend.shp")
if not os.path.exists(points_to_append):
    # find max value from base points
    print "find max value"
    arcpy.MakeFeatureLayer_management(base_points,"base_points_lyr")
    max_base_value  = arcpy.SearchCursor("base_points_lyr", "", "", "","GRID_CODE D").next().getValue("GRID_CODE")
    print max_base_value
    # extract values from latest raster that are larger than target
    print "extract values from latest raster that are larger than target"
    where = "VALUE > " + str(max_base_value)
    latest_raster_extract = ExtractByAttributes(latest_raster, where)
    

    # convert raster to point
    print "convert raster to point"
    arcpy.RasterToPoint_conversion(latest_raster_extract,points_to_append,"VALUE")


# split points to smaller chunks
print "creating fishnet"
desc = arcpy.Describe(points_to_append)
arcpy.CreateFishnet_management("fishnet.shp",str(desc.extent.lowerLeft),str(desc.extent.XMin) + " " + str(desc.extent.YMax + 10),"","",10,10,str(desc.extent.upperRight),"NO_LABELS","","POLYGON")
arcpy.AddField_management("fishnet.shp","split_ID","TEXT")
expression=""""ID_"+str( !FID!)"""
arcpy.CalculateField_management("fishnet.shp","split_ID",expression,"PYTHON_9.3")

print "splitting points into 100 chunks"
split_dir = os.path.join(maindir,"split.gdb")
if not os.path.exists(split_dir):
    arcpy.CreateFileGDB_management(maindir,"split.gdb")
arcpy.Split_analysis(points_to_append,"fishnet.shp","split_ID",split_dir)


split_dir_int = os.path.join(maindir,"split_int.gdb")
arcpy.CreateFileGDB_management(maindir,"split_int.gdb")
arcpy.env.workspace = split_dir
features = arcpy.ListFeatureClasses()

print "joining points to countries..."
for feature in features:
    points_to_append_intersect = os.path.join(split_dir_int,feature)
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

print "merge all the features back into one"
arcpy.env.workspace = split_dir_int
pointstomerge = arcpy.ListFeatureClasses()
points_to_append_int_merge = os.path.join(maindir,'points_to_append_int_merge.shp')
arcpy.Merge_management(pointstomerge,points_to_append_int_merge)

# add observation date field to points to append
arcpy.AddField_management(points_to_append_int_merge,"obs_date","TEXT")

# update date field
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

# append points
print "append points"
arcpy.Append_management(points_to_append_int_merge,base_points)
print "total elapsed time: " + str(datetime.datetime.now() - start)