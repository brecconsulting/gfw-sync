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
merged_file = r"D:\temp\umd\points\gfw_landsat_alerts.shp"
arcpy.Merge_management(["roc_day2015.shp", "peru_day2015.shp", "borneo_day2015.shp"], merged_file)
print "points merged"

#add date field to merged file 
merged_file = "D:\temp\umd\points\gfw_landsat_alerts.shp"
field_name = "date"
field_type = "TEXT"
arcpy.AddField_management(merged_file, field_name, field_type)
print "date field added"

#Create function that converts julian dates to regular dates 

def getDate(day):
	Y=2015
	if day < 32:
		M = 1 
		D = day
	elif day < 60:
		M = 2
		D = day - 31
	elif day < 91:
		M = 3
		D = day - 59
	elif day < 121:
		M = 4
		D = day - 90
	elif day < 152:
		M = 5
		D = day - 120
	elif day < 182:
		M = 6
		D = day - 151
	elif day < 213:
		M = 7
		D = day - 181
	elif day < 244:
		M = 8
		D = day - 212
	elif day < 274:
		M = 9
		D = day - 243
	elif day < 305:
		M = 10
		D = day - 273
	elif day < 335:
		M = 11
		D = day - 304
	elif day < 366:
		M = 12
		D = day - 334
	d =str( D) + "-" + str(M) + "-" + str(Y)
	return d

#execute calculate field 
expression = getDate("!GRID_CODE!")
field_name = "date"	
arcpy.CalculateField_management(merged_file, field_name, expression, "PYTHON_9.3")
print "dates converted"
	

