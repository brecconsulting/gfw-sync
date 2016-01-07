import urllib
import subprocess
import os


def get_auth_key():
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    token_file = os.path.join(dir_name, r"config\cartodb_token.txt")
    with open(token_file, "r") as f:
        for row in f:
            return row

def cartodb_sql(sql):
    key = get_auth_key()
    return urllib.urlopen("http://wri-01.cartodb.com:80/api/v2/sql?api_key=%s&q=%s" % (key, sql))

    
def cartodb_push(file_name):
    key = get_auth_key()
    subprocess.call([r'C:\Program Files\GDAL\ogr2ogr.exe',
                    '--config', 'CARTODB_API_KEY', key,
                    #'-append',
                    '-progress', '-skipfailures',
                    '-t_srs', 'EPSG:4326',
                    '-f', 'CartoDB',
                    'CartoDB:wri-01', file_name])



def update_cartodb(shp, production_table):

    basename = os.path.basename(shp)
    staging_table = os.path.splitext(basename)[0]

    #print "truncate staging"
    #sql= 'TRUNCATE %s' % staging_table
    #cartodb_sql(sql)

    print "upload data"
    cartodb_push(shp)
    
    print "repair geometry"
    sql = 'UPDATE %s SET the_geom = ST_MakeValid(the_geom), the_geom_webmercator = ST_MakeValid(the_geom_webmercator) WHERE ST_IsValid(the_geom) = false' % staging_table
    cartodb_sql(sql)

    print "push to production"
    sql= 'TRUNCATE %s; INSERT INTO %s SELECT * FROM %s; COMMIT' % (production_table, production_table, staging_table)
    cartodb_sql(sql)

    print "delete staging"
    sql= 'DROP TABLE IF EXISTS %s CASCADE' % staging_table
    cartodb_sql(sql)

if __name__ == "__main__":
    update_cartodb(r'C:\Users\Thomas.Maschler\Desktop\imazon_sad\imazon_sad_copy2.shp', 'imazon_sad_copy')
