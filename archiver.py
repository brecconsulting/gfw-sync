#!/usr/bin/env python2.7


import os
import zipfile
import shutil
import time
import datetime


def gen_paths(shp):
    basepath, fname = os.path.split(shp)
    base_fname = os.path.splitext(fname)[0]

    return basepath, fname, base_fname


def add_to_zip(dirname, fname, zf):

    full_path = os.path.join(dirname, fname)
    print 'Writing %s to archive' % os.path.splitext(fname)[1]
    # flatten zipfile
    zf.write(full_path, fname)

    return


def zip_shapefile(shp, dst, local):

    basepath, fname, base_fname = gen_paths(shp)

    if local:
        zip_name = base_fname + ".zip"
    else:
        zip_name = base_fname + "_local.zip"

    zip_path = os.path.join(dst, zip_name)
    zf = zipfile.ZipFile(zip_path, 'w', allowZip64=False)

    for dirname, subdirs, files in os.walk(basepath):
        for f in files:
            if (base_fname in f) and (f != zip_name):
                add_to_zip(dirname, f, zf)

    zf.close()

    print '\nZip archive complete:\n%s' % dst

    return zip_name


def archive_shapefile(shp_path, zip_folder, dst_folder=None, arc_folder=None, local=False):

    print 'Processing %s' % shp_path

    zip_name = zip_shapefile(shp_path, zip_folder, local)

    if dst_folder is not None:
        src = os.path.join(zip_folder, zip_name)
        dst = os.path.join(dst_folder, zip_name)
        print "Copy ZIP archive to %s" % dst_folder
        shutil.copy(src, dst)

    if arc_folder is not None:
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        src = os.path.join(zip_folder, zip_name)
        dst = os.path.join(arc_folder, "%s_%s.zip" % (zip_name, timestamp))
        shutil.copy(src, dst)

    print 'Processing complete.'



