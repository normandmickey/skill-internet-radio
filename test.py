import json
import requests

s_details = requests.get('http://localhost:5000/station')
stations = s_details.json()

for station in stations:
    if station['name'] == "Rocks reatest Hits":
       stream_url = station['url']
       stream_name = station['name']
       stream_url2 = stream_url.encode('utf-8')
    else:
       stream_url2 = "none"
       stream_name = "none"
       
 
    print stream_url2, stream_name

