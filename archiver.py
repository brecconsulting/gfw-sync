#!/usr/bin/env python2.7

"""This module zips up a shapefile's constituent parts and uploads
them to S3."""

import sys
import os
import subprocess
import zipfile

import boto
from boto.s3.key import Key

# standard shell command to generate flat zipfile
BASECMD = 'zip -j %s %s*'

def gen_paths(shp):
    basepath, fname = os.path.split(shp)
    base_fname = os.path.splitext(fname)[0]

    return basepath, fname, base_fname

def add_to_zip(dirname, fname, zf):
    full_path = os.path.join(dirname, fname)
    
    print 'Writing %s to archive' % os.path.splitext(fname)[1]
    zf.write(full_path, fname) # flatten zipfile

    return

def zip(shp, dst):

    basepath, fname, base_fname = gen_paths(shp)

    zf = zipfile.ZipFile(dst, 'w', allowZip64=False)

    for dirname, subdirs, files in os.walk(basepath):
        print 'Zipping %s' % shp
        for f in files:
            if (base_fname in f) and (f != dest):  # only process components of specified shapefile
                add_to_zip(dirname, f, zf)

    zf.close()

    print '\nZip archive complete:\n%s' % dst

    return

def create_bucket_conn(bucket_name):
    conn = boto.connect_s3() # requires creds in environment
    return conn.create_bucket(bucket_name)

def add_to_s3(path, s3path, bucket):
    k = Key(bucket)
    k.key = s3path

    print 'Uploading to s3'
    k.set_contents_from_filename(path)
    print 'Upload complete'

    return k

def upload(path, s3path, bucket_name):
    """Upload file to S3."""

    bucket = create_bucket_conn(bucket_name)

    k = add_to_s3(path, s3path, bucket)

    return dict(zip_path=path, bucket=bucket_name, s3path=s3path)

def main(shp_path, zip_path, s3path, bucket_name):

    print 'Processing %s' % shp_path

    zip(shp_path, zip_path)

    dct = upload(zip_path, s3path, bucket_name)
    dct['shapefile'] = shp_path

    print 'Processing complete.'

    return dct

if __name__ == '__main__':
    shp_path = sys.argv[1]
    zip_path = sys.argv[2]
    s3path = sys.argv[3]
    bucket_name = sys.argv[4]

    print main(shp_path, zip_path, s3path, bucket_name)
