#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging

import os
import json
import sys
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import io
import markdown2

lkpColName_to_mdName = {'Map Service URL': u'map_service', 
                        'Title': u'title', 
                        'Source': u'source', 
                        'Other': u'other', 
                        'ArcGIS Online Item ID': u'agol_id', 
                        'Function': u'function', 
                        'SQL API': u'sql_api', 
                        'Tags': u'tags', 
                        'Translated Overview': u'translated_overview', 
                        'Link to Data in Amazon S3': u'amazon_link', 
                        'Download Data': u'download_data', 
                        'License': u'license', 
                        'Resolution': u'resolution', 
                        'Geographic Coverage': u'geographic_coverage', 
                        'Cautions': u'cautions', 
                        'Subtitle': u'subtitle', 
                        'Overview': u'overview', 
                        'Citation': u'citation', 
                        'Translated Title': u'translated_title', 
                        'Translated Function': u'translated_function', 
                        'Learn More': u'learn_more', 
                        'Frequency of Updates': u'frequency_of_updates', 
                        'Date of Content': u'date_of_content'}

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf8')
    else:
        return input

def open_spreadsheet():

    #specify oauth2client credentials
    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    spreadsheet_file = os.path.join(dir_name, 'spreadsheet.json')

    json_key = json.load(open(spreadsheet_file))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    #authorize oauth2client credentials
    gc = gspread.authorize(credentials)

    #open the metadata entry spreadsheet
    #wks = gc.open("GFW Metadata Entry Form (Responses)").sheet1
    wks = gc.open_by_key("1hJ48cMrADMEJ67L5hTQbT5hhV20YCJHpN1NwjXiC3pI").sheet1

    gdocAsLists = wks.get_all_values()

    return gdocAsLists

def gdoc_lists_to_layer_dict(inGdocAsLists):

    #Create emtpy metadata dictionary
    md = {}

    #Pull the header row from the Google doc
    headerRow = inGdocAsLists[0]

    #Iterate over the remaining data rows
    for dataRow in inGdocAsLists[1:]:

        #Build a dictionary for each row with the column title
        #as the key and the value of that row as the value
        rowAsDict = {k: v for (k, v) in zip(headerRow, dataRow)}

        #Grab the technical title (what we know the layer as)
        layerName = rowAsDict['Technical Title']

        #Add that as a key to the larger md dictionary
        md[layerName] = {}

        #For all the 
        for key, value in rowAsDict.iteritems():
            try:
                mdItemName = lkpColName_to_mdName[key]
                md[layerName][mdItemName] = value

            #If the field isn't in our metadata lookup, ignore it
            except:
                pass
            

    return md

def rebuild_cache(f):

    #Grab data from the spreadsheet in one request
    #Comes back as a list of lists
    gdocAsLists = open_spreadsheet()

    #Parse this data into layerName: {'metadata info': 'value'} format
    md = gdoc_lists_to_layer_dict(gdocAsLists)

    with io.open(f, 'w', encoding='utf8') as cache:
        cache.write(u'{')
        i = 0
        for layer in md.keys():
            if i > 0:
                cache.write(u', ')
            cache.write(u'"{0!s}": {{'.format(layer))
            j = 0
            for field in md[layer].keys():
                if j > 0:
                    cache.write(u', ')

                if field in ['title', 'translated_title', 'subtitle', 'tags', 'learn_more', 'download_data']:
                    cache.write(u'"{0!s}": "{1!s}"'.format(field, markdown2.markdown(md[layer][field], extras=["code-friendly"]).strip().replace('{', '\\{').replace('}', '\\}').replace('"', '\\"').replace(u'\n', u'<br>').replace(u'</p><br>', u'</p>').replace(u'<br><p>', u'<p>').replace(u'<p>', u'').replace(u'</p>', u'')))
                else:
                    cache.write(u'"{0!s}": "{1!s}"'.format(field, markdown2.markdown(md[layer][field], extras=["code-friendly"]).strip().replace('{', '\\{').replace('}', '\\}').replace('"', '\\"').replace(u'\n', u'<br>').replace(u'</p><br>', u'</p>').replace(u'<br><p>', u'<p>').replace(u'<p></p>', u'')))

                j += 1
            cache.write(u'}')

            i += 1
        cache.write(u'}')

    print 'done rebuild'


def print_json():

    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    cache_file = os.path.join(dir_name, 'cache.json')

    with open(cache_file) as cache:
        data = cache.read()

    udata = data.decode('utf8')

    if len(sys.argv) < 2:
        print byteify(cache)

    else:

        #Very important to set the header before printing data
        print "Content-Type: application/json; charset=utf-8\n"

        if sys.argv[1] == 'rebuild_cache':
            rebuild_cache(cache_file)
            with open(cache_file) as cache:
                data = cache.read()
            print data

        elif os.path.dirname(sys.argv[1]) == dir_name or sys.argv[1] == '{0!s}\\metadata\\'.format(dir_name):
            print data

        elif os.path.dirname(sys.argv[1]) == r'{0!s}\metadata'.format(dir_name):
            layer = os.path.basename(sys.argv[1])
            if layer == 'rebuild_cache':
                rebuild_cache(cache_file)
                with open(cache_file) as cache:
                    data = cache.read()
                print data

            else:
                if udata.find(u'"{0!s}":'.format(layer)) != -1:
                    start = udata.find(u'"{0!s}":'.format(layer)) + len(u'"{0!s}":'.format(layer))
                    end = udata[start:].find(u'}') + start + 1

                    output = udata[start:end].encode('utf8').strip()
                    print output
                else:
                    print {"error": "Layer {0!s} unknown".format(layer)}
        else:
            print {"error": "wrong argument"}


if __name__ == "__main__":
    print_json()
