import pyrebase

config = {
    "apiKey": "AIzaSyB4kWJtF_Rle79bsYxgn-s9wZsupiYFPY4",
    "authDomain": "attendance-face-recognit-f55e6.firebaseapp.com",
    "projectId": "attendance-face-recognit-f55e6",
    "storageBucket": "attendance-face-recognit-f55e6.appspot.com",
    "messagingSenderId": "791980223908",
    "appId": "1:791980223908:web:49e903a6296c8864bf2531",
    "measurementId": "G-0H34JG6QEK",
    "databaseURL": "https://attendance-face-recognit-f55e6-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# # Upload images to Firebase Storage
# storage.child("ImgTest1.png").put("testImg1.png")
# storage.child("ImgTest2.jpg").put("testImg2.jpg")

# Download images from Firebase Storage
img1_download = storage.download("ImgTest1.png", "dwnld1.png")
img2_download = storage.download("ImgTest2.jpg", "dwnld2.jpg")

# Check if downloads were successful
if img1_download:
    print("ImgTest1.png downloaded successfully!")
else:
    print("Failed to download ImgTest1.png")

if img2_download:
    print("ImgTest2.jpg downloaded successfully!")
else:
    print("Failed to download ImgTest2.jpg")
