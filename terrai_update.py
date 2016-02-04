''' author: Sam Gibbes
date: 2/1/16
'''

import datetime, time
import urllib
import os
from archiver import *
from datetime import date
import glob


'''Create zipped, unzipped, and archived raster in s3 for visualization.'''

destination_latest_raster = r'F:\forest_change\terra_i_alerts'
name_latest_raster= "latest_raster.tif"
zip_folder = r'F:\forest_change\terra_i_alerts\zip'

print "downloading latest file"
latest_raster = os.path.join(destination_latest_raster,name_latest_raster)
terrai_file = urllib.urlretrieve("http://www.terra-i.org/data/current/raster/latin_decrease_current.tif",
                                          latest_raster)
print "archive current raster"
current_raster = r'F:\forest_change\terra_i_alerts\latin_decrease_current.tif'
archive_directory = r'F:\forest_change\terra_i_alerts\archive'
prefix =  date.fromtimestamp(time.time()).strftime("%m%d%y")


'''Create zipped raster in s3 for visualization'''

def zip_raster(rst, dst):
    basepath, fname, base_fname = gen_paths(rst)
    # zip_name = timestamp + "_"+ base_fname + ".zip"
    zip_name = base_fname + ".zip"
    zip_path = os.path.join(dst, zip_name)
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

    bname = os.path.basename(rst)
    if (base_fname in bname) and (bname != zip_name):
        add_to_zip(rst, zf)
    zf.close()

# destination_latest_raster = r'F:\forest_change\terra_i_alerts'
# zip_folder = r'F:\forest_change\terra_i_alerts\zip'
# archive_directory = r'F:\forest_change\terra_i_alerts\archive'

timestamp =  date.fromtimestamp(time.time()).strftime("%m%d%y")
basename = "latest_raster.tif"

zip_folder =r'C:\Users\samantha.gibbes\Documents\gis\terraI\terraitest\zipfolder'
destination_latest_raster = r'C:\Users\samantha.gibbes\Documents\gis\terraI\terraitest\destination'
archive_directory = r'C:\Users\samantha.gibbes\Documents\gis\terraI\terraitest\archivefolder'

latest_raster = os.path.join(destination_latest_raster,basename)
existing = glob.glob(os.path.join(destination_latest_raster,"*"))

if len(existing) == 1:
    for i in existing:
        print "archiving old raster"
        shutil.copy(i,os.path.join(archive_directory,timestamp+"_"+basename))
        print "deleting old raster"
        os.remove(i)
if len(existing) > 1:
    print "more than 1 raster exists, not sure which to archive, fail"
    quit()
print "delete old zip"
zips = glob.glob(zip_folder+"\\"+"*")
if len(zips)>0:
    for z in zips:
        os.remove(z)
print "downloading latest raster"
terrai_file = urllib.urlretrieve("http://www.terra-i.org/data/current/raster/latin_decrease_current.tif",
                                          latest_raster)
print "zip latest raster"
zip_raster(latest_raster,zip_folder)

'''replace raster on R drive for analysis'''
