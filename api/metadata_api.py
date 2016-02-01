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

    return wks

def get_layer_names(wks):
    return wks.col_values(2)[1:]

def get_metadata(wks, row):

    #define metadata variables that correspond to cells in the metadata spreadsheet 
    md = {}
    md[u"title"] = wks.cell(row, 3).value
    md[u"translated_title"] = wks.cell(row, 14).value
    md[u"function"] = wks.cell(row, 4).value
    md[u"overview"] = wks.cell(row, 12).value
    md[u"translated_overview"] = wks.cell(row, 16).value
    #md["category"] = wks.cell(row, 10).value
    md[u"tags"] = wks.cell(row, 17).value #.value.split(", ")
    md[u"geographic_coverage"] = wks.cell(row, 6).value
    md[u"date_of_content"] = wks.cell(row, 9).value
    md[u"frequency_of_updates"] = wks.cell(row, 8).value
    #md["credits"] = wks.cell(row, 18).value
    md[u"citation"] = wks.cell(row, 13).value
    md[u"license"] = wks.cell(row, 11).value
    md[u"cautions"] = wks.cell(row, 10).value
    md[u"source"] = wks.cell(row, 7).value
    md[u"resolution"] = wks.cell(row, 5).value
    md[u"download_data"] = wks.cell(row, 20).value
    md[u"other"] = wks.cell(row, 35).value
    md[u"subtitle"] = wks.cell(row, 36).value
    md[u"translated_function"] = wks.cell(row, 15).value
    md[u"learn_more"] = wks.cell(row, 37).value

    return md


def rebuild_cache(f):

    wks = open_spreadsheet()
    layers = get_layer_names(wks)
    md = {}
    i = 1
    for layer in layers:
        i += 1
        md[layer] = get_metadata(wks, i)

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

        print "Content-Type: application/json; charset=utf-8"
        print

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



print_json()
