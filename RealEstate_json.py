from lxml import html
import xml.etree.ElementTree as ET
import requests
import urllib
import json
import csv


def recurse_dstructure(object):
	if isinstance(object, (list)):
		for loop_item in object:
			recurse_dstructure(loop_item)
	elif isinstance(object, (dict)):
		for loop_key in object.keys():
			if isinstance(object[loop_key], (dict)) or  isinstance(object[loop_key], (list)):
#				recurse_dstructure(loop_key)
				recurse_dstructure(object[loop_key])
			else:
				print loop_key, ":\t", object[loop_key]
	else:
		print object

def write_text_file(string = "", filename="pg13.txt"):
	with open(filename, "wb") as text_file:
		text_file.write(string.encode('ascii', 'ignore'))




baseURL1="https://services.realestate.com.au/services/listings/summaries/search?query={%22channel%22:%22rent%22,%22filters%22:{%22surroundingSuburbs%22:%22true%22,%22excludeTier2%22:%22true%22,%22geoPrecision%22:%22address%22,%22excludeAddressHidden%22:%22true%22},%22boundingBoxSearch%22:[-37.87925404508927,144.83564027954094,-37.75476608745239,145.0701297204589],%22pageSize%22:%221000%22}"

#page1 = requests.get(baseURL1)
#text_string1 = page1.text
#print text_string1
#top_dict1 = json.loads(text_string1)
#recurse_dstructure(top_dict1)

#baseURL2="https://services.realestate.com.au/services/listings/summaries/search?query={%22channel%22:%22rent%22,%22filters%22:{%22surroundingSuburbs%22:%22true%22,%22excludeTier2%22:%22true%22,%22geoPrecision%22:%22address%22,%22excludeAddressHidden%22:%22true%22},%22boundingBoxSearch%22:[-37.87925404508927,144.83564027954094,-37.75476608745239,145.0701297204589],%22pageSize%22:%22500%22}"
baseURL2 = "https://services.realestate.com.au/services/listings/search?query=%7B%22channel%22:%22rent%22,%22localities%22:%5B%7B%22locality%22:%22Melbourne%20City%20-%20Greater%20Region%22,%22subdivision%22:%22VIC%22,%22searchLocation%22:%22Melbourne%20City%20-%20Greater%20Region,%20VIC%22%7D%5D,%22pageSize%22:%22200%22,%22page%22:%221%22,%22filters%22:%7B%22surroundingSuburbs%22:true,%22excludeAddressHidden%22:true,%22geoPrecision%22:%22address%22%7D%7D"

#page2 = requests.get(baseURL2)
#text_string2 = page2.text
#print text_string2
#top_dict2 = json.loads(text_string2)
#recurse_dstructure(top_dict2)

baseURL3 = "https://www.realestate.com.au/rent/in-doncaster+east%2c+3109/map-1?channel=rent&source=location-search"

page3 = requests.get(baseURL3)
text_string3 = page3.text
write_text_file(text_string3)

print text_string3.encode('ascii', 'ignore')
