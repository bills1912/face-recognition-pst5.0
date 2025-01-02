import os
import cv2
import pickle
import face_recognition

from PIL import Image
from io import BytesIO
from pymongo import MongoClient

# Importing student images
folderPath = 'Files/Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

client = MongoClient('path/of/mongodb/connection')
frecog_mongo = client["face_recognition_mongo"]
frecog_mongo_coll_img = frecog_mongo["image_recog_data"]

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    img_bytes = BytesIO()
    fileName = f'{folderPath}/{path}'
    img_file = Image.open(fileName)
    img_file.save(img_bytes, format='PNG')
    img_mongo_data = {"id":path.split(".")[0], "img_data":img_bytes.getvalue()}
    frecog_mongo_coll_img.insert_one(img_mongo_data)

print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
print(encodeListKnown)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")



