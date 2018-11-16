import cv2
from keras.models import load_model
import numpy as np
from websocket_server import WebsocketServer
import logging
import sys
from util import *
import rumps
from subprocess import Popen, PIPE
from threading import Thread
from os import listdir
from os.path import isfile, join


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

# starting video streaming
video_capture = cv2.VideoCapture(0)

#counter
emotion_counter = [0] * 7

server = WebsocketServer(13254, host='127.0.0.1', loglevel=logging.INFO)

def websocket_thread(threadname):
    global conn
    global server
    def new_client(client, server):
        conn = True

    def client_left(client, server):
        conn = False	


    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.run_forever()

def notif(msg, title):
    cmd = "display notification \"{}\" with title \"{}\"".format(msg, title)
    #cmd = b"""display notification "Notification message" with title "Title" Subtitle "Subtitle" """
    Popen(["osascript", '-'], stdin=PIPE, stdout=PIPE).communicate(str.encode(cmd))
    
def pred_from_img(gray_image):
    faces = detect_faces(face_detection, gray_image)
    ar = []

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
        ar.append(np.argmax(emotion_classifier.predict(gray_face)))

    return ar


def processing_thread(threadname):
    global conn
    global server
    while True:
        try:

            bgr_image = video_capture.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            em = pred_from_img(gray_image)
            
            for e in em:
                emotion_counter[e] += 1

                if conn:
                    server.send_message_to_all("hi")
    
                emotion_text = emotion_labels[e]
        except:
            continue

class App(rumps.App):
    def __init__(self):
        super(App, self).__init__("RNE")
        self.menu = ["Check stats", "Order photos"]
        thread1 = Thread( target=websocket_thread, args=("Thread-1", ) )
        thread2 = Thread( target=processing_thread, args=("Thread-2", ) )
        
        thread1.join()
        thread2.join()

    @rumps.clicked("Check stats")
    def check_stats(self, _):
        s = sum(emotion_counter)
        data = ""
        for i in range(7):
            emotion_counter[i]*100/s = percent
            data += "{}: {} %\n".format(emotion_labels[i], int(percent))
        notif(data, text)
        
    @rumps.clicked("Order photos")
    def order(self, _):
        path = ""
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for i in range(7):
            try:
                os.makedirs(join(path, emotion_labels[i]))
            except:
                continue
        for file in files:
            img = cv2.imread(file, 0)
            em = pred_from_img(img)
            if em != []:
                counter = [0]*7
                for e in em:
                    counter[0] += 1
                category = counter.index(max(counter))
                d = join(path, category)
                os.rename(join(path, file), join(d, file))               

App().run()



