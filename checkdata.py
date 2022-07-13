import streamlit as st
import firebase_admin
from firebase_admin import db,storage
import json
from geopy.geocoders import Nominatim
import geocoder
import base64
from PIL import Image
import datetime
import io
import requests
import cv2
import numpy as np
from start_db import start

def get_location():
	g = geocoder.ip('me')
	geoLoc = Nominatim(user_agent="GetLoc")
	locname = geoLoc.reverse(f"{g.latlng[0]},{g.latlng[1]}")
	location = locname.address
	print(locname.address)
	return location
	
def widget():
	location = get_location()
	try:

		bucket = storage.bucket() 
		ref = db.reference(f"/{location}/Detections")

		data = ref.get()
		# print(data)
		# print(len(data))
		t = 0
		for i in data:
			try:
				if 'time' not in data[i]:
					data[i]['time'] = "Time not recorded"
				with st.expander(f"Prediction {t} - {data[i]['time']} - {data[i]['date']}",expanded=False):
					blob = bucket.blob(f"{data[i]['uid']}.jpg")
					link = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
					response = requests.get(link)
					img = Image.open(io.BytesIO(response.content))
					i = str(i)
					image = cv2.rectangle(np.array(img),(int(float(data[i]['xmin'])),int(float(data[i]['ymin']))),(int(float(data[i]['xmax'])),int(float(data[i]['ymax']))),(0,255,0),2)
					st.write(data[i])
					st.image(image)
				t += 1
			except:
				continue
	except ValueError:
		start()
		bucket = storage.bucket() 
		ref = db.reference(f"/{location}/Detections")

		data = ref.get()
		# print(data)
		# print(len(data))
		t = 0
		for i in data:
			try:
				if 'time' not in data[i]:
					data[i]['time'] = "Time not recorded"
				with st.expander(f"Prediction {t} - {data[i]['time']} - {data[i]['date']}",expanded=False):
					blob = bucket.blob(f"{data[i]['uid']}.jpg")
					link = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
					response = requests.get(link)
					img = Image.open(io.BytesIO(response.content))
					i = str(i)
					image = cv2.rectangle(np.array(img),(int(float(data[i]['xmin'])),int(float(data[i]['ymin']))),(int(float(data[i]['xmax'])),int(float(data[i]['ymax']))),(0,255,0),2)
					st.write(data[i])
					st.image(image)
				t += 1
			except:
				continue

	except TypeError:
		st.write("NO DATA TO SHOW")
