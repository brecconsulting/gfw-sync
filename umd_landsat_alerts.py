import urllib
import os 
import arcpy
from arcpy import env
from arcpy.sa import *
from datetime import datetime

#Check out ArcGIS Extensions
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#specify S3 urls to the umd alert data 
urls = [
r"http://umd-landsat-alerts.s3.amazonaws.com/roc_day2015.tif", 
r"http://umd-landsat-alerts.s3.amazonaws.com/peru_day2015.tif",
r"http://umd-landsat-alerts.s3.amazonaws.com/borneo_day2015.tif",
]

#download urls and save them to a temporary file 
for url in urls:
	file_name = url.split("/")[-1]
	path_var = os.path.join (r"D:\temp\umd", file_name)
	urllib.urlretrieve(url,path_var)
	print "downloaded"

#specify locations for temporary file storage 	
files = [
r"D:\temp\umd\roc_day2015.tif",
r"D:\temp\umd\peru_day2015.tif",
r"D:\temp\umd\borneo_day2015.tif",
]

#convert files to points 
for file in files:
	point_name = os.path.basename(file)
	output = os.path.join(r"D:\temp\umd\points", point_name)
	value = "Value"
	arcpy.RasterToPoint_conversion(file, output, value)
	print "converted to points"

#specify point data location 
points = [
r"D:\temp\umd\points\roc_day2015.shp",
r"D:\temp\umd\points\peru_day2015.shp",
r"D:\temp\umd\points\borneo_day2015.shp",
]

#merge point data 
arcpy.env.workspace = r"D:\temp\umd\points"
merged_file = "D:\temp\umd\points\gfw_landsat_alerts.shp"
arcpy.Merge_management(["roc_day2015.shp", "peru_day2015.shp", "borneo_day2015.shp"], merged_file)

#add date field to merged file 
merged_file = "D:\temp\umd\points\gfw_landsat_alerts.shp"
field_name = "date"
field_type = "TEXT"
arcpy.AddField_management(merged_file, field_name, field_type)

#Calculate date from julian dates "GRID_CODE"
expression = convert_julian(!GRID_CODE!)
code_block = """"
def convert_julian(date):
	d = datetime.datetime.strptime(date, '%j')
	d.strftime("%Y/%m/%d")
	dnew = d.replace(year = 2015)
	return dnew """
arcpy.CalculateField_management(merged_file, field_name, expression, "PYTHON_9.3", code_block)
	

