import json
import gspread
import arcpy_metadata as md
from oauth2client.client import SignedJwtAssertionCredentials
from sys import argv

#prompt for name and path of dataset in Amazon S3
script, filename, filepath = argv

#specify oauth2client credentials 
json_key = json.load(open('metadata_spreadsheet.json'))
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
title = wks.cell(cell.row, 3).value
function = wks.cell(cell.row, 4).value
resolution = wks.cell(cell.row, 5).value
geographic_coverage = wks.cell(cell.row, 6).value
source = wks.cell(cell.row, 7).value
update_frequency = wks.cell(cell.row, 8).value
date_of_content = wks.cell(cell.row, 9).value
cautions = wks.cell(cell.row, 10).value
license = wks.cell(cell.row, 11).value
overview = wks.cell(cell.row, 12).value
citation = wks.cell(cell.row, 13).value
translated_title = wks.cell(cell.row, 14).value
translated_function = wks.cell(cell.row, 15).value
translated_overview = wks.cell(cell.row, 16).value
tags = wks.cell(cell.row, 17).value.split(", ")
last_update = wks.cell(cell.row, 18).value
data_language = wks.cell(cell.row, 19).value
download_data = wks.cell(cell.row, 20).value
amazon_s3 = wks.cell(cell.row, 21).value
map_service = wks.cell(cell.row, 22).value
key_restrictions = wks.cell(cell.row, 23).value
wri_funded = wks.cell(cell.row, 24).value
gfw_partner = wks.cell(cell.row, 25).value
source_org = wks.cell(cell.row, 26).value
gfw_applications = wks.cell(cell.row, 27).value.split(", ")
download = wks.cell(cell.row, 28).value
analysis = wks.cell(cell.row, 29).value
scale = wks.cell(cell.row, 30).value
wms = source_org = wks.cell(cell.row, 31).value
data_updates = wks.cell(cell.row, 32).value
date_ added = wks.cell(cell.row, 33).value
why_added = wks.cell(cell.row, 34).value

#Let script know the path to the dataset that needs metadata 
metadata = md.MetadataEditor(filepath)

#write metadata from spreadsheet to .xml file
metadata.title.set(title)
metadata.purpose.set(function)
metadata.extent_description.set(geographic_coverage)
metadata.source.set(source)
metadata.update_frequency_description.set(update_frequency)
metadata.temporal_extent_description.set(date_of_content)
metadata.limitation.set(cautions)
metadata.abstract.set(overview)
metadata.citation.set(citation)
metadata.language.set(data_language)
metadata.last_update.set(last_update)

metadata.finish()

#remove then add tags 
metadata.tags.removeall()
metadata.tags.add(tags)

#add translated title and overview
metadata.locales["french"].add()
metadata.locales["french"].title.set(translated_title)
metadata.locales["french"].abstract.set(translated_overview)

print "metadata written from spreadsheet to xml"




