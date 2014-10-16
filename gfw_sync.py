import sys
from config import settings
import merge_layers

layers = settings.get_target_feature_classes()

if __name__ == '__main__':

    if len(sys.argv)>1:

        for i in range(1,len(sys.argv)):
            if sys.argv[i] in layers:
                print merge_layers.merge(sys.argv[i])
            else:
                print "Layer %s is not listed in config/settings.py" % sys.argv[i]
    else:
        for layer in layers:
            print merge_layers.merge(layer)
