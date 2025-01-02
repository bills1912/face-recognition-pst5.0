import os
import cv2
import pickle
import face_recognition

# Importing student images
folderPath = 'Files/Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
# for path in pathList:
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#     studentIds.append(os.path.splitext(path)[0])

#     fileName = f'{folderPath}/{path}'
#     bucket = storage.bucket()
#     blob = bucket.blob(fileName)
#     blob.upload_from_filename(fileName)


#     # print(path)
#     # print(os.path.splitext(path)[0])
# print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    print("Encoding Started ...")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")

    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved")



