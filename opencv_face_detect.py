from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import face_recognition
import pyrebase
import cv2
import urllib
import firebase_admin
from firebase_admin import storage

# Set the camera index to 0 for the built-in camera
camera_index = 0
cap = cv2.VideoCapture(camera_index)

attendance_file = 'Attendance.csv'

# Check if Attendance.csv exists
if not cv2.os.path.isfile(attendance_file):
    # Create a new DataFrame and save it if the file does qnot exist
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

# Cloud storage configuration
# Change this to the path of your images folder in Firebase Storage
cloud_image_folder = 'mini_images'

# List files in the cloud image folder
blobs = bucket.list_blobs(prefix=cloud_image_folder)

images = []
classNames = []

# Define the expiration time (e.g., 1 hour from now)
expiration = datetime.utcnow() + timedelta(hours=1)

flag = True
# Iterate over the files
for blob in blobs:

    if flag:
        flag = False
        continue

    file_name_temp = blob.name.split('/')[-1].split('.')[0]
    print(file_name_temp)
    file_name = file_name_temp.split('-')[0]
    classNames.append(file_name)

    # Get the download URL of the file with the specified expiration time
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

    except Exception as e:
        print(f"Error downloading image: {str(e)}")

print("Images and names loaded from cloud storage.")


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if len(face_encodings) > 0:
            encode = face_encodings[0]
            encodeList.append(encode)
        else:
            print("Error: No face detected in the image.")
    return encodeList


def markAttendance(name):
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString}')


encodeListKnown = findEncodings(images)
print('Encoding Complete')

# RTSP stream URL
rtsp_url = "rtsp://attendaceCam:071063062@192.168.1.100:554/stream1"

# Open RTSP stream with authentication
cap = cv2.VideoCapture(rtsp_url)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to open RTSP stream.")
else:
    while True:
        # Read a frame from the stream
        ret, frame = cap.read()

        if ret:
            # Display the frame
            cv2.imshow("RTSP Stream", frame)

            # Face recognition on the frame
            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(
                imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(
                    encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(
                    encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            cv2.imshow('Webcam', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            print("Error: Failed to read frame from RTSP stream.")
