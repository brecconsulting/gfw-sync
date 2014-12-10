def get_bucket_drive():
    bucket_drive = {
        'wri-forest-atlas': 'E:\\',
        'gfw2-data': 'F:\\',
        'gfw2_download': "G:\\"
    }
    return bucket_drive


def get_target_gdb():
    target_gdb = "D:\\GIS Data\\GFW\\GFW_data_wm.gdb"
    return target_gdb

def get_target_feature_classes():
    target_feature_classes = ["logging",
                              "land_rights"]
    return target_feature_classes

def get_scratch_folder():
    scratch_folder = "D:\\GIS Data\\GFW\\temp"
    return scratch_folder

def get_download_bucket():
    download_bucket = "gfw2_download"
    return download_bucket

def get_scratch_gdb():
    scratch_gdb = "D:\\GIS Data\\GFW\\temp\\temp.gdb"
    return scratch_gdb

def get_geojson_toolbox():
    toolbox = "D:\\scripts\\geojson-madness\\GeoJSONUtilities.pyt"
    return toolbox

def get_version():
    version = "0.1"
    return version