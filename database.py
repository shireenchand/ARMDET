import firebase_admin
from firebase_admin import db
import json


databaseURL = "YOUR DATABASE URL"

cred_obj = firebase_admin.credentials.Certificate('key.json')

default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

ref = db.reference("/")
# with open("data.json", "r") as f:
# 	file_contents = json.load(f)
# ref.set(file_contents)

# ref.set({
# 	"Books":
# 	{
# 		"Best_Sellers": -1
# 	}
# })

# ref = db.reference("/Books/Best_Sellers")
# with open("data.json", "r") as f:
# 	file_contents = json.load(f)

# for key, value in file_contents.items():
# 	ref.push().set(value)

ref = db.reference("/Books/Best_Sellers")
best_sellers = ref.get()
print(best_sellers)
for key, value in best_sellers.items():
	if(value["Author"] == "J.R.R. Tolkien"):
		# value["Price"] = 90
		ref.child(key).update({"Price":10})
