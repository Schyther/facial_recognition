from django.shortcuts import render
from django.http import StreamingHttpResponse

import cv2
from camera import Camera
import face_recognition

# Create your views here.
def return_stream(request):
    return  render(request, template_name='stream.html')

def generate_stream(request):
    return StreamingHttpResponse(gen(Camera()),
                content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)

        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
