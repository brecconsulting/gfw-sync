import arcpy
from config import settings as set


def validate():

    # Test 1
    # Check if target DB exists

    warnings = 0
    errors = 0

    settings = set.get_settings()
    target_db = settings['paths']['target_gdb']
    if not arcpy.Exists(target_db):
        print "ERROR: target geodatabase %s does not exists" % target_db
        print "Validate value in config/settings.ini"
        print ""
        print "Skip test 2: Validate target feature classes"
        print "Skip test 3: Validate target feature class fields"

        errors += 1

    else:
        arcpy.env.workspace = target_db
        layer_settings = set.get_layers()

        for ls in layer_settings:
            # Test 2
            # Check if target feature classes exist

            gfw_layer = "gfw_%s" % ls['name']

            ########
            #Still need a test here to check if bucket for layer is linked to a Drive (setting) and that folder exists on S3
           ############ 

            if not arcpy.Exists(gfw_layer):
                print "ERROR: feature class %s does not exist in target geodatabase" % gfw_layer
                print "Create feature class or validate spelling"
                print "Skip test 3: Validate target feature class fields for %s" % gfw_layer
                print ""

            else:
                # Test 3
                # Check if target feature class fields exists

                field_list = arcpy.ListFields(gfw_layer)
                field_names = []
                for field in field_list:
                    field_names.append(field.name) #str(field.name)??

                layers = []
                for key in ls.keys():
                    if key != 'name' and key != 'bucket' and key != 'folder':
                        layers.append(ls[key])

                for layer in layers:
                    for target_field in layer['fields'].keys():
                        if not target_field in field_names:
                            print "ERROR: field %s does not exist in feature class %s" % (target_field, gfw_layer)
                            print ""
                            errors += 1


            # Test 4
            # Check if source feature classes exists

            layers = []
            for key in ls.keys():
                if key != 'name' and key != 'bucket' and key != 'folder':
                    layers.append([ls[key],key])

            for ldef in layers:
                layer = ldef[0]
                layer_name = ldef[1]

                if not (layer['location'].lower() in ['server']):
                    print "ERROR: unexpected location value for layer %s " % layer_name
                    errors += 1
                    
                if len(layer['country']) != 3:
                    print "WARNING: country code for %s is not compliant with ISO3" % layer_name
                    warnings += 1
                if not arcpy.Exists(layer['full_path']):
                    print "ERROR: source feature class %s does not exist" % layer['full_path']
                    errors += 1
                    
                else:
                    if layer['transformation']:
                        desc = arcpy.Describe(layer['full_path'])
                        from_sr = desc.spatialReference
                        to_sr = arcpy.SpatialReference('WGS 1984')
                        extent = desc.extent
                        transformations = arcpy.ListTransformations(from_sr, to_sr, extent)
    
                        #print layer['transformation']
                        #print transformations

                        if not layer['transformation'] in transformations:
                            print "WARNING: transformation for %s is not comtabile with in- and output spatial reference or extent" % layer_name
                            warnings += 1
                    if layer['where_clause']:
                        try:
                            arcpy.MakeFeatureLayer_management(layer['full_path'], layer_name, layer['where_clause'])
                        except:
                            print "ERROR: where clause for layer %s is incorrect" % layer_name
                            errors += 1
                            
                            print arcpy.GetMessages()

                    # Test 5
                    # Check if soure feature class fields exist

                    field_list = arcpy.ListFields(layer['full_path'])
                    field_names = []
                    for field in field_list:
                        field_names.append(field.name) #str(field.name)??

                    for key in layer['fields'].keys():
                        f = layer['fields'][key]
                        if f:
                            if f[0]== 'value':
                                if len(f)!=2:
                                    print "ERROR: validate field value for %s in layer %s" % (key, layer_name)
                                    errors += 1
                            elif f[0]== 'field':
                                if not f[1] in field_names:
                                    print "ERROR: source field %s of layer %s does not exist" % (f[1], layer_name)
                                    errors += 1
                            else:
                                print "ERROR: validate field definition for %s in layer %s" % (key, layer_name)
                                errors += 1

    print ""
    print "Finished validation with %i error(s) and %i warning(s)" % (errors, warnings)
