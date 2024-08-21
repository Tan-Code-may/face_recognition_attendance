import cv2

# # RTSP stream URL
# rtsp_url = "rtsp://attendaceCam:071063062@192.168.1.105:554/stream1"


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

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            print("Error: Failed to read frame from RTSP stream.")
            break

    # Release the RTSP capture
    cap.release()
    cv2.destroyAllWindows()
