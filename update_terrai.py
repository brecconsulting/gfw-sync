''' author: Sam Gibbes
Date: 11/5/15
 purpose: Start with a file of all terra i point, this script will append new terra i updates
'''
import datetime, time
import arcpy
from arcpy.sa import *
import datetime
# set environments
arcpy.env.overwriteOutput = "TRUE"
arcpy.env.workspace = r'D:\_sam\terraI'
arcpy.env.scratchWorkspace = r'D:\_sam\terraI\scratch.gdb'

# set input files
latest_raster = r'D:\_sam\terraI\latin_decrease_current_proj_clip.tif'
base_points = r'D:\_sam\terraI\latin_decrease_current_proj_clip.shp'

country_file = r'H:\gfw_gis_team_data\gadm27_levels.gdb\adm0'
arcpy.CheckOutExtension("Spatial")
# find max value from base points
arcpy.MakeFeatureLayer_management(base_points,"base_points_lyr")
max_base_value  = arcpy.SearchCursor("base_points_lyr", "", "", "","GRID_CODE D").next().getValue("GRID_CODE")

# extract values from latest raster that are larger than target
where = "VALUE > " + str(max_base_value)
latest_raster_extract = ExtractByAttributes(latest_raster, where)
points_to_append = "pointstoappend.shp"

# convert raster to point
arcpy.RasterToPoint_conversion(latest_raster_extract,points_to_append,"VALUE")

# intersect new points with country file
points_to_append_intersect = "pointstoappend_intersect.shp"
arcpy.Intersect_analysis([points_to_append,country_file],points_to_append_intersect)

# remove extra fields
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
arcpy.Append_management(points_to_append_intersect,base_points)
