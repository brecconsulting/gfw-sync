gfw-sync
========

Synchronization stuff for easier management of GFW data


#### Usage

To update all layers call

Command line
```shell
python gfw_sync.py
```

To update specific layers call

Command line
```shell
python gfw_sync.py logging mining
```


Python:
```python
>>> import merge_layers
>>> merge_layers.merge('logging')
```



### Configuration

Layer files live in the layer folder and must have suffix .py
You can add as many layer files as you want.

All layer files must contain function "layers()"

Layers() function must return a list with layers.

Layers are Python dictionaries with the following keys:

1. Location
2. Full Path to file or feature class
3. Where clause
4. Transformation
5. Fields

Fields is also a python dictionary, keys correspond to field names in target feature class; values can contain field names, fixed values or expressions
There must be at least a field called "country" for any target dataset


#### Example

Logging layers must follow the following schema

```python
    layer_name = {
        'location: "" # Either "S3" or "Server"
        'full_path': "" # Full path to file or feature class. For server including Drive name, for s3 including bucket name. For geodatabases including feature dataset name
        'where_clause': "",  # Definition query (same as syntax as Definition Query in ArcMap. Leave empty quotes ("") if no filter is applied
        'transformation': "",  # ArcGIS transformation. Leave empty quotes ("") or type None (without quotes) if no transformation is needed
        'fields': {

            # for all fields:
            # if corresponding field exists type ["field", "fieldname"], fieldname is case sensitive!
            # if you want to add a fixed value for all fields type ["value", "some text"]
            # if you want to add an expression based type ["expression", "some expression"], expression must correspond to Python expression in "Calculate Field" Tool
            # Example: ["expression", "!SHAPE_Area!/10000"]
            # if you want to leave the field blank type None (without quotes and squared brackets)

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
            'shape_length': [],  # optional, can be left out
            'shape_area': []  # optional, can be left out
        }
    }
```

afterwards add input file to country list at the end of file

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
