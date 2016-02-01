''' author: Sam Gibbes
date: 2/1/16
'''

import datetime, time
import urllib
import os
from archiver import *
from datetime import date

destination_latest_raster = r'C:\Users\samantha.gibbes\Documents\gis\terraI'
name_latest_raster= "latest_raster.tif"
zip_folder = r'C:\Users\samantha.gibbes\Documents\gis\terraI\zipfolder'

print "downloading latest file"
latest_raster = os.path.join(destination_latest_raster,name_latest_raster)
terrai_file = urllib.urlretrieve("http://www.terra-i.org/data/current/raster/latin_decrease_current.tif",
                                          latest_raster)
print "archive current raster"
current_raster = r'/'
archive_directory = r'/'
prefix =  date.fromtimestamp(time.time()).strftime("%m%d%y")

def zip_raster(rst, dst):
    basepath, fname, base_fname = gen_paths(rst)
    zip_name = prefix + "_"+ base_fname + ".zip"
    zip_path = os.path.join(dst, zip_name)
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

    bname = os.path.basename(rst)
    if (base_fname in bname) and (bname != zip_name):
        add_to_zip(rst, zf)
    zf.close()
zip_raster(latest_raster,zip_folder)