import cv2
import numpy as np
import face_recognition

from PIL import Image
from io import BytesIO
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ricardozalukhu1925:kuran1925@cluster0.lhmox.mongodb.net/')
frecog_mongo = client["face_recognition_mongo"]
frecog_mongo_coll_img = frecog_mongo["image_recog_data"]

def findEncodings(imagesList):
    id_list = []
    encodeList = []
    for id in imagesList:
        id_list.append(id)
        array = np.asanyarray(bytearray(BytesIO(frecog_mongo_coll_img.find_one({'id':id})['img_data']).read()), np.uint8)
        arr_decode = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
        img = cv2.cvtColor(arr_decode, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    img_encode_with_id = [encodeList, id_list]

    return img_encode_with_id



