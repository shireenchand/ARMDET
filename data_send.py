import firebase_admin
from firebase_admin import db,storage
import json
from start_db import start
import io
import base64
from PIL import Image


class creds:
	def __init__(self,location):
		self.location = location
		start()
	def send_data(self,prediction,uid=None,image=None):
		bucket = storage.bucket()
		ref = db.reference(f"/{self.location}/Detections")
		for key,value in prediction.items():
			ref.push().set(value)
		if image != None and uid != None:
			blob = bucket.blob(f'{uid}.jpg')
			blob.upload_from_string(image,content_type='image/jpg')
