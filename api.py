# importing libraries
import flask
import io
import string
import time
import os
import numpy as np
import torch
from PIL import Image
import cv2
from flask import Flask, jsonify, request, Response 
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
import geocoder
import data_send
import base64
from PIL import Image
from io import BytesIO
import uuid
import tempfile
from datetime import datetime,date
from tw import messenger

# Function to get current time
def get_time():
	now = datetime.now()
	date_now = date.today()
	current_time = now.strftime("%H:%M:%S")
	return current_time,date_now

# Function to get location
def get_location():
	g = geocoder.ip('me')
	geoLoc = Nominatim(user_agent="GetLoc")
	locname = geoLoc.reverse(f"{g.latlng[0]},{g.latlng[1]}")
	location = locname.address
	print(locname.address)
	return location

# Store location
location = get_location()

# Initialize Database
obj = data_send.creds(location)

# Variable to check if message sent for live cam
global sent
sent = False


# Loading the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/final.pt')

# Predict Function for individual frames and images
def predict(img,time,date,uid,type="no"):
	results = model(img)
	data = results.pandas().xyxy[0]
	pred = dict()
	for i in range(data.shape[0]):
		ind = dict()
		ind['xmin'] = str(data.iloc[i]['xmin'])
		ind['ymin'] = str(data.iloc[i]['ymin'])
		ind['xmax'] = str(data.iloc[i]['xmax'])
		ind['ymax'] = str(data.iloc[i]['ymax'])
		ind['confidence'] = str(data.iloc[i]['confidence'])
		ind['class'] = str(data.iloc[i]['class'])
		ind['name'] = str(data.iloc[i]['name'])
		ind['time'] = str(time)
		ind['uid'] = uid
		ind['date'] = str(date)
		if type == "video":
			ind['image'] = str(base64.b64encode(img))
		pred[i] = ind
	print(pred)
	return pred


app = Flask(__name__)

# Endpoint for image and individual live cam frame prediction 
@app.route('/predict-image',methods=['POST'])
def infer_image():
	# Get file from the request sent
	if 'file' not in request.files:
		return "Please try again. The Image doesn't exist"

	file = request.files.get('file')

	if not file:
		return

	time,date = get_time()
	img_bytes = file.read()
	image = Image.open(io.BytesIO(img_bytes))
	uid = str(uuid.uuid4())  # Generating uid

	prediction=predict(image,time,date,uid) 

	if len(prediction) > 0:
		obj.send_data(prediction,uid,img_bytes) # Sending data to be stored in database
		
		# Send alerts if weapon detected
		msg_obj = messenger(location,time,date)
		msg_obj.send_message()

	return jsonify(prediction)



# Endpoint for video prediction
@app.route('/predict-video',methods=['POST'])
def infer_video():

	present = False

	if 'file' not in request.files:
		return "Please try again. The Image doesn't exist"

	file = request.files.get('file')

	if not file:
		return
	
	filename = secure_filename(file.filename)
	tfile = tempfile.NamedTemporaryFile(delete=False)
	tfile.write(file.read())
	video = cv2.VideoCapture(tfile.name)
	fps = video.get(cv2.CAP_PROP_FPS)
	frame_width = int(video.get(3))
	frame_height = int(video.get(4))
	# Initialise VideoWriter
	out = cv2.VideoWriter('now.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         fps, (frame_width,frame_height))
	
	# Traversing through each frame
	while True:
		ret,frame = video.read()
		if ret:
			uid = str(uuid.uuid4())
			prediction=predict(frame,time,date,uid)
			f = frame.copy()
			if len(prediction) == 0:
				pass

			elif prediction[0]['class'] is not None:
				present = True
				for i in prediction:
					f = cv2.rectangle(frame,(int(float(prediction[i]['xmin'])),int(float(prediction[i]['ymin']))),(int(float(prediction[i]['xmax'])),int(float(prediction[i]['ymax']))),(0,255,0),2)
					pil_im = Image.fromarray(frame)
					b = io.BytesIO()
					pil_im.save(b,'jpeg')
					im_bytes = b.getvalue()
					obj.send_data(prediction,uid,im_bytes)
			out.write(f)
		else:
			if present == True:
				time,date = get_time()
				# Send alerts if weapon detected
				msg_obj = messenger(location,time,date)
				msg_obj.send_message()
			video.release()
			out.release()
			cv2.destroyAllWindows()
			break
	return "NOTHING FOUND"


@app.route('/predict-live',methods=['POST'])
def infer_live():
	# Get file from the request sent
	if 'file' not in request.files:
		return "Please try again. The Image doesn't exist"

	file = request.files.get('file')

	if not file:
		return

	time,date = get_time()
	img_bytes = file.read()
	image = Image.open(io.BytesIO(img_bytes))
	uid = str(uuid.uuid4())  # Generating uid

	prediction=predict(image,time,date,uid) 
	
	
	if len(prediction) > 0:
		obj.send_data(prediction,uid,img_bytes) # Sending data to be stored in database
		
		# Send alerts if weapon detected
		if sent == False:
			msg_obj = messenger(location,time,date)
			msg_obj.send_message()
			sent = True

	return jsonify(prediction)




