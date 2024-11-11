from flask import Blueprint, Response, jsonify
import cv2
import threading
import time
from picamera2 import Picamera2
import io
import numpy as np

video_bp = Blueprint('video', __name__)

# 전역 변수
camera = None
camera_lock = threading.Lock()
is_streaming = False
stream_thread = None

class RaspberryCamera:
    def __init__(self):
        try:
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration(
                main={"size": (640, 480)},
                lores={"size": (640, 480)},
                display="lores"
            )
            self.camera.configure(config)
            self.camera.start()
            time.sleep(2)
            print("라즈베리파이 카메라가 초기화되었습니다.")
            
        except Exception as e:
            print(f"카메라 초기화 오류: {e}")
            if hasattr(self, 'camera'):
                self.camera.close()
            raise
    
    def __del__(self):
        self.release()
    
    def release(self):
        if hasattr(self, 'camera'):
            self.camera.close()
            print("카메라가 해제되었습니다.")
    
    def get_frame(self):
        if not hasattr(self, 'camera'):
            return None
        try:
            frame = self.camera.capture_array()
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        except Exception as e:
            print(f"프레임 처리 중 오류 발생: {e}")
            return None

def get_camera():
    global camera
    with camera_lock:
        if camera is None:
            try:
                camera = RaspberryCamera()
                print("새로운 라즈베리파이 카메라 객체가 생성되었습니다.")
            except Exception as e:
                print(f"카메라 생성 실패: {e}")
                return None
    return camera

def generate_frames():
    global camera, is_streaming
    while is_streaming:
        try:
            cam = get_camera()
            if cam is None:
                print("카메라를 사용할 수 없습니다.")
                time.sleep(1)
                continue
            
            frame = cam.get_frame()
            if frame is None:
                print("프레임을 가져올 수 없습니다.")
                time.sleep(0.1)
                continue
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.033)
            
        except Exception as e:
            print(f"스트리밍 중 오류 발생: {e}")
            time.sleep(1)
    
    print("스트리밍 종료")

@video_bp.route('/video_feed')
def video_feed():
    global is_streaming
    is_streaming = True
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@video_bp.route('/camera/start', methods=['POST'])
def start_camera():
    global is_streaming, camera
    try:
        is_streaming = True
        if camera is None:
            camera = get_camera()
        if camera:
            return jsonify({"status": "success", "message": "Camera started"})
        else:
            return jsonify({"status": "error", "message": "Failed to start camera"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@video_bp.route('/camera/stop', methods=['POST'])
def stop_camera():
    global camera, is_streaming
    try:
        is_streaming = False
        with camera_lock:
            if camera:
                camera.release()
                camera = None
        return jsonify({"status": "success", "message": "Camera stopped"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@video_bp.before_request
def before_request():
    pass

@video_bp.teardown_app_request
def teardown_request(exception):
    pass
