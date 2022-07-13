import firebase_admin
from firebase_admin import db

def start():

	databaseURL = "YOUR DATABASE URL"
	# storagURL = 'weapon-detection-91345.appspot.com'
	storagURL = 'YOUR STORAGE URL'
	cred_obj = firebase_admin.credentials.Certificate('key.json')

	default_app = firebase_admin.initialize_app(cred_obj, {
			'databaseURL':databaseURL,
			'storageBucket': storagURL
			})
