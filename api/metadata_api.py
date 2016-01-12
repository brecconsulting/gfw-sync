#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging

import os
import json
import sys
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
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
    md["Title"] = wks.cell(row, 3).value
    md["Translated_Title"] = wks.cell(row, 14).value
    md["Function"] = wks.cell(row, 4).value
    md["Overview"] = wks.cell(row, 12).value
    md["Translated Overview"] = wks.cell(row, 16).value
    #md["category"] = wks.cell(row, 10).value
    md["Tags"] = wks.cell(row, 17).value #.value.split(", ")
    md["Geographic Coverage"] = wks.cell(row, 6).value
    md["Date of Content"] = wks.cell(row, 9).value
    md["Frequency of Updates"] = wks.cell(row, 8).value
    #md["credits"] = wks.cell(row, 18).value
    md["Citation"] = wks.cell(row, 13).value
    md["License"] = wks.cell(row, 11).value
    md["Cautions"] = wks.cell(row, 10).value
    md["Source"] = wks.cell(row, 7).value
    md["Resolution"] = wks.cell(row, 5).value

    return md


def rebuild_cache(f):

    wks = open_spreadsheet()
    layers = get_layer_names(wks)
    md = {}
    i = 1
    for layer in layers:
        i += 1
        md[layer] = get_metadata(wks, i)

    with open(f, 'w') as cache:
        cache.write(json.dumps(md, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf8'))

def print_json():


    abspath = os.path.abspath(__file__)
    dir_name = os.path.dirname(abspath)
    cache_file = os.path.join(dir_name, 'cache.json')
    
    with open(cache_file) as cache:
        data=cache.read()

    cache = json.loads(data)

    if len(sys.argv) < 2:
        print cache

    else:

        print "Content-Type: application/json"
        print

        #if len(sys.argv) > 2:
        #	args = sys.argv[2].split('&')
        #	for arg in args:
        #		pass

        if sys.argv[1] == 'rebuild_cache':
            rebuild_cache(cache_file)
            cache = json.load(open(cache_file))
            print byteify(cache)

        elif os.path.dirname(sys.argv[1]) == dir_name:
            print byteify(cache)

        elif os.path.dirname(sys.argv[1]) == r'%s\metadata' % dir_name:
            layer = os.path.basename(sys.argv[1])
            if layer == 'rebuild_cache':
                rebuild_cache(cache_file)
                cache = json.load(open(cache_file))
                print byteify(cache)

            elif layer in cache.keys():
                print byteify(cache[layer])
            else:
                print {"error": "Layer %s unknown" % layer}
        else:
            print {"error": "wrong argument"}


print_json()
