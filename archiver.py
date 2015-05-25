#!/usr/bin/env python2.7


import os
import glob
import zipfile
import shutil
import time
import datetime


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


def zip_shapefile(shp, dst, local):

    basepath, fname, base_fname = gen_paths(shp)

    if local:
        zip_name = base_fname + "_local.zip"
    else:
        zip_name = base_fname + ".zip"

    zip_path = os.path.join(dst, zip_name)
    zf = zipfile.ZipFile(zip_path, 'w', allowZip64=False)

    search = os.path.join(basepath, "*.*")
    files = glob.glob(search)
    for f in files:
        bname = os.path.basename(f)
        if (base_fname in bname) and (bname != zip_name):
            add_to_zip(f, zf)

    zf.close()

    #print '\nZip archive complete:\n%s' % dst

    return zip_name


def archive_shapefile(shp_path, zip_folder, dst_folder=None, arc_folder=None, local=False):

    print 'Zip %s' % shp_path

    zip_name = zip_shapefile(shp_path, zip_folder, local)
    src = os.path.join(zip_folder, zip_name)

    if dst_folder is not None:
        if not os.path.exists(dst_folder):
            os.mkdir(dst_folder)
        dst = os.path.join(dst_folder, zip_name)
        print "Copy ZIP to %s" % dst_folder
        #print src
        #print dst
        shutil.copy(src, dst)

    if arc_folder is not None:
        if not os.path.exists(arc_folder):
            os.mkdir(arc_folder)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        dst = os.path.join(arc_folder, "%s_%s.zip" % (os.path.splitext(zip_name)[0], timestamp))
        #dst = os.path.join(arc_folder, zip_name)
        print "Copy archived ZIP to %s" % arc_folder
        #print src
        #print dst
        shutil.copy(src, dst)

    #print 'Processing complete.'




