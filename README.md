gfw-sync
========

Synchronization stuff for easier management of GFW data

### merge_country_layers.py

This python script merges features from different feature classes into one feature class.

#### Configuration

Input feature classes can be configured within the script


input_feature_class = {
    'input_ws': "full_path_to_gdb",  # full path to input workspace, escape backslashes (\) with another backslash
    'input_ds': "dataset_name",  # name of feature dataset, if no feaure class not in a feature dataset type ""
    'input_fc_name': "feature_class_name",  # input feature_class name
    'country_code': "ISO_3166-1 Code",  # use three letter country code (http://en.wikipedia.org/wiki/ISO_3166-1)
    'layer_type': "layer type",  # feature type, use when fields{'type'] is None, otherwise type None
    'where_clause': "SQL style where clause",  # to use entire dataset type "", string expressions within the where clause must be with single quotes
    'transformation': "ArcGIS transformation name",  # specify geographic transformation (if necessary, otherwise type ""). Features will be projected to WGS_1984_Web_Mercator_Auxiliary_Sphere
    'fields': {
        'type': "type field name",  # if field is not provided type ""
        'company': "company field name",  # if field is provided type field name (case sensitive!)
        'group': "group field name",  # if field is provided type field name (case sensitive!)
        'area': "area field name",  # if field is provided type field name (case sensitive!)
        'shape_length': "shape length field name",  # if field is provided type field name (case sensitive!)
        'shape_area': "shape area field name"  # if field is provided type field name (case sensitive!)
    }
}


afterwards add input file to country list

countries = [input_feature_class1, input_feature_class2, ...]


#### Usage

python merge_country_layers.py



### Archiver.py

This python script handles zipping a single shapefile and uploading it to S3.

It assumes that you have set your AWS credentials in your environment. On Linux, you'd add this to your `.bashrc` file (with actual values of course):

```shell
export AWS_ACCESS_KEY_ID="<access id>"
export AWS_SECRET_ACCESS_KEY="<secret key>"
```

On Windows:

1- Create your file with the name you want(e.g boto_config.cfg) and place it in a location of your choice (e.g C:\Users\<your_account_name>\configs).

2- Specify your credentials in the credential section of your file:
    [Credentials]
    aws_access_key_id = <access id>
    aws_secret_access_key = <secret key>"

3- Create an environment variable with the Name='BOTO_CONFIG' and Value= file_locatio/file_name

4- Boto is now ready to work with credentials automatically configured!


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
>>> archiver.main('worldborder_sinusoidal.shp', '/tmp/worldborder_sinusoidal.zip',
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
