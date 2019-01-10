import os
import csv
import collections
class myKml:
	def __init__(self):
		self.kml_string_dict = {
			"head": '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.1">\n<Document>\n\t<name>\"My map of school catchment areas\"</name>\n\t<description>Cash\'s project</description>',
			"tail":"\n</Document>\n</kml>",
			"Primary School Locations":'\n<Folder>\n\t<name>"Primary School Locations"</name>\n\t<description>Points where schools are located</description>',
			"Primary School Catchment Areas": '\n<Folder>\n\t<name>"Primary School Catchment Areas"</name>\n\t<description>Areas lying in the schools catchments</description>',
			"ShortListed School Locations": '\n<Folder>\n\t<name>"ShortListed School Locations"</name>\n\t<description>Points where schools are located</description>',
			"ShortListed School Catchment Areas": '\n<Folder>\n\t<name>"ShortListed School Catchment Areas"</name>\n\t<description>Areas lying in the schools catchments</description>',
			"Secondary School Locations": '\n<Folder>\n\t<name>"Secondary School Locations"</name>\n\t<description>Points where schools are located</description>',
			"Secondary School Catchment Areas": '\n<Folder>\n\t<name>"Secondary School Catchment Areas"</name>\n\t<description>Areas lying in the schools catchments</description>',
			"Rentals Available": '\n<Folder>\n\t<name>"Rentals Available"</name>\n\t<description>Rentals available on realestate.com.au</description>',
			"Rentals Available 250_350": '\n<Folder>\n\t<name>"Rentals 250_350"</name>\n\t<description>Rentals available on realestate.com.au</description>', 
			"Rentals Available 350_450": '\n<Folder>\n\t<name>"Rentals 350_450"</name>\n\t<description>Rentals available on realestate.com.au</description>',
			"Rentals Available 450_500": '\n<Folder>\n\t<name>"Rentals 450_500"</name>\n\t<description>Rentals available on realestate.com.au</description>',
			"Rentals available in the shortlisted areas": '\n<Folder>\n\t<name>"Rentals available in the shortlisted areas"</name>\n\t<description>Rentals available on realestate.com.au</description>',
			"TrainStations": '\n<Folder>\n\t<name>"Train Stations in Melbourne"</name>\n\t<description>Rentals available on realestate.com.au</description>',
			"CSV Headers":['Link', 'School', 'School Rank'],
			"Rentals Available CSV": [] #["Rentals Available, link, School"]
		} 
			
		self.kml_style_dict = {
			"My_Style": '\n<Style id="My_Style">\n\t<LabelStyle><scale>1</scale></LabelStyle>\n\t<IconStyle>\n\t<color>ff0051e6</color>\n\t<scale>1</scale>\n\t<Icon><href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_Style1": '\n<Style id="My_Style1">\n\t<IconStyle>\n\t<color>ff0051e6</color>\n\t<scale>0.5</scale>\n\t<Icon><href>http://maps.google.com/mapfiles/kml/pal3/icon56.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_Style12": '\n<Style id="My_Style12">\n\t<IconStyle>\n\t<color>ff005100</color>\n\t<scale>0.5</scale>\n\t<Icon><href>http://maps.google.com/mapfiles/kml/pal3/icon56.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_Style13": '\n<Style id="My_Style13">\n\t<IconStyle>\n\t<color>ff00e600</color>\n\t<scale>0.5</scale>\n\t<Icon><href>http://maps.google.com/mapfiles/kml/pal3/icon56.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_Style2": '\n<Style id="My_Style2">\n\t<IconStyle>\n\t<color>ff0051e6</color>\n\t<scale>0.5</scale>\n\t<Icon><href>http://maps.google.com/mapfiles/kml/shapes/rail.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_Style3": '\n<Style id="My_Style3">\n\t<LabelStyle><scale>1</scale></LabelStyle>\n\t<IconStyle>\n\t<color>ff0051e6</color>\n\t<scale>1</scale>\n\t<Icon><href>http://maps.google.com/mapfiles/kml/shapes/rail.png</href></Icon>\n\t</IconStyle>\n</Style>',
			"My_StyleMap":'\n<StyleMap id="My_StyleMap">\n\t<Pair>\n\t<key>normal</key>\n\t<styleUrl>#My_Style2</styleUrl>\n\t</Pair>\n\t<Pair>\n\t<key>highlight</key>\n\t<styleUrl>#My_Style3</styleUrl>\n\t</Pair>\n</StyleMap>'
		}
			
		self.style_elem_dict = {
			"ShortListed School Locations": ["My_Style"],
			"Rentals Available": ["My_Style1"],
			"Rentals Available 250_350": ["My_Style12"],
			"Rentals Available 350_450": ["My_Style13"],
			"Rentals Available 450_500": ["My_Style1"],
			"TrainStations": ["My_Style2", "My_Style3", "My_StyleMap"]
		}

		self.counts = {}

		self.myKml_string = self.kml_string_dict["head"]
		
		self.kml_cache_dict = {}

	def read_filter_file(self, filename="Schools.csv"):
		list_of_dicts = []
		if filename in self.kml_cache_dict.keys():
			return self.kml_cache_dict[filename]
			
		with open(filename, "rb") as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for loop_dict in csv_reader:
				list_of_dicts.append(loop_dict)
		self.kml_cache_dict[filename] = list_of_dicts
		return list_of_dicts

	def write_to_csv(self, filename, list_of_dicts):
		if len(list_of_dicts) > 0:
			field_names = self.kml_string_dict["CSV Headers"] #list_of_dicts[0].keys()
			with open(filename, "wb") as csv_file:
				writer = csv.DictWriter(csv_file, field_names)
				writer.writeheader()
				for data in list_of_dicts:
					writer.writerow(data)
				
		with open("summary.csv", "wb") as summary_csv_file:
			writer = csv.DictWriter(summary_csv_file, self.counts.keys())
			writer.writeheader()
			writer.writerow(self.counts)
			

	def write_to_file(self, filename = "myNewKmlFile.kml", filter_list = ["Primary School Locations", "Primary School Catchment Areas", "ShortListed School Locations", "ShortListed School Catchment Areas", "Rentals Available"] ):
		print "write_to_file 1.", filename, filter_list
#debug		write_string = ""
		write_string = "" #self.kml_style_dict["Style1"]
		style_string = ""
		
		if not os.path.exists("Output"):
			os.mkdir("Output")
	
		filename = "Output" + "/" + filename
		if  "Rentals Available CSV" in filter_list and "Rentals Available CSV" in self.kml_string_dict.keys():
#			print self.kml_string_dict["Rentals Available CSV"]
			self.write_to_csv(filename, self.kml_string_dict["Rentals Available CSV"])
		else:
#			print self.kml_string_dict.keys()
			for key_str in self.kml_string_dict.keys():
				if key_str != "head" and key_str != "tail":
#					print "write_to_file 1.25.\t", key_str
#					print "write_to_file 1.5.\t", filter_list
					if key_str in filter_list:
#						print "write_to_file 2.\t", key_str
						if key_str in self.style_elem_dict.keys():
							style_string_List = self.style_elem_dict[key_str]
							for style_str in style_string_List:
								style_string = style_string + self.kml_style_dict[style_str]
#						print "write_to_file 3.\t", self.kml_string_dict[key_str]
						self.kml_string_dict[key_str] = self.kml_string_dict[key_str] + "\n</Folder>"
						write_string = write_string + self.kml_string_dict[key_str]
	#					print "write_to_file 3.", filter_list, "\n", self.kml_string_dict[key_str]
	#		style_string
			write_string = self.kml_string_dict["head"] + style_string + write_string + self.kml_string_dict["tail"]
				
			with open(filename, "wb") as kml_file:
				kml_file.write(write_string)
		print self.counts		

	def add_kml_string_dict(self, type):
		local_string = '\n<Folder>\n\t<name>"' + type  + '"</name>\n\t<description>Rentals available on realestate.com.au</description>'
		self.kml_string_dict[type] = local_string
		
	def create_point(self, lat, lng, type, name="point", description="description", extended_data = ""):
#		print lat, lng, type, shortlist, name

		local_style_str = ""
		if type not in self.style_elem_dict.keys():
			self.style_elem_dict[type] = ["My_Style1"]
			
		style_list = self.style_elem_dict[type]
		local_style_str = '\t<styleUrl>#' + style_list[0] + '</styleUrl>\n' 

		if type in self.counts.keys():
			self.counts[type] = self.counts[type] + 1
		else:
			self.counts[type] = 1
			
		local_str = '\n<Placemark>\n\t<name>\"' + str(name) + '\"</name>\n\t' + local_style_str + '<ExtendedData>' + extended_data + '</ExtendedData>\n'
#debug		local_str = local_str + '<description><![CDATA[' + description + ']]></description>\n'
			
		local_str = local_str + '\t<Point><coordinates>' + str(lng) + ", " + str(lat) + ", 0" + "</coordinates></Point>"
		local_str = local_str + "\n</Placemark>\n"

		if type not in self.kml_string_dict.keys():
			self.add_kml_string_dict(type)			
#			print self.kml_string_dict.keys() 
		for key_str in self.kml_string_dict.keys():
			if key_str == type:
				self.kml_string_dict[key_str] = self.kml_string_dict[key_str] + local_str

	def create_poly(self, list_lat, list_lng, type, name="polygon", description="description", str_extended_data = "extended_data"):
#		local_str = '\n<Placemark><name>\"' + str(name) + '\"</name>\n<description><![CDATA[' + description + ']]></description>\n'
		local_str = '\n<Placemark><name>\"' + str(name) + '\"</name>\n' + '<ExtendedData>' + str_extended_data + '</ExtendedData>\n'

		local_str = local_str + '<Polygon><outerBoundaryIs><LinearRing><coordinates>\n'
		for x, lat in enumerate(list_lat):
			str_lng = str(list_lng[x])
			str_lat = str(lat)
			local_str = local_str + str_lng + ", " + str_lat + ", 0\n"
		local_str = local_str + "\n</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>\n"
		
		for key_str in self.kml_string_dict.keys():
			if key_str == type:
				self.kml_string_dict[key_str] = self.kml_string_dict[key_str] + local_str
#				print "create_poly\t", local_str

	def add_to_csv(self, type = "Rentals Available CSV", str_link = "", dict_description = {}, dict_school = {}):
		if type in self.counts.keys():
			self.counts[type] = self.counts[type] + 1
		else:
			self.counts[type] = 1

		local_dict = collections.OrderedDict()
		local_dict["Link"] = str_link.encode('ascii','ignore')
		tmp_str = dict_school["school_name"]
		tmp_str = tmp_str.encode('ascii','ignore')
		local_dict["School"] = tmp_str
		tmp_str = dict_school["School Rank"]
		tmp_str = tmp_str.encode('ascii','ignore')
		local_dict["School Rank"] = tmp_str

#		print dict_description
		list_of_hdrs = self.kml_string_dict["CSV Headers"]
		for key_ in dict_description.keys():
			str_loop = dict_description[key_]
			local_dict[key_] = str_loop.encode('ascii','ignore')
			if key_ not in list_of_hdrs:
				list_of_hdrs.append(key_)
					
		local_list = self.kml_string_dict[type]
		local_list.append(local_dict)

		set1 = set(list_of_hdrs)
		set2 = set(dict_description.keys())
		extras = set2 - set1 
		while len(extras) > 0:
			list_of_hdrs.append(extras.pop())
