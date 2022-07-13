import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
from PIL import Image
import requests
import io
import cv2
import numpy as np

class live_pred(VideoTransformerBase):
	def recv(self, frame):
		url = "http://127.0.0.1:5000/predict-image"
		pil_im = frame.to_image()
		b = io.BytesIO()
		pil_im.save(b,'jpeg')
		im_bytes = b.getvalue()
		r = requests.post(url=url,files={'file':im_bytes})
		print(r.json())
		prediction = r.json()
		img = frame.to_ndarray(format="bgr24")
		for i in range(len(prediction)):
			i = str(i)
			img = cv2.rectangle(np.array(img),(int(float(prediction[i]['xmin'])),int(float(prediction[i]['ymin']))),(int(float(prediction[i]['xmax'])),int(float(prediction[i]['ymax']))),(0,255,0),2)
		return av.VideoFrame.from_ndarray(img, format="bgr24")


















