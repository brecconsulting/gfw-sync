import json
import gspread
import arcpy_metadata as md
from oauth2client.client import SignedJwtAssertionCredentials
from sys import argv

#prompt for name and path of dataset in Amazon S3
script, filename, filepath = argv

#specify oauth2client credentials 
json_key = json.load(open('spreadsheet.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

#authorize oauth2client credentials 
gc = gspread.authorize(credentials)

#open the metadata entry spreadsheet 
wks = gc.open("GFW Metadata Entry Form (Responses)").sheet1

#determine row value based on technical name 
print "searching for %s in metadata spreadsheet" %(filename)
cell = wks.find(filename)
print "file is in row %d" %cell.row

#define metadata variables that correspond to cells in the metadata spreadsheet 
title = wks.cell(cell.row, 2).value 
translated_title = wks.cell(cell.row, 3).value
function = wks.cell(cell.row, 5).value
overview = wks.cell(cell.row, 6).value
translated_overview = wks.cell(cell.row, 7).value
category = wks.cell(cell.row, 10).value
tags = wks.cell(cell.row, 11).value
geographic_coverage = wks.cell(cell.row, 12).value
date_of_content = wks.cell(cell.row, 13).value
update_frequency = wks.cell(cell.row, 17).value 
credits = wks.cell(cell.row, 18).value
citation = wks.cell(cell.row, 19).value
license = wks.cell(cell.row, 21).value
cautions = wks.cell(cell.row, 23).value
source = wks.cell(cell.row, 24).value

#Let script know the path to the dataset that needs metadata 
metadata = md.MetadataEditor(filepath)

#write metadata from spreadsheet to .xml file
metadata.title.set(title)
metadata.abstract.set(overview)
metadata.purpose.set(function)
metadata.tags.set(tags)
metadata.place_keywords.set(geographic_coverage)
metadata.temporal_extent_description.set(date_of_content)
metadata.update_frequency.set(update_frequency)
metadata.credits.set(credits)
metadata.citation.set(citation)
metadata.limitation.set(cautions)
metadata.source.set(source)
metadata.finish()
print "metadata written from spreadsheet to xml"




