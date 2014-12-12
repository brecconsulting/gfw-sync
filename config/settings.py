import glob
import os
from configobj import ConfigObj



def get_settings():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    settings = ConfigObj("settings.ini")

    return settings

def get_layers():

    os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'layers')))

    layers = []

    for file in glob.glob("*.ini"):
        layers.append(ConfigObj(file))

    return layers

def get_layerlist():

    os.chdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'layers')))

    layers = []

    for file in glob.glob("*.ini"):
        layer = ConfigObj(file)
        layers.append(layer['name'])

    return layers

