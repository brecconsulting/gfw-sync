import sys
from config import settings
import merge_layers
import getopt


# if __name__ == '__main__':
#
#     if len(sys.argv) > 1:
#
#         for i in range(1, len(sys.argv)):
#             if sys.argv[i] in layers:
#                 print merge_layers.merge(sys.argv[i])
#             else:
#                 print "Layer %s is not listed in config/settings.py" % sys.argv[i]
#     else:
#         for layer in layers:
#             print merge_layers.merge(layer)






def main(argv):

    layers = []
    countries = []
    try:
        opts, args = getopt.getopt(argv, "hl:c:", ["help", "layer=", "country="])
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
        elif opt in ("-l", "--layer"):
            layers.append(arg)
        elif opt in ("-c", "--country"):
            countries.append(arg)

    if not len(layers):
        print len(layers)
        layers = settings.get_target_feature_classes()

    merge_layers.merge(list(set(layers)), list(set(countries)))


def usage():
    layers = settings.get_target_feature_classes()

    print "GFW SYNC v%s" % settings.get_version()
    print "Usage: gfw_sync.py [options]"
    print "Options:"
    print "-h, --help               Show help of GFW Sync Tool"
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