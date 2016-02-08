import urllib
import zipfile
import os
import re
import shutil
import arcpy
import archiver
import settings
import api.metadata_api as MD



def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


def get_id_list(out_table):

    cur = arcpy.SearchCursor(out_table)
    ids = list()
    for row in cur:
        ids.append(row.getValue("FEATURE_ID"))

    print "{0} gemetries to fix".format(len(ids))

    if len(ids) == 0:
        return 0, None
    elif len(ids) == 1:
        return 1, ids[0]
    else:
        i = 0
        for id in ids:
            if i == 0:
                id_list = "({0}".format(id)
                i += 1
            else:
                id_list = "{0}, {1}".format(id_list, id)

        id_list = "{0})".format(id_list)
        return 2, id_list


def repair_geometry(fc):
    arcpy.env.overwriteOutput = True
    gdb = os.path.dirname(fc)
    out_table = os.path.join(gdb, "invalid_geometries")
    #arcpy.CheckGeometry_management(fc, out_table)
    arcpy.RepairGeometry_management(fc, "DELETE_NULL")
    #
    # for i in range(5):
    #     geoms, ids = get_id_list(out_table)
    #     if geoms == 0:
    #         break
    #     elif geoms == 1:
    #         arcpy.MakeFeatureLayer_management(fc, 'fix_geoms', '"{0}" = {1}'.format(arcpy.Describe(fc).OIDFieldName, ids))
    #     else:
    #         arcpy.MakeFeatureLayer_management(fc, 'fix_geoms', '"{0}" IN {1}'.format(arcpy.Describe(fc).OIDFieldName, ids))
    #     arcpy.RepairGeometry_management("fix_geoms", "DELETE_NULL")
    #     arcpy.CheckGeometry_management("fix_geoms", out_table)


def download_wdpa(url, wdpa, path):
    sets = settings.get_settings()
    wdpa_path = os.path.join(path, "wdpa")
    if not os.path.exists(wdpa_path):
        os.mkdir(wdpa_path)
    else:
        shutil.rmtree(wdpa_path)
        os.mkdir(wdpa_path)

    zip_name = "{0!s}.zip".format(wdpa)
    zip_path = os.path.join(wdpa_path, zip_name)

    urllib.urlretrieve(url, zip_path)
    unzip(zip_path, wdpa_path)
    os.remove(zip_path)

    for root, dirs, files in os.walk(wdpa_path):
        for dir in dirs:
            if dir.endswith(".gdb"):
                return os.path.join(root, dir)


def get_wdpa_fc(src_gdb):
    arcpy.env.workspace = src_gdb
    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:

        desc = arcpy.Describe(fc)
        if desc.shapeType == 'Polygon':
            return os.path.join(src_gdb, fc)
        else:
            return None


def replace_wdpa_data(src_gdb, dst_gdb, wdpa_fc, sde_gdb):
    arcpy.env.workspace = src_gdb
    src_fc = get_wdpa_fc(src_gdb)
    if src_fc is not None:

            dst_fc = os.path.join(dst_gdb, wdpa_fc)

            ##delete all features
            arcpy.DeleteFeatures_management(dst_fc)
            #arcpy.Compress_management(sde_gdb)

            ##load new data
            arcpy.Append_management(src_fc, dst_fc, "NO_TEST")


def export_wdpa_to_shp(src, dst, simplify=True, transform=True):
    base = os.path.dirname(dst)
    simple = os.path.join(base, "simple.shp")

    sets = settings.get_settings()
    default_srs = sets["spatial_references"]["default_srs"]

    if simplify:
        # dst is a shapefile
        arcpy.SimplifyPolygon_cartography(src, simple, algorithm="POINT_REMOVE", tolerance="10 Meters",
                                          minimum_area="0 Unknown", error_option="NO_CHECK",
                                          collapsed_point_option="NO_KEEP")
    if transform:

        arcpy.Project_management(simple, dst, arcpy.SpatialReference(default_srs))

    else:
        # dst is a folder, name of shapefile will be the same as input feature class
        # arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(default_srs)
        arcpy.FeatureClassToShapefile_conversion([src], dst)


def wdpa():
    arcpy.env.overwriteOutput = True

    sets = settings.get_settings()

    url = "http://wcmc.io/wdpa_current_release"
    wdpa = "wdpa_current_release"
    path = sets["paths"]["scratch_workspace"]

    print "download"
    src_gdb = download_wdpa(url, wdpa, path)
    print src_gdb

    print "Repair geometry"
    src_fc = get_wdpa_fc(src_gdb)
    repair_geometry(src_fc)

    # src_gdb = os.path.join(path,"%s.gdb" % wdpa) #download_wdpa(url, wdpa, path)
    dst_gdb = r"D:\scripts\connections\gfw (gfw@localhost).sde\conservation"
    sde_gdb = r"D:\scripts\connections\gfw (sde@localhost).sde.sde"

    wdpa_fc = "wdpa_protected_areas"

    print "upload data"
    replace_wdpa_data(src_gdb, dst_gdb, wdpa_fc, sde_gdb)

    src = os.path.join(dst_gdb, wdpa_fc)
    dst = os.path.join(path, wdpa_fc + ".shp")

    print "export to shp"
    export_wdpa_to_shp(src, dst)

    print "archive"
    drive = sets['bucket_drives']['gfw2-data']
    layer_folder = os.path.join(drive, 'conservation')
    zip_folder = os.path.join(layer_folder, sets['folders']['zip_folder'])
    archive_folder = os.path.join(layer_folder, sets['folders']['archive_folder'])

    archiver.archive_shapefile(dst, path, zip_folder, archive_folder, True)

    print "copy shp to s3"
    s3_shp = os.path.join(layer_folder, wdpa_fc + ".shp")
    arcpy.Copy_management(dst, s3_shp)

    print "Update metadata"
    wks = MD.open_spreadsheet()
    layers = MD.get_layer_names(wks)
    i = 1
    for layer in layers:
        i += 1
        if layer == "wdpa_protected_areas":
            wks.update_cell(i, 8, 'Monthly. Current version: {0} {1}'.format(src_fc[-7:-4], src_fc[-4:]))


if __name__ == "__main__":
    wdpa()
