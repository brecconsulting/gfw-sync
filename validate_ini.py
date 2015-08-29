import os
import arcpy
import settings
import logging

from configobj import ConfigObj
from configobj import ConfigObjError

from validate import Validator
from validate import ValidateError

import time
import datetime


def log_info(msg, l, v):
    if l:
        logging.info(msg)
    if v:
        print "%s" % msg
        

def log_msg(msg, msg_type, l, v):
    if l:
        if msg_type == "i":
            logging.info(msg)
        if msg_type == "w":
            logging.warning(msg)
        if msg_type == "e":
            logging.error(msg)
    if v:
        if msg_type == "i":
            print "[VALID] %s" % msg
        if msg_type == "w":
            print "[WARNING] %s" % msg
        if msg_type == "e":
            print "[FAILED] %s" % msg
            

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


def validate_bucket(bucket, bucket_drives, l=True, v=True):
    bucket_drive = False
    for key in bucket_drives.keys():
        if key == bucket:
            bucket_drive = bucket_drives[key]
            log_msg("bucket drive %s" % bucket, "i", l, v)
            #print "[VALID] bucket drive %s" % bucket
    if not bucket_drive:
        log_msg("bucket drive %s: No drive assigned" % bucket, "e", l, v)
        #print "[FAILED} bucket drive %s: No drive assigned" % bucket
    return bucket_drive


def validate_folder(folder, l=True, v=True):
    if os.path.exists(folder):
        log_msg("folder %s" % folder, "i", l, v)
        #print "[VALID] folder %s" % folder
        return folder
    else:
        log_msg("folder %s: does not exist" % folder, "e", l, v)
        #print "[FAILED] folder %s: does not exist" % folder
        return False


def validate_shapefile(shp, l=True, v=True):
    if arcpy.Exists(shp):
        desc = arcpy.Describe(shp)
        if not desc.dataType == 'ShapeFile':
            log_msg("shapefile %s: is not a Shapefile" % shp, "e", l, v)
            #print "[FAILED] shapefile %s: is not a Shapefile" % shp
            return False
        else:
            log_msg("shapefile %s" % shp, "i", l, v)
            #print "[VALID] shapefile %s" % shp
            return shp
    else:
        log_msg("shapefile %s: does not exist" % shp, "e", l, v)
        #print "[FAILED] shapefile %s: does not exist" % shp
        return False


def validate_gdb(gdb, l=True, v=True):

    if arcpy.Exists(gdb):
        desc = arcpy.Describe(gdb)
        print desc.dataType
        print desc.workspaceFactoryProgID
        if not desc.workspaceFactoryProgID == 'esriDataSourcesGDB.FileGDBWorkspaceFactory.1':
            log_msg("gdb %s: is not a fileGDB" % gdb, "e", l, v)
            #print "[FAILED] gdb %s: is not a fileGDB" % gdb
            return False
        else:
            log_msg("gdb %s" % gdb, "i", l, v)
            #print "[VALID] gdb %s" % gdb
            return gdb
    else:
        log_msg("gdb %s: does not exist" % gdb, "e", l, v)
        #print "[FAILED] gdb %s: does not exist" % gdb
        return False


def validate_feature_class(fc, l=True, v=True):
    if arcpy.Exists(fc):
        desc = arcpy.Describe(fc)
        if not desc.dataType == 'FeatureClass':
            log_msg("feature class %s: is not a Feature Class" % fc, "e", l, v)
            #print "[FAILED] feature class %s: is not a Feature Class" % fc
            return False
        else:
            log_msg("feature class %s" % fc, "i", l, v)
            #print "[VALID] feature class %s" % fc
            return fc
    else:
        log_msg("feature class %s: does not exist" % fc, "e", l, v)
        #print "[FAILED] feature class %s: does not exist" % fc
        return False


def validate_where(fc, where, l=True, v=True):
    try:
        arcpy.MakeFeatureLayer_management(fc, where)
        log_msg("where clause %s" % where, "i", l, v)
        #print "[VALID] where clause %s" % where
    except:
        log_msg("where clause %s: is invalide" % where, "e", l, v)
        #print "[FAILED] where clause %s: is invalide" % where
        log_info(arcpy.GetMessages(), l, v)
        #print arcpy.GetMessages()
        return False
    return where


def validate_transformation(fc, srs, transformation, l=True, v=True):
    desc = arcpy.Describe(fc)
    from_srs = desc.spatialReference
    to_srs = arcpy.SpatialReference(srs)
    extent = desc.extent
    transformations = arcpy.ListTransformations(from_srs, to_srs, extent)

    #print layers['transformation']
    #print transformations

    if not transformation in transformations:
        log_msg("transformation %s: not compatible with in- and output spatial reference or extent" % transformation, "e", l, v)
        #print "[FAILD] transformation %s: not compatible with in- and output spatial reference or extent" % transformation
        return False
    else:
        log_msg("transformation %s" % transformation, "i", l, v)
        #print "[VALID] transformation %s" % transformation
        return transformation


def validate_srs(srs, l=True, v=True):
    try:
        arcpy.SpatialReference(srs)
        log_msg("srs %s" % srs, "i", l, v)
        #print "[VALID] srs %s" % srs
        return srs
    except:
        log_msg("srs %s: not a spatial reference system" % srs, "e", l, v)
        #print "[FAILED] srs %s: not a spatial reference system" % srs
        return False


def get_field_names(fc):
    field_list = arcpy.ListFields(fc)
    field_names = []
    for field in field_list:
        field_names.append(field.name)
    return field_names


def validate_fields(in_fc, out_fc, fields, l=True, v=True):

    in_fc_flist = get_field_names(in_fc)
    out_fc_flist = get_field_names(out_fc)

    e = 0
    for key in fields.keys():
        if key in out_fc_flist:
            if fields[key][0] == 'field':
                if not fields[key][1] in in_fc_flist:
                    log_msg("field %s: does not exist in feature class %s" % (key, in_fc), "e", l, v)
                    #print "[FAILED] field %s: does not exist in feature class %s" % (key, in_fc)
                    e += 1
                else:
                    log_msg("field %s" % key, "i", l, v)
                    #print "[VALID] field %s" % key
            elif fields[key][0] == 'value':
                if len(fields[key][1])> 255:
                    log_msg("field value for %s for feature class %s is too long" % (key, in_fc), "e", l, v)
                    #print "[FAILED] field value for %s for feature class %s is too long" % (key, in_fc)
                    e += 1
                else:
                    log_msg("field %s" % key, "i", l, v)
                    #print "[VALID] field %s" % key
            elif fields[key][0] == 'expression':
                # no test for expression at this point
                log_msg("field %s: skip test (no validation routine for expressions)" % key, "w", l, v)
                #print "[WARNING] field %s: skip test (no validation routine for expressions)" % key
            else:
                log_msg("field %s: invalide statement" % key, "e", l, v)
                #print "[FAILED] field %s: invalide statement" % key
                e += 1
        else:
            log_msg("field %s: does not exist in feature class %s" % (key, out_fc), "e", l, v)
            #print "[FAILED] field %s: does not exist in feature class %s" % (key, out_fc)
            e += 1
    if e == 0:
        return fields
    else:
        return False


def print_dic_value(d, l=True, v=True):
    errors = 0
    for key, value in d.iteritems():
        if isinstance(value, dict):
            errors = errors + print_dic_value(value)
        else:
            if value != True:
                log_msg("{0} : {1}".format(key, value), "e", l, v)
                #print "{0} : {1}".format(key, value)
                errors += 1
    return errors


def validate_structure(ini_file, configspec, l=True, v=True):

    log_info("", l, v)
    log_info("Validate file structure of %s" % ini_file, l, v)
    #print ""
    #print "Validate file structure of %s" % ini_file

    errors = 0
    warnings = 0
    
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)

    f = os.path.join(dir_name, configspec, ini_file)
    cspec = os.path.join(dir_name, 'config', configspec)

    validator = Validator({'drive': validate_drive, 'path': validate_path, 'shapefile': validate_shapefile_name, 'gdb': validate_gdb_name})

    try:
        config = ConfigObj(f, configspec=cspec)
        results = config.validate(validator, preserve_errors=True)

        if results != True:
            errors = errors + print_dic_value(results, l, v)

    except (ConfigObjError, IOError), e:
        log_msg('Could not read "%s": %s' % (f, e), "e", l, v)
        #print 'Could not read "%s": %s' % (f, e)
        errors += 1

    return errors, warnings


def validate_settings(l=True, v=True):

    log_info("", l, v)
    log_info("Validate GFW-sync settings", l, v)
    #print ""
    #print "Validate GFW-sync settings"
    
    sets = settings.get_settings()
    errors = 0
    warnings = 0
    bucket = sets['folders']['default_bucket']
    bucket_drives = sets['bucket_drives']
    bucket = validate_bucket(bucket, bucket_drives, l, v)
    if not bucket:
        errors += 1

    default_srs = sets['spatial_references']['default_srs']
    default_srs = validate_srs(default_srs, l, v)
    if not default_srs:
        errors += 1

    gdb_srs = sets['spatial_references']['gdb_srs']
    gdb_srs = validate_srs(gdb_srs, l, v)
    if not gdb_srs:
        errors += 1

    return errors, warnings


def validate_layer(ini_file, layer_name, countries, l=True, v=True):

    log_info("", l, v)
    log_info("Validate parameters of %s" % ini_file, l, v)
    #print ""
    #print "Validate parameters of %s" % ini_file
    
    errors = 0
    warnings = 0
    sets = settings.get_settings()
    layers = settings.get_layers_from_file(ini_file)

    for l in layers:

        if l == layer_name:

            log_info("", l, v)
            log_info("Layer %s" % layer_name, l, v)
            #print ""
            #print "Layer %s" % key
            layer = layers[layer_name]

            gdb = os.path.join(sets['paths']['workspace'], layer['gdb'])
            gdb = validate_gdb(gdb, l, v)

            if gdb:
                fc = os.path.join(gdb, layer_name)
                fc = validate_feature_class(fc, l, v)
                if not fc:
                    errors += 1
            else:
                log_msg("feature class %s: skipped" % layer_name, "w", l, v)
                #print "[WARNING] feature class %s: skipped" % layer_name
                fc = False
                errors += 1
                warnings += 1

            bucket_drive = validate_bucket(layer['bucket'], sets['bucket_drives'], l, v)

            if bucket_drive:
                folder = os.path.join(bucket_drive, layer['folder'])
                folder = validate_folder(folder, l, v)
                if not folder:
                    errors += 1
            else:
                log_msg("folder %s: skipped" % layer['folder'], "w", l, v)
                #print "[WARNING] folder %s: skipped" % layer['folder']
                folder = False
                errors += 1
                warnings += 1
                

            if layer['type'] == 'simple':
                if folder:
                    shp = os.path.join(folder, layer['shapefile'])
                    shp = validate_shapefile(shp, l, v)
                    if shp:
                        if layer['where_clause']:
                            where_clause = validate_where(shp, layer['where_clause'])
                            if not where_clause:
                                errors += 1
                        if layer['transformation']:
                            transformation = validate_transformation(shp, sets['spatial_references']['default_srs'], layer['transformation'], l, v)
                            if not transformation:
                                errors += 1
                    else:
                        log_msg("where clause %s: skipped" % layer['where_clause'], "w", l, v)
                        log_msg("transformation %s: skipped" % layer['transformation'], "w", l, v)
                        #print "[WARNING] where clause %s: skipped" % layer['where_clause']
                        #print "[WARNING] transformation %s: skipped" % layer['transformation']
                        errors += 1
                        warnings += 2
                else:
                    log_msg("shapefile %s: skipped" % layer['shapefile'], "w", l, v)
                    log_msg("where clause %s: skipped" % layer['where_clause'], "w", l, v)
                    log_msg("transformation %s: skipped" % layer['transformation'], "w", l, v)
                    #print "[WARNING: shapefile %s: skipped" % layer['shapefile']
                    #print "[WARNING: where clause %s: skipped" % layer['where_clause']
                    #print "[WARNING: transformation %s: skipped" % layer['transformation']
                    warnings += 3
            elif layer['type'] == 'merge':
                if folder:
                    for c_layer in layer['layers']:
                        country_layer = layer['layers'][c_layer]
                        if country_layer["country"] in countries or not len(countries):
                            log_info("", l, v)
                            log_info("Country layer %s" % c_layer, l, v)
                            #print ""
                            #print "Country layer %s" % c_layer
                            country_layer = layer['layers'][c_layer]
                            shp = os.path.join(folder, country_layer['shapefile'])
                            shp = validate_shapefile(shp, l, v)
                            if shp:
                                if country_layer['where_clause']:
                                    where_clause = validate_where(shp, country_layer['where_clause'], l, v)
                                    if not where_clause:
                                        errors += 1
                                if country_layer['transformation']:
                                    transformation = validate_transformation(shp, sets['spatial_references']['default_srs'], country_layer['transformation'], l, v)
                                    if not transformation:
                                        errors += 1

                                if fc:
                                    fields = validate_fields(shp, fc, country_layer['fields'], l, v)
                                    if not fields:
                                        errors += 1 #doesn't count all field errors
                                else:
                                    log_msg("fields: skipped", "w", l, v)
                                    #print "[WARNING] fields: skipped"
                                    warnings += 1
                            else:
                                log_msg("where clause %s: skipped" % layer['where_clause'], "w", l, v)
                                log_msg("transformation %s: skipped" % layer['transformation'], "w", l, v)
                                log_msg("fields: skipped", "w", l, v)
                                #print "[WARNING: where clause %s: skipped" % layer['where_clause']
                                #print "[WARNING: transformation %s: skipped" % layer['transformation']
                                #print "[WARNING] fields: skipped"
                                errors += 1
                                warnings += 3
                else:
                    for c_layer in layer['layers']:
                        country_layer = layer['layers'][c_layer]
                        if country_layer["country"] in countries or not len(countries): 
                            log_msg("country layer %s: skipped" % c_layer, "w", l, v)
                            #print "[WARNING] country layer %s: skipped" % c_layer
                            warnings += 1

    return errors, warnings


def validate(layers, countries, l=True, v=True):

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    log_folder = os.path.join(dir_name, "log")
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    log_name = os.path.join(log_folder, "validation_%s.log" % timestamp)
    logging.basicConfig(filename=log_name,level=logging.INFO)

    errors = 0
    warnings = 0

    e, w = validate_structure("settings.ini", "config", l, v)
    errors += e
    warnings += w

    e, w = validate_settings(l, v)
    errors += e
    warnings += w

    for layer in layers:

        ini_files = settings.get_layer_ini_files()
        for ini_file in ini_files:
            layer_def = settings.get_layers_from_file(os.path.basename(ini_file))

            if layer in layer_def:
                e, w = validate_structure(ini_file, "layers", l, v)
                errors += e
                warnings += w

                e, w = validate_layer(ini_file, layer, countries, l, v)
                errors += e
                warnings += w

    print ""
    print ""
    print "Validation ended with %i errors and %i warnings" % (errors, warnings)
    if l:
        print "See %s for details" % log_name
    print ""
    print ""


