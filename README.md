gfw-sync
========

Synchronization stuff for easier management of GFW data

### Dependencies

arcpy (comes with ArcGIS)

configobj # pip install configobj

BeautifulSoup  # pip install beuatifulsoup4

requests  # pip install requests

CloudBerry Drive (or similar tool to map S3 buckets as Windows drives)

### Usage

Command line
```shell
    gfw-sync.py [options]
    Options:
    -h, --help               Show help of GFW Sync Tool
    -v, --validate           Validate all config files before update
    -n, --nonverbose        Turn console messages off
    -g, --nolog             Turn logging off
    -c <country ISO3 code>   Country to be updated. Update will affect all selected layers.
                             If left out, all countries will be selected.
                             You can use this option multiple times
    -l <GFW layers name>      GFW Layer, which will be updated. Update will affect all selected countries
                             If left out, all layers will be selected.
                             You can use this option multiple times
```


### Script Configuration

Script is configured in config/settings.ini

You can define drive names for S3 buckets as well as target and scratch GDB and folders, and default projections


### Layer Configuration

Layers are configured in layer folder using ini files.
One INI file can contain one or many layers. The order doesn't matter.
New INI files will be detected automatically.

There are different layer types which are handled differently
1. Country layers
2. Simple layers
3. Merged layers
4. Custom layers



####Country Layers

Country layers (SHP files) will be zipped and archived and directly registered with ArcGIS Online.
They have the following properties:

```ini
[layer_name]
type = country
alias = Layer Name
bucket = gfw2-data
folder = country\ISO3
shapefile = country_shapefile.shp
```

####Simple Layers

Simple Layers are imported into a GDB and served as web services. Original SHP files will also be zipped and archived.
They have the follwing properties

```ini
[layer_name]
type = simple
alias = Layer Name
bucket = gfw2-data
folder = country\ISO3
shapefile = simple_shapefile.shp
gdb = name_of_gdb.gdb
```

####Merged Layers

Merged Layers are a product of several country layers. Country layers are merged into one global layer,
imported into a GDB and served as web services. Original input SHP files as well as new output SHP files will be zipped and archived.
They have the follwing properties

```ini
[layer_name]
type = simple
alias = Layer Name
bucket = gfw2-data
folder = country\ISO3
shapefile = simple_shapefile.shp
gdb = name_of_gdb.gdb
keywords = keyword1, keword2, keyword3

[[layers]]

## First country layer

[[[country_layer1]]]
country = ISO3 code
alias = Layer Name 1
shapefile = coutry_shapefile1.shp
where_clause = '"FIELD" = 1'  # SQL expression
transformation = ARCGIS_TRANSFORMATION_NAME
    [[[[fields]]]]
    field_name1 = field, Name
    field_name2 = value, Field Value
    field_name3 = expression, !field1! * !field2!
    ...


## Second country layer

[[[country_layer2]]]
country = ISO3 code
alias = Layer Name 2
shapefile = coutry_shapefile2.shp
where_clause = '"FIELD" = 2'  # SQL expression
transformation = ARCGIS_TRANSFORMATION_NAME
    [[[[fields]]]]
    field_name1 = field, Name
    field_name2 = value, Field Value
    field_name3 = expression, !field1! * !field2!
    ...

...

```


####Custom Layers

Custom layers don't follow any of the above workflows and need to be handled differently. They will have their own procedures.
Properties might vary, but they will need to have at least a name, type and alias.

```ini
[layer_name]
type = custom1
alias = Layer Name
prob1 = Property 1
prob2 = Property 2
...
```