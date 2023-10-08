from fastapi import FastAPI, HTTPException
from datetime import datetime
import face_recognition
import time
import cv2
from pydantic import BaseModel
from typing import List

app = FastAPI()


#------------ firebase set-up ---------
#import required modules
import firebase_admin
from firebase_admin import db,credentials

#auth to firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://attendancesym-3b022-default-rtdb.firebaseio.com/"})

# creating reference to root node
ref = db.reference("/")


class CaptureResponse(BaseModel):
    username: str
    face_encodings: List[List[float]]

@app.post("/capture_image/{username}", response_model=CaptureResponse)
async def capture_image(username: str):
    try:
        video_capture = cv2.VideoCapture(0)
        time.sleep(5)
        t = 0

        while True:
            ret, frame = video_capture.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Error capturing frame")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb)

            face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
            t += 1

            if t == 1:
                face_encodings_lists = [encoding.tolist() for encoding in face_encodings]
                db.reference("/").push().set({"username":username,"face_encodings":face_encodings_lists})
                ref.get()
                return CaptureResponse(username=username, face_encodings=face_encodings_lists)
    
    finally:
        # Release the video capture resource when done
        video_capture.release()
