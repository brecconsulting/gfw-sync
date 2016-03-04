import arcpy
import datetime, time
import urllib
import os
from archiver import *
from datetime import date
import glob

#enable extentions and overwrite permissions
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Download the data from stable url and add to R Drive
def download_data():
    print "downloading data"
    url = r"http://www.terra-i.org/data/current/raster/latin_decrease_current.tif"
    file_name = url.split("/")[-1]
    path = "R:\\"
    path_var = os.path.join(path, file_name)
    urllib.urlretrieve(url,path_var)
    print "Terra_I Downloaded to R drive"
    build_table()

#Build attribute table/add field/calculate field
def build_table():
    print "building attribute table"
    raster = "R:\\latin_decrease_current.tif"
    arcpy.BuildRasterAttributeTable_management(raster, "Overwrite")
    arcpy.AddField_management(raster, "date", "TEXT")
    print "attribute table built"
    calculate_date()

def calculate_date():
    print "calculating dates"
    raster = "R://latin_decrease_current.tif"
    fields = ['Value','date']
    with arcpy.da.UpdateCursor(raster,fields) as cursor:
        for row in cursor:
            gridcode = row[0]
            year = 2004+int((gridcode)/23)
            year_format = datetime.datetime.strptime(str(year) +"/01/01",'%Y/%m/%d')
            days = datetime.timedelta(days=(gridcode%23)*16)
            date_formatted= (year_format+days).strftime('%m/%d/%Y')
            row[1]=date_formatted
            cursor.updateRow(row)
            export_shp()
            print "dates calculated"

#Convert File to Points and add to S3
def export_shp():
    print "sending points to S3"
    input = "R://latin_decrease_current.tif"
    output = "D:\\temp\\terra_i\\terra_i.shp"
    s3 = "F:\\forest_change\\terra_i_alerts\\terra_i.shp"
    arcpy.RasterToPoint_conversion(input, output, "date")
    arcpy.Copy_management(output, s3)
    print "points uploaded to S3"

#Zip file in S3
def gen_paths(shp):
    basepath, fname = os.path.split(shp)
    base_fname = os.path.splitext(fname)[0]

    return basepath, fname, base_fname


def add_to_zip(fname, zf):

    bname = os.path.basename(fname)
    ending = os.path.splitext(bname)[1]
    if not ending ==  ".lock" and not ending == ".zip" :
        #print 'Writing %s to archive' % ending
        # flatten zipfile
        zf.write(fname, bname)

    return


def zip_shapefile(shp, dst):

    basepath, fname, base_fname = gen_paths(shp)

    zip_name = base_fname + ".zip"

    zip_path = os.path.join(dst, zip_name)
    zf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

    search = os.path.join(basepath, "*.*")
    files = glob.glob(search)
    for f in files:
        bname = os.path.basename(f)
        if (base_fname in bname) and (bname != zip_name):
            add_to_zip(f, zf)

    zf.close()

    #print '\nZip archive complete:\n%s' % dst

    return zip_name

shp = "D:\\temp\\terra_i\\terra_i.shp"
dst = "D:\\temp\\terra_i\\zip"

def copy_zip():
    src = "F://forest_change//terra_i_alerts//zip//terra_i.zip"
    s3_zip = "F://forest_change//terra_i_alerts//zip//terra_i.zip"
    shutil.copy(src,s3_zip)

#call functions
download_data()
zip_shapefile(shp, dst)
copy_zip()
