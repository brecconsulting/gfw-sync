import arcpy
import numpy
from arcpy import env
from arcpy.sa import *

#Check out ArcGIS Extensions
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = r"D:\temp\environment"

#identify max values in previous data
print "searching for peru max" 
peru = r"D:\Skybox\older_points\peru_umd_alerts.shp" #path to points used in last analysis 
peru_max = arcpy.SearchCursor(peru, "", "", "","GRID_CODE D").next().getValue("GRID_CODE")
print peru_max

#Extract values for peru
print "extracting latest alerts for peru from S3"
peru_tif = r"U:\peru_day2015.tif" #path to latest umd alerts in s3
where_clause = "Value > " + str(peru_max)
per_extract = ExtractByAttributes(peru_tif, where_clause)
per_extract.save(r"D:\Skybox\latest_raster\peru_latest.tif")

#convert latest tif to points for peru 
print "converting latest alerts for peru into points"
peru_latest = r"D:\Skybox\latest_raster\peru_latest.tif"
peru_output = r"D:\Skybox\latest_points\peru_latest.shp"
arcpy.RasterToPoint_conversion(peru_latest, peru_output, "Value")

#analyze latest points using kernel density function
print "running kernel density analysis"
outKernelDensity = KernelDensity(peru_output, "NONE", "", "", "HECTARES") #need an output with pixel type integer
outKernelDensity.save(r"D:\Skybox\analysis_layers\peru_density")
print "analysis results available here D:\Skybox\analysis_layers\peru_density"

# Convert output to integer pixel type
print "converting analysis results to type integer"
kernel = r"D:\Skybox\analysis_layers\peru_density.grid"
final_output = Int(kernel)
final_output.save(r"D:\Skybox\analysis_layers\peru_den_int")
print "results available here D:\Skybox\analysis_layers\peru_den_int"

#Build Attribute table for peru_den_int
print "building raster attribute table"
raster = r"D:\Skybox\analysis_layers\peru_den_int"
arcpy.BuildRasterAttributeTable_management(raster)

# Identify max value
print "creating max table"
env.workspace = r"D:\Skybox\analysis_layers"
in_table = "peru_den_int"
out_table = "peru_max"
fields = [["Rowid", "MAX"]]
casefield = ""
arcpy.Statistics_analysis(in_table, out_table, fields, casefield) 
print "peru_max table created"

#assign the max value to a variable 
print "searching for max value"
env.workspace = r"D:\Skybox\analysis_layers"
in_table = "peru_max"
field_names = ["MAX_ROWID"]
max_value = arcpy.da.SearchCursor (in_table, field_names)
for row in max_value:
	peru_max = row[0]
print peru_max

#Create threshold
threshold = peru_max - 100
print threshold

#extract by threshold 
print "extracting top 100 max values"
env.workspace = r"D:\Skybox\analysis_layers"
in_raster = "peru_den_int"
where_clause = "\"Rowid\">="+str(threshold)
extract = ExtractByAttributes (in_raster, where_clause)
extract.save(r"D:\Skybox\analysis_layers\peru_max")
print "Top 100 density cells extracted to peru_max"

#convert final density cells to points 
print "converting top 100 density cells to points"
env.workspace = r"D:\Skybox\analysis_layers"
density_output = "density_points.shp"
density_input = "peru_max" 
arcpy.RasterToPoint_conversion(density_input, density_output, "VALUE")
print "ANALYSIS COMPLETE"

#Final Step: Post all umd points to D:\Skybox\older_points\peru_umd_alerts.shp
print "converting all peru data to points in D:\Skybox\older_points\peru_umd_alerts.shp"
peru_output = r"D:\Skybox\older_points\peru_umd_alerts.shp"
peru_tif = r"U:\peru_day2015.tif" #path to latest umd alerts in s3
arcpy.RasterToPoint_conversion(peru_tif, peru_output, "Value")
print "data now available in D:\Skybox\older_points\peru_umd_alerts.shp"







