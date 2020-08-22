from lxml import html
import xml.etree.ElementTree as ET
import requests
import urllib
import json
import csv
import collections
import Json2kml_2

def read_text_file(filename="data39.js"):
        with open(filename, "rb") as text_file:
                string = text_file.read()
#Get rid of the trailing semi colon
                split_list = string.split(';',1)
                split_list = split_list[0].split('=',1)
        return split_list

def rec_search_key(object, input_key, input_val):
	return_object = {}
#	print "---"
	if isinstance(object, (list)):
		for loop_item in object:
			return_object = rec_search_key(loop_item, input_key, input_val)
			if len(return_object.keys()) > 0 :
				break
	elif isinstance(object, (dict)):
		for loop_key in object.keys():
			if loop_key == "name":
				if input_val in str(object[loop_key]) or str(object[loop_key]) in input_val:
#					print object[loop_key], "===", input_val
					return_object = object
					break
			else:
				return_object = rec_search_key(object[loop_key], input_key, input_val)
	else:
		return_object = {}
		#print "not list or dict = ", type(object)

	return return_object

def merge_dict(dest_dict, param_dict):
	for loop_key in param_dict.keys():
		dest_dict[loop_key] = param_dict[loop_key]


def merge_d_structures(json_dict, list_of_dicts):
#merged output should be json_dict
	for local_dict in list_of_dicts:
#Python returns the reference of the original leaf_dict
		leaf_dict = rec_search_key(json_dict, "School Name", local_dict["School Name"])
		merge_dict(leaf_dict, local_dict)
		#print leaf_dict.keys()
		#print local_dict["School Name"]

def rec_parse_types(kml_func, object):
	return_string = ""
	if isinstance(object, (list)):
		for loop_item in object:
			rec_parse_types(kml_func, loop_item)		
	elif isinstance(object, (dict)):
		str_poly_lat = []
		str_poly_lng = []
		str_description = ""
		str_extended_data = ""
		keylist = object.keys()

		for loopkey in keylist:
			if loopkey == "schools":
				rec_parse_types(kml_func, object[loopkey])
			else:
				#Create point data
				if loopkey == "zone":
					for loop_dict in object[loopkey]:
						str_poly_lat.append(loop_dict["lat"])
						str_poly_lng.append(loop_dict["lng"])
					#Create and add Bounding Rect to the citionary but do not plot it yet
					#Bounding Rect bottom left, top right coordinates
					object["boundRect"] = [(min(str_poly_lat), min(str_poly_lng) ), (max(str_poly_lat), max(str_poly_lng))]
					
				elif loopkey == "secondaryZone":
					for loop_dict in object[loopkey]:
						str_poly_lat.append(loop_dict["lat"])
						str_poly_lng.append(loop_dict["lng"])
					#Create and add Bounding Rect to the citionary but do not plot it yet
					#Bounding Rect bottom left, top right coordinates
					object["boundRect"] = [(min(str_poly_lat), min(str_poly_lng) ), (max(str_poly_lat), max(str_poly_lng))]
					# pass
				elif loopkey == "name":
					str_name = '<![CDATA[' + str(object[loopkey]) +  ']]>'
				elif loopkey == "lat":
					str_lat = str(object[loopkey])
				elif loopkey == "lng":
					str_lng = str(object[loopkey])
				else:
					str_description = str_description + "</br>" + str(loopkey) + " : " + str(object[loopkey])
					str_extended_data = str_extended_data + '\n\t<Data name="' + str(loopkey) + '">' + "<value>" + '<![CDATA[' + str(object[loopkey]) +  ']]></value>' + '</Data>\n'
#					print str(loopkey), str(object[loopkey])
#					print str_extended_data 
					
		if loopkey != "schools":
			if "Shortlist" in object.keys():
				shortlist_key_present = 1
			else:
				shortlist_key_present = 0

			if shortlist_key_present == 1 and object["Shortlist"] == "Y":
				str_type = "ShortListed School Locations"
				str_polytype = "ShortListed School Catchment Areas"
			else:
				if str(object["type"]) == "Primary":
					str_type = "Primary School Locations"
					str_polytype = "Primary School Catchment Areas"
				else: #if str(object["type"]) == "Secondary":
					str_type = "Secondary School Locations"
					str_polytype = "Secondary School Catchment Areas"
				
			kml_func.create_point(str_lat, str_lng, str_type, str_name, str_description, str_extended_data)
			kml_func.create_poly(str_poly_lat, str_poly_lng, str_polytype, str_name, str_description, str_extended_data)
			
	return return_string

def getDescription(strlink):
	prop_desc = collections.OrderedDict()
	page_desc = requests.get(strlink)
	text_desc = page_desc.text
	tree_desc = html.fromstring(text_desc)
	tree_desc.make_links_absolute(strlink)

#	print text_desc
	xpath_price = '//p[@class="priceText"]/text()'
	colname_price = tree_desc.xpath(xpath_price)
#	print strlink, "\t", colname_price
	
	prop_desc["link"] = strlink
	
	if len(colname_price) > 0:
		prop_desc["price"] = colname_price[0]
	else:
		prop_desc["price"] = "-1"
#	print "price:", colname_price

	xpath_attrname = '//dl[@class="rui-property-features rui-clearfix"]/dt/span[@class="rui-visuallyhidden"]/text()'
	colname_attrname = tree_desc.xpath(xpath_attrname)
#	print "attrname:", colname_attrname
	xpath_attrvalue = '//li[@class="property_info"]/dl[@class="rui-property-features rui-clearfix"]/dd/text()'
	colname_attrvalue = tree_desc.xpath(xpath_attrvalue)
#	print "attrvalue:", colname_attrvalue
	for index, item in enumerate(colname_attrname, start=0):
		prop_desc[item] = colname_attrvalue[index]

	xpath_type = '//span[@class="propertyType"]/text()'
	colname_type = tree_desc.xpath(xpath_type)
#	print "type:", colname_type
	if len(colname_type) > 0:
		prop_desc["type"] = colname_type[0]
	else:
		prop_desc["type"] = "Unknown"

	xpath_available = '//div[@class="available_date"]//span/text()'
	colname_available = tree_desc.xpath(xpath_available)
#	print "xpath_available:", colname_available
	if len(colname_available) > 0:
		prop_desc["availability"] = colname_available[0]
	else:
		prop_desc["availability"] = "Unknown"

	xpath_address1 = '//span[@itemprop="streetAddress"]/text()'
	xpath_address2 = '//span[@itemprop="addressLocality"]/text()'
	colname_address1 = tree_desc.xpath(xpath_address1)
	colname_address2 = tree_desc.xpath(xpath_address2)
#	print "Address:", colname_address1, colname_address2
	if len(colname_address1) > 0:
		prop_desc["address"] = colname_address1[0]
	else:
		prop_desc["address"] = "Unknown"
	
	if len(colname_address2) > 0:
		prop_desc["suburb"] = colname_address2[0]
	else:
		prop_desc["suburb"] = "Unknown"
	
#	xpath_inspection_time = '//div[@class="inspectionTimesWrapper"]//[@data-krux-event="openForInspection"]//meta[@itemprop="startDate"]/content()'
	xpath_inspection_time = '//div[@id="inspectionTimes"]//text()'
	colname_inspect = tree_desc.xpath(xpath_inspection_time)
	if len(colname_inspect) > 5:
		prop_desc["inspection_date"] = str(colname_inspect[3])
		tmp_str = str(colname_inspect[5])
		tmp_list = tmp_str.split("-")
		if len(tmp_list) > 1:
			prop_desc["inspection_time_start"] = str(tmp_list[0])
			prop_desc["inspection_time_end"] = str(tmp_list[1])
		else:
			prop_desc["inspection_time_start"] = str(tmp_list[0])
			prop_desc["inspection_time_end"] = str(tmp_list[0])
		
#		prop_desc["inspection_time"] = str(colname_inspect[5])
	else:
		prop_desc["inspection_time_start"] = "Unknown"
		prop_desc["inspection_time_end"] = "Unknown"
		
	xpath_desc_para = '//p[@class="body"]//text()'
	colname_desc_para = tree_desc.xpath(xpath_desc_para)
	str_desc_para = ""
	for _str in colname_desc_para:
		str_desc_para = str_desc_para + "\n" + _str.encode('ascii','ignore')
	prop_desc["description para"] = str_desc_para

	xpath_agent_name = '//div[@class="agentContactInfo"]//p[@class="agentName"]/text()'
	colname_agent_name = tree_desc.xpath(xpath_agent_name)
	
	for i, agent_name in enumerate(colname_agent_name, start=0):
		key1 = "Agent_Name_" + str(i)
		prop_desc[key1] = agent_name
		
	xpath_agent_phone = '//div[@class="agentContactInfo"]//li[@class="phone"]/a/text()'
	colname_agent_phone = tree_desc.xpath(xpath_agent_phone)
	for i, agent_phone in enumerate(colname_agent_phone, start=0):
		key1 = "Agent_Phone_" + str(i)
		prop_desc[key1] = agent_phone
		
	#	xpath_agent_mail = '//div[@id="agentInfoExpanded"]/*/a/img/@src'
	xpath_agent_mail = '//div/a[@class="button plusplus applyButton"]/@data-url'
	colname_agent_list = tree_desc.xpath(xpath_agent_mail)
	for i, tmp_str in enumerate(colname_agent_list, start=0):
		key1 = "Agent_Email_" + str(i)
		loop_list = tmp_str.split("&")
		for _str in loop_list:
			if "papf_realestatem" in _str:
				loop_list = tmp_str.split("=")
				break
		prop_desc[key1] = loop_list[1]
#	else:
#		print "colname_agent_list 0 for link=", strlink  
	
#	print colname_agent_name, ",\t", colname_agent_phone, ",\t", tmp_str_list
#	print "-------\n", str_desc_para
	return prop_desc

def within_sch_zone(lat, lng, tag):
#	lat = float(str_lat)
#	lng = float(str_lng)
	list_dict_zone_orig = tag["School Zone"]
	list_dict_zone = list_dict_zone_orig[:-1]
	#Nr of corners in the polygon is len(list_dict_zone)
	#use the method of ray casting of the point for each line of the polygon
	#traverse the polygon for each line 
	prev_vertice = list_dict_zone[-1]
#	print list_dict_zone
	nr_of_intersections = 0
	for curr_vertice in list_dict_zone:
		#We check for the intersection point of 2 lines
		#Line 1. prev_vertice -> curr_vertice
		#Line 2. x = lng, y = lat to x = inf., y = lat (Horizontal line)
		y = lat
		y1 = curr_vertice["lat"]
		y2 = prev_vertice["lat"]
		x = lng
		x1 = curr_vertice["lng"]
		x2 = prev_vertice["lng"]
		
#		print "y = ", lat, " x = ", lng
#		print "y1 = ", curr_vertice["lat"], " x1 = ", curr_vertice["lng"]
#		print "y2 = ", prev_vertice["lat"], " x2 = ", prev_vertice["lng"]
		T1 = prev_vertice["lat"] > lat and curr_vertice["lat"] < lat
#		print "T1 = ", T1
		T2 = prev_vertice["lat"] < lat and curr_vertice["lat"] > lat
#		print "T2 = ", T2
		
		T3 = T2 or T1
#		print "T3 = ", T3
		
		#Check if the point is within the y coords of the prev and curr vertices
		if (T1 or T2):
			# Equation of line prev to curr point => (y - y1)/(y2 - y1) = (x - x1)/(x2 - x1)
			#A point on the line prev -> curr, with fixed y coord, will have x = [(y - y1)/(y2 - y1)]*(x2 - x1) + x1 = (A/B)*C + x1
			A = (y - y1)
			B = (y2 - y1)
			C = (x2 - x1)
			D = (x - x1)
#			print "A = ", A, " B = ", B, " C = ", C, " D = ", D
			lng_on_line = (A/B)*C + x1
#			print "lng_on_line = ", lng_on_line
			if lng_on_line < lng:
				#x is on the left of the line, so a horizontal line intersects once
				nr_of_intersections = nr_of_intersections + 1
				
		prev_vertice = curr_vertice

	if nr_of_intersections % 2 == 0:
		point_in_poly = False
	else:
		point_in_poly = True
#	print "---", nr_of_intersections
	return point_in_poly

def parse_real_estate_data(kml_func, object, tag):
	str_type = "Rentals Available " + tag["price_filter"]
	loc_dict = {}
	print "parse_real_estate_data - ", object
	if isinstance(object, (list)):
		for loop_item in object:
			print "List ", loop_item
			parse_real_estate_data(kml_func, loop_item, tag)		
	elif isinstance(object, (dict)):
		keylist = object.keys()
		print "keylist ", keylist
		for loopkey in keylist:
			if loopkey == "latitude":
				str_lat = str(object[loopkey])
				loc_dict["lat"] = object[loopkey]
			elif loopkey == "listingId":
				str_link = "https://www.realestate.com.au/"
				str_link = str_link + str(object[loopkey])
				dict_desc = getDescription(str_link)
				dict_desc["Price Category"] = str_type
#				str_description = str_type
				str_Id = str(object[loopkey])
			elif loopkey == "longitude":
				#This is a leaf dict
				str_lng = str(object[loopkey])
				loc_dict["lng"] = object[loopkey]
			else: 
				print "Dict parse_real_estate_data", object
				print "Dict parse_real_estate_data", object[loopkey]
				parse_real_estate_data(kml_func, object[loopkey], tag)

		if set(['latitude', 'longitude', 'listingId']) == set(keylist):
			str_description = ""
			str_extended_data = ""
			
#			check for accuracy of the location within the school zone
			if within_sch_zone(loc_dict["lat"], loc_dict["lng"], tag):
				for keys in dict_desc.keys():
					str_keys = keys.encode('ascii','ignore')
					str_desc = dict_desc[keys]
					str_desc = str_desc.encode('ascii','ignore')
					if keys != "description para":
						str_description = str_description + str_keys + "<b>" + str_desc + "</b>" + "</br>"
						str_extended_data = str_extended_data + '\n\t<Data name="' + str_keys + '">' + "<value>" + '<![CDATA[' + str_desc + "]]></value>" + '</Data>\n'				
				addr = dict_desc["address"]
				str_addr = addr.encode('ascii','ignore')
				str_name = '<![CDATA[' + str_addr + " [" + str_link + "]" + "]]>"
#				print "IN -->", str_name
#				str_type = str(dict_desc["type"]) + "_" + str(tag["price_filter"]) + "_" + str(dict_desc["suburb"])
#debug				str_type = str(dict_desc["type"]) + "_" + str(tag["price_filter"])
				str_type = str(tag["price_filter"])
#				str_type = str(dict_desc["inspection_time"])
#				list_type = str_type.split(" ")
#				str_type = str(list_type[0]) + str(list_type[1]) + str(list_type[2])
#				print "A.", str_type
				if str_type not in tag["list types"]:
					tag["list types"].append( str_type )
#filter 1				
				list_of_filter_dicts = kml_func.read_filter_file("rejects.csv")
				found = 0
				for loop_dict in list_of_filter_dicts:
					if str_link == loop_dict["Link"]:
#						print "skipping ", loop_dict 
						found = 1
						break
						
#filter 2
#				if dict_desc["inspection_date"] != "Sat 29 Dec":
#					found = 1
						
				if found == 0:
					kml_func.create_point(str_lat, str_lng, str_type, str_name, str_description, str_extended_data)
					kml_func.add_to_csv("Rentals Available CSV", str_link, dict_desc, tag)
#			else:
#				print "OUT -->", str_extended_data

def parse_trainstations_dict(kml_inst, list_of_dicts_trainstations):
	str_type = "TrainStations"
	for loop_dict in list_of_dicts_trainstations:
		str_coords = loop_dict["the_geom"]
		lst_coords = str_coords.split(" ")
		str_lng = lst_coords[1]
		tmp_lst = str_lng.split("(")
		str_lng = tmp_lst[1]
		
		str_lat = lst_coords[2]
		tmp_lst = str_lat.split(")")
		str_lat = tmp_lst[0]
		str_description = loop_dict["station"] + " Metro Station"
#		print str_lat, "\t", str_lng
		kml_inst.create_point(str_lat, str_lng, "TrainStations", loop_dict["station"], str_description)

kmlX = Json2kml_2.myKml()

list_of_dicts_csvschools = kmlX.read_filter_file()
str_json = read_text_file()
top_dict = json.loads(str_json[1])
merge_d_structures(top_dict, list_of_dicts_csvschools)
rec_parse_types(kmlX, top_dict)

list_of_dicts_trainstations = kmlX.read_filter_file("metro_stations_accessibility.csv")
parse_trainstations_dict(kmlX, list_of_dicts_trainstations)

del_var = 1
debug = 0
if del_var == 1:
	baseURL3 = "https://services.realestate.com.au/services/listings/summaries/search?query={%22channel%22:%22rent%22,"
	filter_str = "%22filters%22:{%22priceRange%22:{%22minimum%22:%220%22,%22maximum%22:%22225%22}},"
	rect_str = "%22boundingBoxSearch%22:[-37.8558026842471,145.04633426988528,-37.81546953042379,145.10495663011477]"
	url_tail = "%22pageSize%22:%22500%22}"
	list_of_sch_dicts = top_dict["schools"]
#	list_of_price_filters = [(250,300), (300,350), (350,400), (400,450), (450,500)]
	list_of_price_filters = [(350,480)]
	str_list_of_price_filters = []
#"filters":{"priceRange":{"minimum":"0","maximum":"225"}}
	i = 5
	if debug == 0:
		for sch_dict in list_of_sch_dicts:
			if "Shortlist" in sch_dict.keys():
				if sch_dict["Shortlist"] == "Y":
					tup1=sch_dict["boundRect"][0]
					tup2=sch_dict["boundRect"][1]
					print sch_dict
					for price_tupl in list_of_price_filters:
						price_url = "%22filters%22:{%22priceRange%22:{%22minimum%22:%22" + str(price_tupl[0]) + "%22,%22maximum%22:%22" + str(price_tupl[1]) + "%22}},"
						rect_url = "%22boundingBoxSearch%22:[" + str(tup1[0]) + "," + str(tup1[1]) + "," + str(tup2[0]) + "," + str(tup2[1]) + "],"
						loopURL = baseURL3 + price_url + rect_url + url_tail
						print "loopURL = ", loopURL
#					break
						page_loop = requests.get(loopURL)
						text_loop = page_loop.text
						loop_top_dict = json.loads(text_loop)
						str_price_filter = str(price_tupl[0]) + "_" + str(price_tupl[1])
						tag = { "school_name" : sch_dict["name"], "School Rank": sch_dict["School Rank"], "price_filter": str_price_filter, "School Zone": sch_dict["zone"], "list types":[]}
#						tmp_str = "Rentals Available " + str_price_filter
						print "Before parse_real_estate_data"
						parse_real_estate_data(kmlX, loop_top_dict, tag)
						print "After parse_real_estate_data"
						str_list_of_price_filters.extend(tag["list types"])

#						if tag["list types"] not in str_list_of_price_filters:
#							str_list_of_price_filters.append(tag["list types"])
						
						i = i - 1
#debug												if i <= 0:
#debug													break			

	
#	file_dict = {	"ShortListed_Primary.kml": ["ShortListed School Locations", "ShortListed School Catchment Areas"],
#					"All_Primary.kml": ["Primary School Locations", "Primary School Catchment Areas"],
#					"ShortList_Rental.kml": str_list_of_price_filters,
#					"TrainStations.kml": ["TrainStations"],
#					"ShortList_Rentals.csv": ["Rentals Available CSV"]
#				}
	file_dict = {	"ShortListed_Primary.kml": ["ShortListed School Locations", "ShortListed School Catchment Areas"],
					"ShortListed_Secondary.kml":["ShortListed School Locations", "ShortListed School Catchment Areas"],
					"All_Primary.kml": ["Primary School Locations", "Primary School Catchment Areas"],
					"All_Secondary.kml": ["Secondary School Locations", "Secondary School Catchment Areas"],
					"ShortList_Rental.kml": str_list_of_price_filters,
					"TrainStations.kml": ["TrainStations"],
					"ShortList_Rentals.csv": ["Rentals Available CSV"]
				}

	for my_key in file_dict.keys():
		kmlX.write_to_file(my_key, file_dict[my_key])
		
else:
	baseURL2 = "https://www.realestate.com.au/425421474"
	baseURL2 = "https://www.realestate.com.au/425328050"

	dicti = getDescription(baseURL2)
	print dicti
	
