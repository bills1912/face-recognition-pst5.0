import cv2
import sqlite3
import numpy as np
import face_recognition

from PIL import Image
from io import BytesIO
from pymongo import MongoClient

sqliteConn = sqlite3.connect("face_recog_pst5_1200.db")
cursor = sqliteConn.cursor()

def findEncodings(imagesList):
    id_list = []
    encodeList = []
    for id in imagesList:
        id_list.append(id)
        array = np.asanyarray(bytearray(BytesIO(cursor.execute(f"""SELECT img_data FROM image_recog_data WHERE id={id}""").fetchall()[0][0]).read()), np.uint8)
        arr_decode = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
        img = cv2.cvtColor(arr_decode, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    img_encode_with_id = [encodeList, id_list]

    return img_encode_with_id



