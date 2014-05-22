gfw-sync
========

Synchronization stuff for easier management of GFW data

### Archiver.py

This python script handles zipping a single shapefile and uploading it to S3.

It assumes that you have set your AWS credentials in your environment. On Linux, you'd add this to your `.bashrc` file (with actual values of course):

```shell
export AWS_ACCESS_KEY_ID="<access id>"
export AWS_SECRET_ACCESS_KEY="<secret key>"
```

#### Usage

You must provide four arguments to the `main` function:

1. input shapefile path - best to use full, absolute paths
2. zip output path
3. s3 path
4. s3 bucket name

You can run this script from the command line:

```shell
python archiver.py /tmp/worldborder_sinusoidal.shp /tmp/worldborder_sinusoidal.zip data/worldborder_sinusoidal.zip gfwdata
```

Or you can use it directly from your Python REPL:

```python
>>> import archiver
>>> main('worldborder_sinusoidal.shp', '/tmp/worldborder_sinusoidal.zip',
    'data/worldborder_sinusoidal.zip', 'gfwdata')
Processing worldborder_sinusoidal.shp
Zipping worldborder_sinusoidal.shp
Writing .dbf to archive
Writing .prj to archive
Writing .shp to archive
Writing .shx to archive

Zip archive complete:
/tmp/worldborder_sinusoidal.zip
Uploading to s3
Upload complete
Processing complete.
{'shapefile': 'worldborder_sinusoidal.shp', 's3path': 'data/worldborder_sinusoidal.zip', 'bucket': 'gfwdata', 'zip_path': '/tmp/worldborder_sinusoidal.zip'}
```
