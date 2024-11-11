from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()

time.sleep(5)  # 5초 동안 카메라 작동

# 프레임 캡처
frame = picam2.capture_array()
if frame is not None:
    print("Frame captured successfully!")
else:
    print("Failed to capture frame.")

picam2.stop()
