gfw-sync
========

Synchronization stuff for easier management of GFW data

#### Dependencies

**3rd party Python Extentions:**
arcpy, configobj


**Others:**
CloudBerry Drive

#### Usage

Command line
```shell
gfw-sync.py [options]

Options:
	-h, --help				Show help of GFW Sync Tool
	-v, --validate			Validate all config files before update
	-c {country ISO3 code}	Country to be updated. Update will affect all selected layers.
							If left out, all countries will be selected.
							You can use this option multiple times
	-l {GFW layer name}		GFW Layer, which will be updated. Update will affect all selected countries
							If left out, all layers will be selected.
							You can use this option multiple times
```


Python:
```python
>>> import merge_layers
>>> merge_layers.merge(['logging'],['CAN'])
```
### Script Configuration

Script is configured in config/settings.ini

You can define drive names for S3 buckets as well as target and scratch GDB


### Layer Configuration

Layers are congigured in layer folder. Each layer has its own INI file.
New INI files will be detected automatically.

Each INI files has a header with layer specific parameters. In the body, parameters for included datatsets are listed.


####Layer file header

```ini
name = {name of GFW layer}
bucket = {name of S3 bucket}
folder = {name of folder in S3 bucket}
```

####Layer file body

For each dataset the following parameters must be listed
```ini
[{in dataset name}]
country = {ISO3 code}
location = {Server of S3}
full_path = {full path on server or on S3}
where_clause = {SQL expression as used in ArcMap definition query}
transformation = {ArcGIS transformation name  
```
In addition to general parameters a field map must be provided for each dataset. For each field one of the following option can be used

```ini
[[fields]]
{out field name} = field, {in field name}
{out field name} = value, {value}
{out field name} = expression, {PYTHON expression, as used in ArcMap field calculator}
```

Strings with white spaces need to be in quotes.
If no value is given, parameter will be ignored.

#### Example

Land Rights Layer layers must follow the following schema

```ini
## GFW Land Rights Layer

name = land_rights
bucket = gfw2-data
folder = people\land_rights

## Australia

[aus_land_rights]
country = AUS
location = Server
full_path = F:\people\land_rights\aus_land_rights.shp
where_clause =
transformation = AGD_1966_To_WGS_1984  
    [[fields]]
    # country = value, AUS
    name = field, Name
    legal_term = field, Legal_Term
    legal_reco = field, Reco
    area_ha = 
    source = value, "Commonwealth of Australia (Geoscience Australia)"
    last_updat = value, 2014
	
## Brazil

[bra_land_rights]
country = BRA
location = Server
full_path = F:\people\land_rights\bra_land_rights.shp
where_clause =
transformation = SAD_1969_To_WGS_1984_14  
    [[fields]]
    # country = value, BRA
    name = field, Name
    legal_term = field, Nat_Leg_Te
    legal_reco = field, Leg_Rec
    area_ha = field, Area_ha
    source = value, "Fundação Nacional do Índio (FUNAI)"
    last_updat = value, 2014
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
