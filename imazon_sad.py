from urllib2 import urlopen
import os
import sys
import datetime

from bs4 import BeautifulSoup
import requests

import zipfile

import arcpy
import merge_layers
import archiver
import shutil


def get_soup(url):
    """Make BeautifulSoup object from a url."""
    html = urlopen(url).read()
    bs = BeautifulSoup(html, 'lxml')
    return bs


def recent_file(min_date, url):
    try:
        yrmo = url.split('_')[3]
        year, month = [int(i) for i in yrmo.split('-')]
        dt = datetime.datetime(year, month, 1)

        if dt >= min_date:
            return True
        else:
            return False

    except:
        return False


def parse_urls(bs, mindate):
    # get list elements
    tds = [td.find('a') for td in bs('td')]

    # get urls from list elements li if they exist
    urls = [td['href'] for td in tds if td]

    # only keep urls containing 'desmatamento' or 'degradacao'
    urls = [url for url in urls if 'desmatamento' in url
            or 'degradacao' in url]

    # only return urls from 2014 or later
    return [url for url in urls if recent_file(mindate, url)]


def download_zipfile(url, output_dir):
    fname = os.path.split(url)[1]
    path = os.path.join(output_dir, fname)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    r = requests.get(url, stream=True)

    print "Downloading %s" % url
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
            f.flush
    print "Download complete."
    return path


def make_path(prefix, url):
    fname = os.path.split(url)[1]
    return os.path.join(prefix, fname)



def mirror_sad_files(url, sad_folder, mindate=None, test=False):
    #sad_folder = r"F:\forest_change\imazon_sad"
    #url = 'http://www.imazongeo.org.br/doc/downloads.php'

    if mindate is None:
        mindate= datetime.datetime(2014, 1, 1)  # we've already got stuff < 2014

    
    uploaded = []

    print "Get urls"
    bs = get_soup(url)
    urls = parse_urls(bs, mindate)

    if test:
        urls = [urls[0]]
    
    for url in urls:
        sad_file = make_path(sad_folder, url)
        if not 'http://' in url:
            url = 'http://imazongeo.org.br%s' % url
        if not os.path.exists(sad_file):
            print "Download from %s" % url
            z = download_zipfile(url, sad_folder)
            uploaded.append(sad_file)
        else:
            print 'File already exists at %s' % (sad_file)

    return uploaded
 
    
def unzip(filename, folder):
    if zipfile.is_zipfile(filename):
        zf = zipfile.ZipFile(filename, 'r')
        zf.extractall(folder)
        return zf.namelist()
    else:
        return []


def get_date_from_filename(filename):
    parts = filename.split('_')
    date_obj = datetime.datetime.strptime(parts[3], '%Y-%m')
    
    return date_obj


def get_data_type_from_filename(filename):
    parts = filename.split('_')
    dtype = parts[2]
    if dtype == 'desmatamento':
        return 'defor'
    elif dtype == 'degradacao':
        return 'degrad'
    

def append_to_imazon_sad(input_shp, target_fc):
    
    input_layer = "layer"
    arcpy.MakeFeatureLayer_management(input_shp, input_layer)
    print "Create field map"
    fms = arcpy.FieldMappings()
    fms.addFieldMap(merge_layers.create_field_map(input_shp, "FID", "orig_oid"))

    print "Append layer"
    arcpy.Append_management(input_layer, target_fc, "NO_TEST", fms, "")

    target_layer = "target_layer"
    arcpy.MakeFeatureLayer_management(target_fc, target_layer, "orig_fname IS NULL OR orig_fname = ''", "", "")

    date_obj = get_date_from_filename(input_shp)
    data_type = get_data_type_from_filename(input_shp)
    fname = os.path.basename(input_shp)

    print "update fields"
    arcpy.CalculateField_management(target_layer, "date", "'%s'" % date_obj.strftime("%m/%d/%Y"), "PYTHON", "")
    arcpy.CalculateField_management(target_layer, "data_type", "'%s'" % data_type, "PYTHON", "")
    arcpy.CalculateField_management(target_layer, "orig_fname", "'%s'" % fname, "PYTHON", "")

    




def update_imazon_sad():
    sad_folder = r"C:\Users\asa.strong\Documents\Global Forest Watch\Data Management\Data Updates\Imazon SAD\download"
    url = 'http://www.imazongeo.org.br/doc/downloads.php'
    scratch_folder = r"C:\Users\asa.strong\Documents\Global Forest Watch\Data Management\Data Updates\Imazon SAD\temp"
    gdb = r"C:\Users\asa.strong\Documents\Global Forest Watch\Data Management\Data Updates\Imazon SAD\forest_change.gdb"
    fc = "imazon_sad"
    default_srs = "WGS 1984"
    gdb_srs = 'WGS 1984 Web Mercator (auxiliary sphere)'

    arcpy.env.overwriteOutput = True

    target_fc = os.path.join(gdb,fc)

    print "Clear workspace"
    merge_layers.clear_workspace(scratch_folder)
        

    print "Mirror files"
    zipfiles = mirror_sad_files(url, sad_folder)

    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(gdb_srs)

    for zf in zipfiles:
        bname = os.path.basename(zf)
        fpath = os.path.join(scratch_folder, bname)
        shutil.copy(zf, fpath)
        files = unzip(fpath, scratch_folder)
        
        for f in files:
            if os.path.splitext(f)[1] == ".shp":
                shp_path = os.path.join(scratch_folder, f)
                break
        
        append_to_imazon_sad(shp_path,target_fc)

    print "repair geometries"
    arcpy.RepairGeometry_management(target_fc, "DELETE_NULL")

    export_folder = os.path.join(scratch_folder, "export")
    arcpy.FeatureClassToShapefile_conversion([target_fc], export_folder)

    export_shp =  os.path.join(export_folder,fc + ".shp")

    archiver.archive_shapefile(export_shp, scratch_folder, local=True)

    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(default_srs)

    arcpy.FeatureClassToShapefile_conversion([target_fc], scratch_folder)

    archiver.archive_shapefile(export_shp, scratch_folder, local=False)


update_imazon_sad()
