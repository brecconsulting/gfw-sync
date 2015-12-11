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

table = 'imazon_sad_copy2'
folder = r'C:\Users\Thomas.Maschler\Desktop\imazon_sad'
shp = os.path.join(folder, "%s.shp" % table)

key= get_auth_key()
sql= 'TRUNCATE %s' % table

print "truncate"
print urllib.urlopen("http://wri-01.cartodb.com:80/api/v2/sql?api_key=%s&q=%s" % (key, sql))

print "append"
subprocess.call([r'C:\Program Files\GDAL\ogr2ogr.exe',
                '--config', 'CARTODB_API_KEY', key,
                 '-append', '-progress', '-skipfailures',
                '-t_srs', 'EPSG:4326',
                '-f', 'CartoDB',
                'CartoDB:wri-01', shp])

sql = 'UPDATE %s SET the_geom = ST_MakeValid(the_geom), the_geom_webmercator = ST_MakeValid(the_geom_webmercator) WHERE ST_IsValid(the_geom) = false' % table

print "repair geometry"
print urllib.urlopen("http://wri-01.cartodb.com:80/api/v2/sql?api_key=%s&q=%s" % (key, sql))

