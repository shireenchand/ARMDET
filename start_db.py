import firebase_admin
from firebase_admin import db

def start():

	# databaseURL = "https://weapon-detection-91345-default-rtdb.firebaseio.com/"
	databaseURL = "https://weapon-detection-8d17b-default-rtdb.firebaseio.com/"
	# storagURL = 'weapon-detection-91345.appspot.com'
	storagURL = 'weapon-detection-8d17b.appspot.com'
	cred_obj = firebase_admin.credentials.Certificate('key.json')

	default_app = firebase_admin.initialize_app(cred_obj, {
			'databaseURL':databaseURL,
			'storageBucket': storagURL
			})