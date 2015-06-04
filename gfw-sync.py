import sys
import getopt

import merge_layers
import settings
import validate_ini


def main(argv):
    set = settings.get_settings()
    print "%s v%s" % (set['tool_info']['name'], set['tool_info']['version'])
    print ""

    layers = []
    countries = []
    validate = False
    verbose = True
    logging = True
    try:
        opts, args = getopt.getopt(argv, "hvl:c:", ["help", "validate", "layers=", "country="])
    except getopt.GetoptError:
        print "Error: Invalide argument"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        #elif opt == "-d":
        #    global _debug
        #    _debug = 1
        if opt in ("-v", "--validate"):
            validate = True
        if opt in ("-n", "--nonverbose"):
            verbose = False
        if opt in ("-g", "--nolog"):
            logging = False
        if opt in ("-l", "--layers"):
            layers.append(arg.lower())
        if opt in ("-c", "--country"):
            countries.append(arg.upper())
               
    if not len(layers):
        #print len(layers)
        layers = settings.get_layer_list()
        print layers

    if validate:
        validate_ini.validate(layers, countries, verbose, logging)
        input_var = raw_input("Do you want to continue (Y/N): ")
        if input_var[0].lower() != 'y':
                sys.exit()

    merge_layers.merge(layers, countries)


def usage():
    layers = settings.get_layer_list()

    print "Usage: gfw-sync.py [options]"
    print "Options:"
    print "-h, --help               Show help of GFW Sync Tool"
    print "-v, --validate           Validate all config files before update"
    print "-n, --nonverbose        Turn console messages off"
    print "-g, --nolog             Turn logging off"
    print "-c <country ISO3 code>   Country to be updated. Update will affect all selected layers."
    print "                         If left out, all countries will be selected."
    print "                         You can use this option multiple times"
    print "-l <GFW layers name>      GFW Layer, which will be updated. Update will affect all selected countries"
    print "                         If left out, all layers will be selected."
    print "                         You can use this option multiple times"
    print "                         Currently supported layers:"
    for layer in layers:
        print "                             %s" % layer




if __name__ == "__main__":

    main(sys.argv[1:])

