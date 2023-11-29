import cv2

for i in range(10, 17):  # Adjust range based on your video devices
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Device /dev/video{i} opened successfully")
        # You can add more code here to test frame capture
        cap.release()
    else:
        print(f"Failed to open device /dev/video{i}")
