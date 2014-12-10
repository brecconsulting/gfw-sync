__author__ = 'thomas.maschler'

#####################
# CMR National Parks
#####################
arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.aires_protegees",selection_type="NEW_SELECTION",where_clause="type_ap = 0")
arcpy.Append_management(inputs="CMR.DBO.aires_protegees",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#,CMR.DBO.aires_protegees,class_uicn,-1,-1;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.aires_protegees,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.aires_protegees,statut_creation,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,partenariat,-1,-1;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,statut_amenagement,-1,-1;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Parc National"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""National Park"""",expression_type="VB",code_block="#")

#####################
# CMR Wildlife Reserves
#####################

arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.aires_protegees",selection_type="NEW_SELECTION",where_clause="type_ap = 1")
arcpy.Append_management(inputs="CMR.DBO.aires_protegees",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#,CMR.DBO.aires_protegees,class_uicn,-1,-1;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.aires_protegees,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.aires_protegees,statut_creation,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,partenariat,-1,-1;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Réserve de faune"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Wildlife Reserve"""",expression_type="VB",code_block="#")

#####################
# CMR Wildlife Sanctuary
#####################

arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.aires_protegees",selection_type="NEW_SELECTION",where_clause="type_ap = 2")
arcpy.Append_management(inputs="CMR.DBO.aires_protegees",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#,CMR.DBO.aires_protegees,class_uicn,-1,-1;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.aires_protegees,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.aires_protegees,statut_creation,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,partenariat,-1,-1;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Sanctuaire de faune"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Wildlife Sanctuary"""",expression_type="VB",code_block="#")

#####################
# CMR Wilderness Areas
#####################


arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.aires_protegees",selection_type="NEW_SELECTION",where_clause="type_ap = 6")
arcpy.Append_management(inputs="CMR.DBO.aires_protegees",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,nom_ap,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#,CMR.DBO.aires_protegees,class_uicn,-1,-1;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.aires_protegees,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.aires_protegees,statut_creation,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#,CMR.DBO.aires_protegees,partenariat,-1,-1;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Réserve écologique intégrale"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Wilderness Area"""",expression_type="VB",code_block="#")

#CMR Protected area attributs
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_TYPE",expression=""""National"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="GOV_TYPE",expression=""""Federal or national ministry or agency in charge"""",expression_type="VB",code_block="#")

#STATUS_YR
#Year of decree or year
arcpy.AddJoin_management(in_layer_or_view="protected_areas",in_field="NAME",join_table="CMR.DBO.aires_protegees",join_field="nom_ap",join_type="KEEP_ALL")
arcpy.CalculateField_management(in_table="protected_areas",field="protected_areas.STATUS_YR",expression="year([CMR.DBO.aires_protegees.date_avis_public]  )",expression_type="VB",code_block="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="CMR.DBO.aires_protegees.date_creation is not null")
arcpy.CalculateField_management(in_table="protected_areas",field="protected_areas.STATUS_YR",expression="year( [CMR.DBO.aires_protegees.date_creation]  )",expression_type="VB",code_block="#")
arcpy.RemoveJoin_management(in_layer_or_view="protected_areas",join_name="CMR.DBO.aires_protegees")




#####################
# CMR Protected Forests
#####################


arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.reserve_forestier",selection_type="NEW_SELECTION",where_clause="type_reserve = 0")
arcpy.Append_management(inputs="CMR.DBO.reserve_forestier",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.reserve_forestier,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,statut_classement,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Forêt de protection"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Protected Forest"""",expression_type="VB",code_block="#")


#####################
# CMR Research Forests
#####################


arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.reserve_forestier",selection_type="NEW_SELECTION",where_clause="type_reserve = 3")
arcpy.Append_management(inputs="CMR.DBO.reserve_forestier",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.reserve_forestier,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,statut_classement,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Forêt d'enseignement et de recherche"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Research forest"""",expression_type="VB",code_block="#")


#####################
# CMR Flora Sanctuaries
#####################

arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.reserve_forestier",selection_type="NEW_SELECTION",where_clause="type_reserve = 4")
arcpy.Append_management(inputs="CMR.DBO.reserve_forestier",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.reserve_forestier,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,statut_classement,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Sanctuaire de flore"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Flora Sanctuary"""",expression_type="VB",code_block="#")


#####################
# CMR Reforested Areas
#####################

arcpy.SelectLayerByAttribute_management(in_layer_or_view="CMR.DBO.reserve_forestier",selection_type="NEW_SELECTION",where_clause="type_reserve = 6")
arcpy.Append_management(inputs="CMR.DBO.reserve_forestier",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,nom_reserve,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.reserve_forestier,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#,CMR.DBO.reserve_forestier,statut_classement,-1,-1;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Périmètre de reboisement"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Reforested Area"""",expression_type="VB",code_block="#")

#CMR Reserve attributs
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_TYPE",expression=""""National"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="GOV_TYPE",expression=""""Federal or national ministry or agency in charge"""",expression_type="VB",code_block="#")

####################
#STATUS_YR Reserves

arcpy.AddJoin_management(in_layer_or_view="protected_areas",in_field="NAME",join_table="CMR.DBO.reserve_forestier",join_field="nom_reserve",join_type="KEEP_ALL")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="CMR.DBO.reserve_forestier.date_classement IS NOT NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="protected_areas.STATUS_YR",expression="year( [CMR.DBO.reserve_forestier.date_classement] )",expression_type="VB",code_block="#")
arcpy.RemoveJoin_management(in_layer_or_view="protected_areas",join_name="CMR.DBO.reserve_forestier")

#####################
# CMR RAMSAR Sites
#####################

arcpy.Append_management(inputs="CMR.DBO.sites_ramsar",target="protected_areas",schema_type="NO_TEST",field_mapping="""WDPAID "WDPAID" true true false 4 Long 0 0 ,First,#;WDPA_PID "WDPA_PID" true true false 4 Long 0 0 ,First,#;NAME "NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.sites_ramsar,nom_ramsar,-1,-1;ORIG_NAME "ORIG_NAME" true true false 254 Text 0 0 ,First,#,CMR.DBO.sites_ramsar,nom_ramsar,-1,-1;SUB_LOC "SUB_LOC" true true false 100 Text 0 0 ,First,#;DESIG "DESIG" true true false 254 Text 0 0 ,First,#;DESIG_ENG "DESIG_ENG" true true false 254 Text 0 0 ,First,#;DESIG_TYPE "DESIG_TYPE" true true false 20 Text 0 0 ,First,#;IUCN_CAT "IUCN_CAT" true true false 20 Text 0 0 ,First,#;INT_CRIT "INT_CRIT" true true false 100 Text 0 0 ,First,#;MARINE "MARINE" true true false 20 Text 0 0 ,First,#;REP_M_AREA "REP_M_AREA" true true false 8 Double 0 0 ,First,#;GIS_M_AREA "GIS_M_AREA" true true false 8 Double 0 0 ,First,#;REP_AREA "REP_AREA" true true false 8 Double 0 0 ,First,#,CMR.DBO.sites_ramsar,superficie_admin,-1,-1;GIS_AREA "GIS_AREA" true true false 8 Double 0 0 ,First,#;STATUS "STATUS" true true false 100 Text 0 0 ,First,#;STATUS_YR "STATUS_YR" true true false 4 Long 0 0 ,First,#;GOV_TYPE "GOV_TYPE" true true false 254 Text 0 0 ,First,#;MANG_AUTH "MANG_AUTH" true true false 254 Text 0 0 ,First,#;MANG_PLAN "MANG_PLAN" true true false 254 Text 0 0 ,First,#;NO_TAKE "NO_TAKE" true true false 50 Text 0 0 ,First,#;NO_TK_AREA "NO_TK_AREA" true true false 8 Double 0 0 ,First,#;METADATAID "METADATAID" true true false 4 Long 0 0 ,First,#;PARENT_ISO3 "PARENT_ISO3" true true false 50 Text 0 0 ,First,#;ISO3 "ISO3" true true false 50 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#""",subtype="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="DESIG IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG",expression=""""Zone humide d’importance internationale (Ramsar)"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_ENG",expression=""""Ramsar Site, Wetland of International Importance"""",expression_type="VB",code_block="#")

arcpy.CalculateField_management(in_table="protected_areas",field="DESIG_TYPE",expression=""""International"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="STATUS",expression=""""Designated"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="GOV_TYPE",expression=""""Not Reported"""",expression_type="VB",code_block="#")

arcpy.AddJoin_management(in_layer_or_view="protected_areas",in_field="NAME",join_table="CMR.DBO.sites_ramsar",join_field="nom_ramsar",join_type="KEEP_ALL")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="CMR.DBO.sites_ramsar.date_designation IS NOT null")
arcpy.CalculateField_management(in_table="protected_areas",field="protected_areas.STATUS_YR",expression="year( [CMR.DBO.sites_ramsar.date_designation] )",expression_type="VB",code_block="#")
arcpy.RemoveJoin_management(in_layer_or_view="protected_areas",join_name="CMR.DBO.sites_ramsar")


#####################
#CMR Everything Else


#Filter actual marine areas!
arcpy.CalculateField_management(in_table="protected_areas",field="MARINE",expression="0",expression_type="VB",code_block="#")
#Filter actual marine areas!
arcpy.CalculateField_management(in_table="protected_areas",field="REP_M_AREA",expression="0",expression_type="VB",code_block="#")
#Filter actual marine areas!
arcpy.CalculateField_management(in_table="protected_areas",field="NO_TAKE",expression=""""Not Applicable"""",expression_type="VB",code_block="#")
#Filter actual marine areas!
arcpy.CalculateField_management(in_table="protected_areas",field="NO_TK_AREA",expression="0",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="PARENT_ISO3",expression=""""CMR"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="ISO3",expression=""""CMR"""",expression_type="VB",code_block="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="STATUS = 'cree'")
arcpy.CalculateField_management(in_table="protected_areas",field="STATUS",expression=""""Designated"""",expression_type="VB",code_block="#")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="STATUS = 'prop' OR STATUS = 'en_cours'")
arcpy.CalculateField_management(in_table="protected_areas",field="STATUS",expression=""""Proposed"""",expression_type="VB",code_block="#")
#Find out link to Management plans (PDF)
arcpy.CalculateField_management(in_table="protected_areas",field="MANG_PLAN",expression=""""Not Reported"""",expression_type="VB",code_block="#")
#Convert hectare to km2
arcpy.CalculateField_management(in_table="protected_areas",field="REP_AREA",expression="[REP_AREA]/100",expression_type="VB",code_block="#")


#Empty Names
arcpy.SelectLayerByAttribute_management(in_layer_or_view="protected_areas",selection_type="NEW_SELECTION",where_clause="ORIG_NAME = ' ' OR ORIG_NAME IS NULL")
arcpy.CalculateField_management(in_table="protected_areas",field="ORIG_NAME",expression=""""Not Reported"""",expression_type="VB",code_block="#")
arcpy.CalculateField_management(in_table="protected_areas",field="NAME",expression="Null",expression_type="VB",code_block="#")

#SUB_LOC
#Intersect with regions








