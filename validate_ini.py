import os
import arcpy
import settings

from configobj import ConfigObj
from configobj import ConfigObjError

from validate import Validator
from validate import ValidateError


def validate_path(value):
    if isinstance(value, list):
        raise ValidateError('A list was passed when a path was expected')
    if not os.path.exists(value):
        raise ValidateError('Path "%s"does not exists' % value)

    return value


def validate_drive(value):
    if isinstance(value, list):
        raise ValidateError('A list was passed when a drive was expected')
    if not (value[0].isalpha() and value[1] == ':' and value[2] == "\\"):
        raise ValidateError('Drive not in the right format')
    if len(value) != 3:
        raise ValidateError('Drive not in the right format')
    if not os.path.exists(value):
        raise ValidateError('Drive "%s"does not exists' % value)
    return value


def validate_shapefile_name(value):
    if isinstance(value, list):
        raise ValidateError('A list was passed when a shapefile was expected')
    if not value[-4:] == ".shp":
        raise ValidateError('Not a shapefile')
    return value


def validate_gdb_name(value):
    if isinstance(value, list):
        raise ValidateError('A list was passed when a gdb was expected')
    if not value[-4:] == ".gdb":
        raise ValidateError('Not a GDB')
    return value


def validate_bucket(bucket, bucket_drives):
    bucket_drive = False
    for key in bucket_drives.keys():
        if key == bucket:
            bucket_drive = bucket_drives[key]
    if not bucket_drive:
        print "No drive assigned to bucket %s" % bucket
    return bucket_drive


def validate_folder(folder):
    if os.path.exists(folder):
        return folder
    else:
        print "Folder %s does not exist" % folder
        return False


def validate_shapefile(shp):
    if arcpy.Exists(shp):
        desc = arcpy.Describe(shp)
        if not desc.dataType == 'ShapeFile':
            print "%s is not a Shapefile" % shp
            return False
        else:
            return shp
    else:
        print "Shapefile %s does not exist" % shp
        return False


def validate_gdb(gdb):

    if arcpy.Exists(gdb):
        desc = arcpy.Describe(gdb)
        if not desc.workspaceFactoryProgID == 'esriDataSourcesGDB.FileGDBWorkspaceFactory.1':
            print "%s is not a Workspace" % gdb
            return False
        else:
            return gdb
    else:
        print "GDB %s does not exist" % gdb
        return False


def validate_feature_class(fc):
    if arcpy.Exists(fc):
        desc = arcpy.Describe(fc)
        if not desc.dataType == 'FeatureClass':
            print "%s is not a Feature Class" % fc
            return False
        else:
            return fc
    else:
        print "Feature class %s does not exist" % fc
        return False


def validate_where(fc, where):
    try:
        arcpy.MakeFeatureLayer_management(fc, where)
    except:
        print "Where clause for Feature Class %s is incorrect" % fc
        print arcpy.GetMessages()
        return False
    return where


def validate_transformation(fc, srs, transformation):
    desc = arcpy.Describe(fc)
    from_srs = desc.spatialReference
    to_srs = arcpy.SpatialReference(srs)
    extent = desc.extent
    transformations = arcpy.ListTransformations(from_srs, to_srs, extent)

    #print layers['transformation']
    #print transformations

    if not transformation in transformations:
        print "Transformation %s is not compatible with in- and output spatial reference or extent for feature class %s" % (transformation, fc)
        return False
    else:
        return transformation

def validate_srs(srs):
    try:
        arcpy.SpatialReference(srs)
        return srs
    except:
        print "%s is not a spatial reference system" % srs
        return False


def get_field_names(fc):
    field_list = arcpy.ListFields(fc)
    field_names = []
    for field in field_list:
        field_names.append(field.name)
    return field_names


def validate_fields(in_fc, out_fc, fields):

    in_fc_flist = get_field_names(in_fc)
    out_fc_flist = get_field_names(out_fc)

    e = 0
    for key in fields.keys():
        if key in out_fc_flist:
            if fields[key][0] == 'field':
                if not fields[key][1] in in_fc_flist:
                    print "Field %s does not exist in Feature Class %s" % (key, in_fc)
                    e += 1
            elif fields[key][0] == 'value':
                if len(fields[key][1])> 255:
                    print "Field value for %s for feature class %s is too long" % (key, in_fc)
                    e += 1
            elif fields[key][0] == 'expression':
                pass # no test for expression at this point
            else:
                print "Invalide statement for out field %s for feature class %s" % (key, in_fc)
                e += 1
        else:
            print "Field %s does not exist in Feature Class %s" % (key, out_fc)
            e += 1
    if e == 0:
        return fields
    else:
        return False


def print_dic_value(d):
    errors = 0
    for k, v in d.iteritems():
        if isinstance(v, dict):
            errors = errors + print_dic_value(v)
        else:
            if v != True:
                print "{0} : {1}".format(k, v)
                errors += 1
    return errors


def validate(ini_file, configspec):

    errors = 0
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)

    f = os.path.join(dir_name, configspec, ini_file)
    cspec = os.path.join(dir_name, 'config', configspec)

    validator = Validator({'drive': validate_drive, 'path': validate_path, 'shapefile': validate_shapefile_name, 'gdb': validate_gdb_name})

    try:
        config = ConfigObj(f, configspec=cspec)
        results = config.validate(validator, preserve_errors=True)

        if results != True:
            errors = errors + print_dic_value(results)

    except (ConfigObjError, IOError), e:
        print 'Could not read "%s": %s' % (f, e)
        errors += 1

    return errors


def validate_settings():
    sets = settings.get_settings()
    print sets
    errors = 0
    bucket = sets['folders']['default_bucket']
    bucket_drives = sets['bucket_drives']
    bucket = validate_bucket(bucket, bucket_drives)
    if not bucket:
        errors += 1

    default_srs = sets['spatial_references']['default_srs']
    default_srs = validate_srs(default_srs)
    if not default_srs:
        errors += 1

    gdb_srs = sets['spatial_references']['gdb_srs']
    gdb_srs = validate_srs(gdb_srs)
    if not gdb_srs:
        errors += 1

    return errors


def validate_layers(ini_file):
    errors = 0
    sets = settings.get_settings()
    layers = settings.get_layers_from_file(ini_file)

    for key in layers.keys():
        layer = layers[key]

        gdb = os.path.join(sets['paths']['workspace'], layer['gdb'])
        gdb = validate_gdb(gdb)

        if gdb:
            fc = os.path.join(gdb, key)
            fc = validate_feature_class(fc)
            if not fc:
                errors += 1
        else:
            print "Skip validate feature class"
            fc = False
            errors += 1

        bucket_drive = validate_bucket(layer['bucket'], sets['bucket_drives'])

        if bucket_drive:
            folder = os.path.join(bucket_drive, layer['folder'])
            folder = validate_folder(folder)
            if not folder:
                errors += 1
        else:
            print "Skip validate folder"
            folder = False
            errors += 1

        if layer['type'] == 'simple':
            if folder:
                shp = os.path.join(folder, layer['shapefile'])
                shp = validate_shapefile(shp)
                if shp:
                    if layer['where_clause']:
                        where_clause = validate_where(shp, layer['where_clause'])
                        if not where_clause:
                            errors += 1
                    if layer['transformation']:
                        transformation = validate_transformation(shp, sets['spatial_references']['default_srs'], layer['transformation'])
                        if not transformation:
                            errors += 1
                else:
                    print "Skip validate where clause and validate transformation"
                    errors += 1
            else:
                print "Skip validate shapefile, where_clause and transformation"
        elif layer['type'] == 'merge':
            if folder:
                for country_layer in layer['layers']:

                    shp = os.path.join(folder, country_layer['shapefile'])
                    shp = validate_shapefile(shp)
                    if shp:
                        if layer['where_clause']:
                            where_clause = validate_where(shp, country_layer['where_clause'])
                            if not where_clause:
                                errors += 1
                        if layer['transformation']:
                            transformation = validate_transformation(shp, sets['spatial_references']['default_srs'], country_layer['transformation'])
                            if not transformation:
                                errors += 1

                        if fc:
                            fields = validate_fields(shp, fc, country_layer['fields'])
                            if not fields:
                                errors += 1 #doesn't count all field errors
                        else:
                            print "Skip validate fields"
                    else:
                        print "Skip validate where clause, validate transformation and validate fields"
                        errors += 1
            else:
                print "Skip validate country layers"

    return errors
