picture-gps-parser
==================

Parses EXIF data on pictures to get GPS location data  (Based off of script by Eran Sandler: https://gist.github.com/erans/983821)

Outputs the results in an HTML file in a table including:
	-link to the picture.	
	-image type.	
	-date/time taken (plus date/time digitized and original, all are usually the same).	
	-Latitude/Longitude GPS coordinates.	
	-Link to coordinates on Google Maps.	
	-Make of camera device.	
	-Model of camera device.	
	-SHA1 hash.	



Supports recursive traversal (sub-directories or sub-folders)

Supports specifying a target directory or folder


DEPENDENCIES: 
-Python (http://www.python.org/download/releases/2.7.5/)
-PIL (http://www.pythonware.com/products/pil/)


TODO: 
-See if filetypes other than .jpeg have exif data (.raw ?)


