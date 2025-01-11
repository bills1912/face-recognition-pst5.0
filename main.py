import os
import sys
import cv2
import time
import random
import pickle
import cvzone
import pyttsx3
import playsound
import numpy as np
import face_recognition
from pydub import AudioSegment
from pydub.playback import play
from form_guest import new_guest_form

from PIL import Image
from gtts import gTTS
from io import BytesIO
from datetime import datetime
from pymongo import MongoClient
from form_guest import new_guest_form
from encode_generator import findEncodings

sys.dont_write_bytecode = True

client = MongoClient('path/of/mongodb/connection')
frecog_mongo = client["face_recognition_mongo"]
frecog_mongo_collect = frecog_mongo["frecog_data"]
frecog_mongo_coll_img = frecog_mongo["image_recog_data"]

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
mp3_fp = BytesIO()
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 2.0)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

img_path = 'Files/Images'

# engine.say("I love you so much more sayanggku")
# engine.runAndWait()

imgBackground = cv2.imread('Files/Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Files/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
img_list = []
cursor = frecog_mongo_coll_img.find()
for document in cursor:
    img_list.append(document['id'])

encodeListKnownWithIds = findEncodings(img_list)
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds, encodeListKnown)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # face_recognition.compare
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            print(matches)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)
            # print(matchIndex)

            if (True in matches):
                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1
            else:
                guest_img_bytes = BytesIO()
                new_id = str(random.randint(100000, 999999))
                img_name = f"{new_id}.png"
                guest_img_path = os.path.join(img_path, img_name)
                cv2.imwrite(guest_img_path, img=img)
                guest_img = Image.open(guest_img_path)
                guest_img.save(guest_img_bytes, format='PNG')
                
                new_guest_form(id=new_id, img_guest=guest_img_bytes.getvalue())
                os.remove(guest_img_path)
                
                img_list = []
                cursor = frecog_mongo_coll_img.find()
                for document in cursor:
                    img_list.append(document['id'])
                encodeListKnownWithIds = findEncodings(img_list)
                encodeListKnown, studentIds = encodeListKnownWithIds
                
        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = frecog_mongo_collect.find_one({'id':id})
                
                # Get the Image from the storage
                array = np.asanyarray(bytearray(BytesIO(frecog_mongo_coll_img.find_one({'id':id})['img_data']).read()), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 30:
                    studentInfo['total_attendance'] += 1
                    frecog_mongo_collect.update_one({'id':id}, {"$set": {"total_attendance": studentInfo['total_attendance']}})
                    frecog_mongo_collect.update_one({'id':id}, {"$set": {"last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), 
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, f"{studentInfo['job']}", (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    
                    # Text-to-speech from detected guest's name
                    audio_name = studentInfo['name']
                    tts = gTTS(audio_name, lang='id', slow=False)
                    tts.save(f"{audio_name}.mp3")
                    audio = AudioSegment.from_mp3(f"{audio_name}.mp3")
                    play(audio)
                    os.remove(f"{audio_name}.mp3")
                    # engine.say(studentInfo['name'])
                    # engine.runAndWait()


                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        time.sleep(2)
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
    if 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()