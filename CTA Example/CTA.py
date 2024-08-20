# Used to carry out automated test cases for browsers or web applications.
from selenium import webdriver # pip install selenium
from urllib.request import urlopen
# Module implements a simple and efficient API for parsing and creating XML data.
import xml.etree.ElementTree as ET
import time

###
# Warning: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'.
# pip uninstall urllib3
# pip install urllib3==1.26.7
###

# Latitude of Dave's office.
office_lat = 41.980262

def distance(lat1, lat2):
    'Return approx miles between lat1 and lat2'
    return 69 * abs(lat1 - lat2)

driver = webdriver.Firefox()
# Set of bus ids that you want to monitor.

busids = '1874' # Get the bus is operating from https://www.ctabustracker.com/map
api_key = 'YOUR_API_KEY' # Get API key from https://www.ctabustracker.com/home
url_string = "https://www.ctabustracker.com/bustime/api/v2/getvehicles?key=" + api_key + "&vid=" + busids
print("URL: " + url_string) # Place this URL to browser, you can see the XML file



latitude = ""
longitude = ""
vehicle_id = ""
route = ""
dist = 0
while True:
    with urlopen(url_string) as f:
        tree = ET.parse(f)
        root = tree.iter()
        for child in root:
            #print(child.tag, child.text, child.attrib)
            if child.tag == "lat" :
                latitude = child.text
                latitude_float = float(latitude)
            if child.tag == "lon" :
                longitude = child.text
                longitude_float = float(longitude)
            if child.tag == "vid":
                vehicle_id = child.text
            if child.tag == "rt":
                route = child.text

        dist = distance(latitude_float, office_lat)
        print('%s Latitude: %0.6f Longitude: %0.6f Distance %0.6f miles' % (vehicle_id, latitude_float, longitude_float, dist))
        # Launch a browser to see on a map
        x = 'www.openstreetmap.org/?mlat=%f&mlon=%f&zoom=17' % (latitude_float, longitude_float)
        refreshrate = 5 # five seconds
        driver.get("http://" + x)
        time.sleep(refreshrate)
        # driver.refresh()