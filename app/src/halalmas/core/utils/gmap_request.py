import requests
import json

#https://developers.google.com/maps/documentation/geocoding/start
#https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
url_here = "https://www.google.com/maps/search/?api=1&amp;query=Mano Coffee House,Standard Chartered Building, Lantai Lower Ground, Jl. Prof Dr Satrio, Karet, Jakarta"
# response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')
response = requests.get(url_here)

print("response: {}".format(response))
print(response.status_code, response.encoding)
print(dir(response))
print(response.text)
# resp_json_payload = json.loads(response.json()) #.decode('utf-8').replace('\0', '')

# print("resp_json_payload: {}".format(resp_json_payload))
# print(resp_json_payload['results'][0]['geometry']['location'])