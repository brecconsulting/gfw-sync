__author__ = 'Thomas.Maschler'

import urllib
import zipfile
import os
import re
import shutil
import arcpy
import string

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)



url = "http://wcmc.io/wdpa_current_release"
path = "C:\\temp"  #"D:\\GIS Data\\Global"

zip_name = "wdpa_current_release.zip"
zip_path = os.path.join(path, zip_name)
path_gdb = os.path.join(path, "wdpa_current_release.gdb")
temp_folder = os.path.join(path, "temp")

try:
    shutil.rmtree(path_gdb)
except:
    pass

urllib.urlretrieve(url, zip_path)

unzip(zip_path, temp_folder)

path_gdb = os.path.join(path, "wdpa_current_release.gdb")

sub_folders = [x[0] for x in os.walk(temp_folder)]


for f in sub_folders:
    if re.findall("\W+WDPA\w+\.gdb", f):
        shutil.move(f, path_gdb)
        break

os.remove(zip_path)
shutil.rmtree(temp_folder)

arcpy.env.workspace = path_gdb
fc_list = arcpy.ListFeatureClasses()

for fc in fc_list:
    desc = arcpy.Describe(fc)
    if desc.shapeType == 'Polygon':
        arcpy.Rename_management(fc, 'wdpa_poly', "FeatureClass")
    elif desc.shapeType == 'Point' or desc.shapeType == 'Multipoint':
        arcpy.Rename_management(fc, 'wdpa_point', "FeatureClass")


