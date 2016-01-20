import urllib
import subprocess
import os
import json


def get_auth_key():
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    token_file = os.path.join(dir_name, r"config\cartodb_token.txt")
    with open(token_file, "r") as f:
        for row in f:
            return row

def cartodb_sql(sql, raise_error=True):
    key = get_auth_key()

    result = urllib.urlopen("http://wri-01.cartodb.com:80/api/v2/sql?api_key={0!s}&q={1!s}".format(key, sql))
    json_result = json.loads(result.readlines()[0])
    if raise_error and  "error" in json_result.keys():
        raise SyntaxError("Wrong SQL syntax.\n %s" %json_result['error'])
    return json_result


    
def cartodb_push(file_name):
    key = get_auth_key()
    result = subprocess.check_call([r'C:\Program Files\GDAL\ogr2ogr.exe',
                    '--config', 'CARTODB_API_KEY', key,
                    #'-append',
                    '-skipfailures',
                    '-t_srs', 'EPSG:4326',
                    '-f', 'CartoDB',
                    'CartoDB:wri-01', file_name], shell=True)
    if result == 0:
        raise RuntimeError("OGR2OGR threw an error")


def update_cartodb(shp, production_table):

    basename = os.path.basename(shp)
    staging_table = os.path.splitext(basename)[0]
    layerspec_table="layerspec_nuclear_hazard"
    #layerspec_table="layerspec" in production 

    #print "truncate staging"
    #sql= 'TRUNCATE %s' % staging_table
    #cartodb_sql(sql)

    print "upload data"
    cartodb_push(shp)
    
    print "repair geometry"
    sql = 'UPDATE {0!s} SET the_geom = ST_MakeValid(the_geom), the_geom_webmercator = ST_MakeValid(the_geom_webmercator) WHERE ST_IsValid(the_geom) = false'.format(staging_table)
    cartodb_sql(sql)

    print "push to production"
    sql= 'TRUNCATE {0!s}; INSERT INTO {1!s} SELECT * FROM {2!s}; COMMIT'.format(production_table, production_table, staging_table)
    cartodb_sql(sql)
    
    print "update layer spec max date"
    sql = "UPDATE {0!s} set maxdate= (SELECT max(date)+1 FROM {1!s}) WHERE table_name='{2!s}'".format(layerspec_table, production_table, production_table )
    cartodb_sql(sql)

    print "delete staging"
    sql= 'DROP TABLE IF EXISTS {0!s} CASCADE'.format(staging_table)
    cartodb_sql(sql)

if __name__ == "__main__":
    update_cartodb(r'C:\Users\Thomas.Maschler\Desktop\imazon_sad\imazon_sad_copy2.shp', 'imazon_sad_copy')
