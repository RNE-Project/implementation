import cv2
from keras.models import load_model
import numpy as np
from websocket_server import WebsocketServer
import logging
import sys
from util import *
import rumps
from subprocess import Popen, PIPE

# parameters for loading data and images
detection_model_path = 'face.xml'
emotion_model_path = 'emotion.hdf5'
emotion_labels = get_labels('fer2013')

conn = False

# hyper-parameters for bounding boxes shape
frame_window = 10
gender_offsets = (30, 60)
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming
video_capture = cv2.VideoCapture(0)

#counter
emotion_counter = [0] * 7

def new_client(client, server):
	conn = True

def client_left(client, server):
    conn = False

def notif(msg, title):
    cmd = "display notification \"{}\" with title \"{}\"".format(msg, title)
    #cmd = b"""display notification "Notification message" with title "Title" Subtitle "Subtitle" """
    Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(str.encode(cmd))

server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)


def run_loop():
    while True:
        try:

            bgr_image = video_capture.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(face_detection, gray_image)

            for face_coordinates in faces:

                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue
                gray_face = preprocess_input(gray_face, False)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                em = np.argmax(emotion_classifier.predict(gray_face))
                emotion_counter[em] += 1
                print("ok")

                if conn != None:
                    server.send_message_to_all("hi")

                emotion_text = emotion_labels[em]
        except:
            continue

class App(rumps.App):
    def __init__(self):
        super(App, self).__init__("RNE")
        self.menu = ["Start", "Say hi"]

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        notif("lol", "ok")

    @rumps.clicked("Start")
    def start(self, _):
        run_loop()

App().run()
server.run_forever()



