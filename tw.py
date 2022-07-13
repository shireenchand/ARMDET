from twilio.rest import Client
from twilio_creds import auth_sid,auth_token,phone_no


class messenger:
	def __init__(self,location,time,date):
		self.location = location
		self.time = time
		self.date = date
		self.to_number = "NUMBER TO SEND TO"

	def send_message(self):
		client = Client(auth_sid, auth_token)
		message = client.messages \
		                .create(
		                     body=f"Weapon Detected at {self.location} on {self.date} at {self.time}",
		                     from_=phone_no,
		                     to=self.to_number
		                 )

		print(message.sid)
