import glob
import os
from configobj import ConfigObj



def get_settings():
    '''
    Read setting.ini and returns config
    '''
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    ini_file = os.path.join(dir_name, 'config', 'settings.ini')
    settings = ConfigObj(ini_file)

    return settings

def get_layers_from_file(file):
    '''

    '''

    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    ini_file = os.path.join(dir_name, 'layers', file)
    layers = ConfigObj(ini_file)

    return layers

def get_layers():
    '''

    '''

    os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'layers')))

    layers = []

    for file in glob.glob("*.ini"):
        layers.append(ConfigObj(file))

    return layers

def get_layer_list():

    layers = get_layers()
    layer_list = []
    for layer in layers:
        layer_list.append(layer.keys()[0])

    return layer_list

