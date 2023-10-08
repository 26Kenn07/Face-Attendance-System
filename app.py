from fastapi import FastAPI, HTTPException
from datetime import datetime
import face_recognition
import time
import cv2
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/attendance", response_model=dict)
async def attendance():
    k = 0
    try:
        video_capture = cv2.VideoCapture(0)
        time.sleep(1)
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Error capturing frame")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb)
            
            if not face_locations:
                # No face detected in the image
                break
            
            # Assuming there's only one face in the image
            face_encoding = face_recognition.face_encodings(frame_rgb, face_locations)[0]
            
            # Retrieve data from Firebase
            data = ref.get()
            for key, value in data.items():
                if "face_encodings" in value and isinstance(value["face_encodings"], list):
                    for encoding in value["face_encodings"]:
                        # Compare the face encoding from Firebase with the captured face encoding
                        match = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.4)
                        if match[0]:
                            k += 1
                            matched_username = value["username"]
                            break
                        
            if k > 0:
                return {"username": matched_username}
                
        if k == 0:
            return {"message": "User Not Found"}
                        
    finally:
        # Release the video capture resource when done
        video_capture.release()