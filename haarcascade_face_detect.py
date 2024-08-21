import cv2
import numpy as np
import pandas as pd
import urllib
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import storage
import face_recognition

# Set the camera index to 0 for the built-in camera
camera_index = 0
cap = cv2.VideoCapture(camera_index)

attendance_file = 'Attendance.csv'

# Check if Attendance.csv exists
if not cv2.os.path.isfile(attendance_file):
    df = pd.DataFrame(list())
    df.to_csv(attendance_file, index=False)
else:
    print("Attendance.csv exists.")

# Initialize Firebase Admin SDK
cred = firebase_admin.credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "attendance-face-recognit-f55e6.appspot.com"
})

# Get a reference to the Firebase Storage bucket
bucket = storage.bucket()
cloud_image_folder = 'image_folder'

# List files in the cloud image folder
blobs = bucket.list_blobs(prefix=cloud_image_folder)

images = []
classNames = []

flag = True
expiration = datetime.utcnow() + timedelta(hours=1)

for blob in blobs:
    if flag:
        flag = False
        continue

    file_name_temp = blob.name.split('/')[-1].split('.')[0]
    print(file_name_temp)
    file_name = file_name_temp.split('-')[0]
    classNames.append(file_name)

    download_url = blob.generate_signed_url(expiration=expiration)

    try:
        # Read the image from the download URL
        resp = urllib.request.urlopen(download_url)
        img_data = resp.read()

        if len(img_data) != 0:
            img_array = np.asarray(bytearray(img_data), dtype="uint8")
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)
            else:
                print(f"Error: Failed to decode image {file_name}")
        else:
            print(f"Error: Empty image data for {file_name}")

    except urllib.error.URLError as e:
        print(f"Error downloading image: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

print("Images and names loaded from cloud storage.")


def findEncodings(images, classNames):
    encodeList = []
    for img, className in zip(images, classNames):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (128, 128))
        encode = face_recognition.face_encodings(img, [(y, x+w, y+h, x)])
        if len(encode) > 0:
            if className:
                print(f"Name: {className}")
            else:
                print("Name: unknown")
            encodeList.append(encode[0])
        else:
            print("Error: No face detected in the image.")
    return encodeList


def markAttendance(name):
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString}')


encodeListKnown = findEncodings(images, classNames)
print('Encoding Complete')

# RTSP stream URL
rtsp_url = "rtsp://attendaceCam:071063062@192.168.1.100:554/stream1"

cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Unable to open RTSP stream.")
else:
    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imshow("RTSP Stream", frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (128, 128))

                face_encodings = face_recognition.face_encodings(
                    frame, [(y, x+w, y+h, x)])
                if len(face_encodings) > 0:
                    similarities = face_recognition.face_distance(
                        encodeListKnown, face_encodings[0])
                    min_similarity_index = np.argmin(similarities)
                    name = classNames[min_similarity_index].upper()

                    markAttendance(name)

                    cv2.rectangle(frame, (x, y), (x+w, y+h),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, name, (x + 6, y + h - 6),
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                else:
                    print("Error: No face detected in the image.")

            cv2.imshow('Webcam', frame)

            if cv2.waitKey(1) == ord('q'):
                break
        else:
            print("Error: Failed to read frame from RTSP stream.")

cap.release()
cv2.destroyAllWindows()
