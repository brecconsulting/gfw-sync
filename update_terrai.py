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

# joining new points with country file
print "joining new points with country file"
points_to_append_intersect = "pointstoappend_intersect.shp"

# split points to smaller chunks
arcpy.MakeFeatureLayer_management(points_to_append,"points_to_append_lyr")
arcpy.MakeFeatureLayer_management(country_file,"country_file_lyr")
arcpy.SpatialJoin_analysis("points_to_append_lyr","country_file_lyr",points_to_append_intersect,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT")
# remove extra fields
print "remove extra fields"
fieldstokeep = ['POINTID','GRID_CODE', 'ISO']
fieldNameList = []
fieldObjList = arcpy.ListFields(points_to_append_intersect)
for field in fieldObjList:
    if not field.required:
        if not field.name in fieldstokeep:
            fieldNameList.append(field.name)
arcpy.DeleteField_management(points_to_append_intersect, fieldNameList)

# add observation date field to points to append
arcpy.AddField_management(points_to_append_intersect,"obs_date","TEXT")

# update date field
print "update date field"
fields = ['GRID_CODE','obs_date']
with arcpy.da.UpdateCursor(points_to_append_intersect,fields) as cursor:
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
arcpy.Append_management(points_to_append_intersect,base_points)
