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
    md[u"Title"] = wks.cell(row, 3).value
    md[u"Translated_Title"] = wks.cell(row, 14).value
    md[u"Function"] = wks.cell(row, 4).value
    md[u"Overview"] = wks.cell(row, 12).value
    md[u"Translated Overview"] = wks.cell(row, 16).value
    #md["category"] = wks.cell(row, 10).value
    md[u"Tags"] = wks.cell(row, 17).value #.value.split(", ")
    md[u"Geographic Coverage"] = wks.cell(row, 6).value
    md[u"Date of Content"] = wks.cell(row, 9).value
    md[u"Frequency of Updates"] = wks.cell(row, 8).value
    #md["credits"] = wks.cell(row, 18).value
    md[u"Citation"] = wks.cell(row, 13).value
    md[u"License"] = wks.cell(row, 11).value
    md[u"Cautions"] = wks.cell(row, 10).value
    md[u"Source"] = wks.cell(row, 7).value
    md[u"Resolution"] = wks.cell(row, 5).value

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
            cache.write(u"'%s': {" % layer)
            j = 0
            for field in md[layer].keys():
                if j > 0:
                    cache.write(u', ')
                cache.write(u"'%s': '%s'" % (field, markdown2.markdown(md[layer][field].replace("'", u"\u2019")).replace(u'\n',u'')))
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

        elif os.path.dirname(sys.argv[1]) == dir_name or sys.argv[1] == '%s\\metadata\\' % dir_name:
            print data

        elif os.path.dirname(sys.argv[1]) == r'%s\metadata' % dir_name:
            layer = os.path.basename(sys.argv[1])
            if layer == 'rebuild_cache':
                rebuild_cache(cache_file)
                print data

            else:
                if udata.find(u"'%s':" % layer) != -1:
                    start = udata.find(u"'%s':" % layer) + len(u"'%s':" % layer)
                    end = udata[start:].find(u'}') + start + 1

                    output = udata[start:end].encode('utf8').strip()
                    print output
                else:
                    print {"error": "Layer %s unknown" % layer}
        else:
            print {"error": "wrong argument"}


print_json()
