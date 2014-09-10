def get_bucket_drive():
    bucket_drive = {
        'wri-forest-atlas': 'E:\\',
        'gfw2-data': 'F:\\',
        'gfw2_download': "G:\\"
    }
    return bucket_drive


def get_target_gdb():
    target_gdb = "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\GFW\\GFW_data_wm.gdb"
    return target_gdb


def get_target_feature_classes():
    target_feature_classes = ["logging",
                              "mining",
                              "plantations",
                              "land_right",
                              "protected_areas",
                              "resource_rights",
                              "wood_fibre"]
    return target_feature_classes


def get_scratch_folder():
    scratch_folder = "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\GFW\\temp"
    return scratch_folder


def get_download_bucket():
    download_bucket = "gfw2_download"
    return download_bucket

def get_scratch_gdb():
    scratch_gdb = "C:\\Users\\Thomas.Maschler\\Documents\\Atlas\\test\\GFW\\temp\\temp.gdb"
    return scratch_gdb

def get_geojson_toolbox():
    toolbox = "C:\\Users\\Thomas.Maschler\\Documents\\GitHub\\geojson-madness\\GeoJSONUtilities.pyt"
    return toolbox