import arcpy
import uuid

# This function was copied from validate_ini, need to find a new place, duplicate
def get_field_names(fc):
    field_list = arcpy.ListFields(fc)
    field_names = []
    for field in field_list:
        field_names.append(field.name)
    return field_names

def add_gfwid(shp):
    field_names = get_field_names(shp)
    field_name = "gfwid"
    if not field_name in field_names:
        arcpy.AddField_management(shp, "gfwid", "TEXT", '#', '#', 36, "GFW ID")
        cur = arcpy.UpdateCursor(shp)
        for row in cur:
            row.setValue(field_name, str(uuid.uuid4()))
            cur.updateRow(row)
