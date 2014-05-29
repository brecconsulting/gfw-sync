gfw-sync
========

Synchronization stuff for easier management of GFW data

### merge_layers.py

This python script merges features from different feature classes into one feature class and exports it as shape file.
In- and output features are defined in separate config file, found in config folder
It calls archiver.py and uploads shapefile to S3.


#### Usage

use shell, you must add an argument which config file to use

```shell
python merge_layers.py logging
```



### config/any_name.py

Config files live in the config folder and must have suffix .py
You can add as many config files as you want.

All config files must have two functions "target()" and "layers()"
Target() function must return a list with four values
1. Target Workspace
2. Target Feature Class
3. Scratch Folder
4. S3 Bucket

Layers() function must return a list with layers.
Layers are dictonaries with
1. Input Workspace
2. Input Dataset
3. Input Feature Class
4. Where clause
5. Transformation
6. Fields

Where Fields is a Dictionary with target fieldnames and their input field names or values
There must be at least a field called "country" for any target dataset


#### Logging

Logging layers must follow the following schema

```python
    layer_name = {
        'input_ws': "",  # Absolute path to Folder or GDB. Backslashes must be escaped by another backslash (\\)
        'input_ds': "",  # Name of Feature Dataset, leave empty quotes ("") if no Feature Dataset is used
        'input_fc_name': "",  # Name of Feature Class or Shapefile
        'where_clause': "",  # Filter statement (same as syntax as Definition Query in ArcMap. Leave empty quotes ("") if no filter is applied
        'transformation': "",  # ArcGIS transformation. Leave empty quotes ("") or type None (without quotes) if no transformation is needed
        'fields': {

            # for all fields:
            # if corresponding field exists type ["field", "fieldname"], fieldname is case sensitive!
            # if you want to add a fixed value for all fields type ["value", "some text"]
            # id you want to leave the field blank type None (without quotes and squared brackets)

            'country': [],  # should always be["value", "3 letter ISO-Code"],
            'year': [],  #  should always be ["value", now.year]
            'type': [],
            'name': [],
            'company': [],
            'group_company': [],
            'group_country': [],
            'province': [],
            'status': [],
            'area_ha': [],
            'source': [],
            'shape_length': [],
            'shape_area': []
        }
    }
```

afterwards add input file to country list

```python
countries = [layer_name_1, layer_name_2, ...]
```



### Archiver.py

This python script handles zipping a single shapefile and uploading it to S3.

It assumes that you have set your AWS credentials in your environment. On Linux, you'd add this to your `.bashrc` file (with actual values of course):

```shell
export AWS_ACCESS_KEY_ID="<access id>"
export AWS_SECRET_ACCESS_KEY="<secret key>"
```

On Windows:

1. Create your file with the name you want(e.g boto_config.cfg) and place it in a location of your choice (e.g C:\Users\<your_account_name>\configs).
2. Specify your credentials in the credential section of your file:

```python
[Credentials]
aws_access_key_id = <access id>
aws_secret_access_key = <secret key>"
```

3. Create an environment variable with the Name='BOTO_CONFIG' and Value= file_locatio/file_name
4. Boto is now ready to work with credentials automatically configured!


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
