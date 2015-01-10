import arcpy
from config import settings as set

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def validate():

    # Test 1
    # Check if target DB exists

    settings = set.get_settings()
    target_db = settings['paths']['target_gdb']
    if not arcpy.Exists(target_db):
        print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "target geodatabase %s does not exists" % target_db
        print "Validate value in config/settings.ini"
        print ""
        print "Skip test 2: Validate target feature classes"
        print "Skip test 3: Validate target feature class fields"

    else:
        arcpy.env.workspace = target_db
        layer_settings = set.get_layers()

        for ls in layer_settings:
            # Test 2
            # Check if target feature classes exist

            gfw_layer = "gfw_%s" % ls['name']

            if not arcpy.Exists(gfw_layer):
                print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "feature class %s does not exist in target geodatabase" % gfw_layer
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
                    for target_field in layer['fields'].keys:
                        if not target_field in field_names:
                            print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "field %s does not exist in feature class %s" % (target_field, gfw_layer)
                            print ""



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
                    print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "unexpected location value for layer %s " % layer_name

                if len(layer['counrty']) != 3:
                    print bcolors.WARNING + "WARNING: " + bcolors.ENDC + "country code for %s is not compliant with ISO3" % layer_name

                if not arcpy.Exists(layer['full_path']):
                    print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "source feature class %s does not exist" % layer['full_path']
                else:

                    desc = arcpy.Describe(layer['full_path'])
                    from_sr = desc.spatialReference
                    to_sr = arcpy.SpatialReference('WGS 1984')
                    extent = desc.extent
                    transformations = arcpy.ListTransformations(from_sr, to_sr, extent)

                    if layer['tansformation'] != "" and not layer['tansformation'] in transformations:
                        print bcolors.WARNING + "WARNING: " + bcolors.ENDC + "transformation for %s is not comtabile with in- and output spatial reference or extent" % layer_name

                    if layer['where_clause'] != "":
                        try:
                            arcpy.MakeFeatureLayer_management(layer['full_path'], layer_name, layer['where_clause'])
                        except:
                            print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "where clause for layer %s is incorrect" % layer_name
                            print arcpy.GetMessages()

                    # Test 5
                    # Check if soure feature class fields exist

                    field_list = arcpy.ListFields(layer['full_path'])
                    field_names = []
                    for field in field_list:
                        field_names.append(field.name) #str(field.name)??

                    for f in layer['fields']:
                        if f:
                            if f[0]== 'value':
                                if len(f)!=2:
                                    print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "validate field value for %s in layer %s" % (f.key, layer_name)
                            elif f[0]== 'field':
                                if not f[1] in field_names:
                                    print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "source field %s of layer %s does not exist" % (f[1], layer_name)
                            else:
                                print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "validate field definition for %s in layer %s" % (f.key, layer_name)