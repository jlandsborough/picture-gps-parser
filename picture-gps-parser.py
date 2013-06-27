#
# Description: Parses EXIF data on pictures to get GPS location data.  Outputs an HTML file containing
#
# By: Jason Landsborough
# Last updated: 06/26/13
#
# Forked from script (get_lat_lon_exif_pil.py) posted by Eran Sandler, here: https://gist.github.com/erans/983821 
#
# Parameters: None

import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import hashlib



###  GLOBAL VARIABLES ###
global_target = os.getcwd()	#Default is same directory as python script
global_recursion = 1		#1 to enable 	0 to disable




#from "get_lat_lon_exif_pil.py" (https://gist.github.com/erans/983821)
def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon
#end of get_lat_lon_exif_pil.py functions








#Function: 	get_from_file(current_file)
#Parameters: 	current_file - Path to a file
#Description:	Checks if current_file is an image, if so, tries to extract EXIF data from it
#
def get_from_file(current_file):
	#Check if the file is an image (currently only jpegs, need to test other files if they support EXIF)
	if ".jpeg"in current_file.lower() or ".jpg" in current_file.lower():			
		fout.write("<tr>")
		f = open(current_file)
		path =  os.path.abspath(current_file);
		print "f:" + str(f)
		filename = os.path.basename(path)
		
		#get file hash	
		sha1 = hashlib.sha1()
		try:
		        sha1.update(f.read())
		finally:
			f.close()
		sha1hash = sha1.hexdigest() 
		print "f:" + str(f)
		
		#Open image, extract EXIF, and output results
		try:
			#write row		
			##IF MORE TYPES ARE ADDED, change this to determine filetype
			filetype = "jpeg"
			img = Image.open(current_file)			
			exif_data = get_exif_data(img)
			location =  get_lat_lon(exif_data)
			
			#check if EXIF data exists, if not skip the file
			if(exif_data != {}):
				make = exif_data['Make']
				model = exif_data['Model']
				pic_dt = exif_data['DateTime']
				pic_dt2 = exif_data['DateTimeDigitized']
				pic_dt3 = exif_data['DateTimeOriginal']
				
				##print exif_data
				fout.write("<td><a href=\""+path+"\">"+filename+"</a></td>")
				fout.write("<td>" + filetype + "</td>")
				fout.write("<td>" + pic_dt + "  ("+pic_dt2+")  ("+pic_dt3+")"+ "</td>")
				fout.write("<td>" + str(location[0]) + ", " + str(location[1]) + "</td>")
			
				if "none" in str(location).lower():
					fout.write("<td></td>")
				else:
					fout.write("<td><a href=\"https://maps.google.com/maps?f=q&q=loc:"+ \
							str(location[0]) + "," + str(location[1]) +"\">Google Maps</a></td>")
				fout.write("<td>" + make + "</td>")
				fout.write("<td>" + model + "</td>")
				fout.write("<td>" + sha1hash + "</td>")
			else:
				print "No EXIF data for " + current_file + ", not processing picture further"
		except IOError:
			print "Unable to open file (" + path + ").  This might be due to missing/corrupted EXIF data.  Skipping" 
		fout.write("</tr>") #end table row



#get date and time
now_time = datetime.datetime.now()
now_dt = now_time.strftime("%Y-%m-%d_%H-%M")

#open output file
fout = open("images_" + now_dt + ".html", "w")
#write initial HTML code to file
fout.write("<HTML><BODY>")
fout.write("<table border=\"1\">")
fout.write("<tr><b><td>Image</td><td>Type</td><td>Date Taken</td><td>GPS Coordinates</td><td>map</td><td>Make</td><td>Model</td><td>SHA1 Hash</td></b></tr>")


#if recursion
if(global_recursion == 1):
	#for all files in the current directory and subdirectories
	for curdir, thedir, files in os.walk(global_target):
		for thefile in files: 
			get_from_file(curdir + "/" + thefile)
#if no recursion
elif(global_recursion == 0):
	#for all files in the current directory and subdirectories
	for thefile in os.listdir(global_target): 
		get_from_file(global_target + "/" + thefile)	
#if bad recursion option
else:
	print "Unknown recursion option"
		
#add last of HTML code and close file
fout.write("</table>")
fout.write("</BODY></HTML>")
fout.close()

