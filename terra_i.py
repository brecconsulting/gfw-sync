preface = '''Terra-i script will reclassify the terra_i raster so that 
only the most recent updates are available, then it converts
those updates to points in the WGS1984 projection'''

print preface

import arcpy
import os
import sys
from arcpy import env
from arcpy.sa import * 
import urllib

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

def download_terrai(url, path):
	# open terra_i data
	urllib.urlretrieve(url, path)
	return path

def get_max_value(inRaster):
	# Find max value and max value - 1
	arcpy.CalculateStatistics_management(inRaster, "1", "1")
	prop = arcpy.GetRasterProperties_management(inRaster,"MAXIMUM")
	return int(prop.getOutput(0))
	
def mask_latest_terrai(inRaster, outRaster, last):	
	# set local variables 
	field = "Value"
	remapString = RemapRange([1, last, 0])
	# Reclassify Raster
	outReclass = Reclassify(inRaster, field, remapString)
	outReclass.save(outRaster)
	return outRaster

def terra_i():
	# set environment settings 
	env.workspace = r"C:\Users\astrong\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\gfw (localhost).sde"
	url = "http://www.terra-i.org/data/current/raster/latin_decrease_current.tif"
	path = r"D:\GIS Data\GFW\temp\latin_decrease_current.tif"
	inRaster = arcpy.Raster(download_terrai(url, path)) # converts data to a raster object
	max = get_max_value(inRaster)
	last = max -1
	outRaster = "C:\Users\astrong\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\gfw (localhost).sde"
	outRaster = mask_latest_terrai(inRaster, outRaster, last)	
	print "done"

if __name__ == "__main__":
	terra_i()