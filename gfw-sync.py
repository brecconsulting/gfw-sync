import sys
from config import settings
import merge_layers
import validate
import getopt

def main(argv):

    layers = []
    countries = []
    try:
        opts, args = getopt.getopt(argv, "hvl:c:", ["help", "validate", "layer=", "country="])
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
            validate.validate()
            input_var = raw_input("Do you want to continue (Y/N): ")
            if input_var[0].lower() != 'y':
                sys.exit()
        elif opt in ("-l", "--layer"):
            layers.append(arg.lower())
        elif opt in ("-c", "--country"):
            countries.append(arg.upper())

    if not len(layers):
        print len(layers)
        layers = settings.get_layerlist()

    merge_layers.merge(list(set(layers)), list(set(countries)))


def usage():
    layers = settings.get_layerlist()
    set = settings.get_settings()

    print "%s v%s" % (set['name'], set['version'])
    print "Usage: gfw_sync.py [options]"
    print "Options:"
    print "-h, --help               Show help of GFW Sync Tool"
    print "-v, --validate           Validate all config files before update"
    print "-c <country ISO3 code>   Country to be updated. Update will affect all selected layers."
    print "                         If left out, all countries will be selected."
    print "                         You can use this option multiple times"
    print "-l <GFW layer name>      GFW Layer, which will be updated. Update will affect all selected countries"
    print "                         If left out, all layers will be selected."
    print "                         You can use this option multiple times"
    print "                         Currently supported layers:"
    for layer in layers:
        print "                             %s" % layer




if __name__ == "__main__":

    main(sys.argv[1:])

