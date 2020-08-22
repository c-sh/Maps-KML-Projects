from lxml import html
import xml.etree.ElementTree as ET
import requests
import urllib
import json
import csv


# baseURL = "http://www.schoolcatchment.com.au/?p=9360"
baseURL = "https://bettereducation.com.au/school/Secondary/vic/vic_top_secondary_schools.aspx"

page = requests.get(baseURL)
text_string = page.text
text_string = text_string.encode('ascii', 'ignore')
tree_ = html.fromstring(text_string)
tree_.make_links_absolute(baseURL)

print text_string

print "@@@@@@"

def fill_dict(tag, attrib_dict, str_text, out_dict):
	for keys in attrib_dict.keys():
		# print keys, attrib_dict[keys]
		if tag == 'a':
			if keys == 'id' and "LinkSchool" in attrib_dict[keys]:
				# print "School = ", str_text
				out_dict["School Name"] = str_text 
				# print "School Link = ", attrib_dict['href']
				out_dict["School Link"] = attrib_dict['href']
			if keys == 'id' and "Postcode" in attrib_dict[keys]:
				# print "Postcode = ", str_text
				out_dict["Postcode"] = str_text
			if keys == 'id' and "HyperLinkOverall" in attrib_dict[keys]:
				# print "Overall Score = ", str_text
				out_dict["Overall Score"] = str_text
		
		elif tag == 'span':
			# print "ICSEA = ", str_text
			out_dict["ICSEA"] = str_text

		elif tag == 'font':
			if "overnment" in str_text:
				out_dict["Sector"] = str_text
			else:
				out_dict["Total Enrolments"] = str_text
		elif tag == 'img':
			if keys == "src" and "medal_gold" in attrib_dict[keys]:
				xstr = str(attrib_dict[keys])
				xstr = xstr[-5:-4]
				out_dict["Maths Score"] = int(xstr)
			elif keys == "src" and "book" in attrib_dict[keys]:
				xstr = str(attrib_dict[keys])
				xstr = xstr[-5:-4]
				out_dict["English Score"] = int(xstr)

		else:
			print "tag = ",tag
			print "attrib = ", attrib_dict
			print "str_text = ", str_text
			
			
			
		
# Get to leaf nodes
def leaf_nodes(list_html_elems, out_dict): 
	for x, child in enumerate(list_html_elems):
			if len(child) == 0:
				# print child.tag, child.attrib, child.text
				# fill up the dictionary
				fill_dict(child.tag, child.attrib, child.text, out_dict)
			else:
				leaf_nodes(child, out_dict)	
			
xpath_keys = '//tr'
col_keys = tree_.xpath(xpath_keys)
print len(col_keys)

value_list = []

for x, child in enumerate(col_keys):
	local_dict = {}
	if x>0: #x = 0 is th and we are only interested in td
		leaf_nodes(child, local_dict)
		if(len(local_dict) > 0):
			# print local_dict
			value_list.append(local_dict)

print len(value_list)



with open('sch__.csv', "wb") as csv_file:
	# csv_file.write(string.encode('ascii', 'ignore'))
	wr = csv.DictWriter(csv_file, fieldnames = value_list[0].keys())
	wr.writeheader()
	for x_dict in value_list:
		wr.writerow(x_dict)
