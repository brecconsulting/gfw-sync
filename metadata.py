import arcpy
import xml.etree.ElementTree as ET
import os
import settings
import cgi


def get_datatype(fc):
    desc = arcpy.Describe(fc)
    return desc.dataType


def copy_metadata(fc, output):
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    xslt = os.path.join(installDir, r"Metadata\Stylesheets\gpTools\exact copy of.xslt")
    arcpy.XSLTransform_conversion(fc, xslt, output)


def export_metadata(fc, output_file, translator="FGDC"):
    #Directory containing ArcGIS Install files
    installDir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    #Path to XML schema for FGDC
    if translator == 'FGDC':
        translator = os.path.join(installDir, "Metadata/Translator/ARCGIS2FGDC.xml")
    elif translator == 'ISO':
        translator = os.path.join(installDir, "Metadata/Translator/ARCGIS2ISO19139.xml")
    #Export your metadata
    arcpy.ExportMetadata_conversion(fc, translator, output_file)


def import_metadata(input_file, fc, format="ARCGIS"):
    if format == "ARCGIS":
        import_type = "FROM_ARCGIS"
    elif format == "ESRI":
        import_type = "FROM_ESRIISO"
    elif format == "FGDC":
        import_type = "FROM_FGDC"
    elif format == "ISO":
        import_type = "FROM_ISO_19139"
    arcpy.ImportMetadata_conversion(input_file, import_type, fc)


def get_metadata_file(fc):
    data_type = get_datatype(fc)
    if data_type == "FeatureClass":
        sets = settings.get_settings()
        temp_folder = sets['paths']['scratch_workspace']
        out_file = os.path.join(temp_folder, fc + ".xml")
        copy_metadata(fc, out_file)
        return out_file

    elif data_type == "ShapeFile":
        return fc + ".xml"

def get_metadata_elements_by_key(metadata, e):
    tree = ET.parse(metadata)
    root = tree.getroot()

    elements = []

    for element in root.iter(e):
        elements.append(element.text)

    return elements


def get_metadata_element_by_etree(metadata, e_tree):
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[0] = root
    for e in e_tree:
        i += 1
        d[i] = d[i-1].find(e)
        if i == len(e_tree):
            return d[i].text

def get_metadata_elements_by_etree(metadata, e_tree):
    elements = []
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[i] = [root]
    for e in e_tree:
        i += 1
        d[i] = []
        for p in d[i-1]:
            d[i] = d[i] + p.findall(e)
        for j in range(len(d[i])):
            if i == len(e_tree):
                elements.append(d[i][j].text)
    return elements


def update_metadata_element(metadata, e_tree, e_text):
    d = {}
    tree = ET.parse(metadata)
    root = tree.getroot()
    i = 0
    d[0] = root
    for e in e_tree:
        i += 1
        d[i] = d[i-1].find(e)
        if i == len(e_tree):
            d[i].text = cgi.escape(e_text)

    tree.write(metadata)

