import streamlit as st
import requests
import cv2
import tempfile
from PIL import Image
import os
import numpy as np
from streamlit_option_menu import option_menu
from checkdata import widget
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
from webcam import live_pred
from app_footer import footer

st.set_page_config(page_title="ARMDET", page_icon='🔫')

selected = option_menu(
	menu_title=None,
	options=["Image","Video","Check Data","Live Camera"],
	menu_icon="cast",
	orientation="horizontal",
	)


st.markdown("<h1 style='text-align: center; color: white;'>ARMDET</h1>", unsafe_allow_html=True)

if selected == "Image":
	k = 0
	p = 0
	image = st.file_uploader("Upload Image")
	if image:  
		# print(type(image))
		url = "http://127.0.0.1:5000/predict-image"
		r = requests.post(url=url,files={'file':image.read()})
		print(r.json())
		prediction = r.json()
		image = Image.open(image)
		for i in range(len(prediction)):
			if prediction[str(i)]['class'] == '0':
				k += 1
			elif prediction[str(i)]['class'] == '1':
				p += 1
			i = str(i)
			image = cv2.rectangle(np.array(image),(int(float(prediction[i]['xmin'])),int(float(prediction[i]['ymin']))),(int(float(prediction[i]['xmax'])),int(float(prediction[i]['ymax']))),(0,255,0),2)
		st.write(f"{k} knives and {p} pistols are detected")
		st.image(image)


if selected == "Video":
	video = st.file_uploader("Upload Video") 
	if video: 
		url = "http://127.0.0.1:5000/predict-video"
		r = requests.post(url=url,files={'file':video.read()})
		print(r.json())

if selected == "Check Data":
	widget()

if selected == "Live Camera":
	webrtc_streamer(key="example",video_processor_factory=live_pred)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown(footer,unsafe_allow_html=True)

	
