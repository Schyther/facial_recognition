from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

import cv2
from camera import Camera
import face_recognition
import requests
import re
import base64

request_database_url = 'http://localhost:8000/recognize/recog/'
true_frame = []
identity = None

# Create your views here.
def request_recognition(request):
    response = {}

    print('ENTERED REQUSEST_RECOGNITION')
    if true_frame != []:
        face_location = face_recognition.face_locations(true_frame)
        face_encoding = face_recognition.face_encodings(true_frame, face_location)[0]

        print(face_encoding)

        string_face_encoding = str(face_encoding).strip('[]')
        string_face_encoding = re.split(' ', string_face_encoding)
        end_string = ''

        for string in string_face_encoding:
            if string != '':
                end_string += string + '@'

        data_stream = end_string.encode("utf-8")
        end_string = base64.b64encode(data_stream)

        print(end_string)

        req = requests.get(request_database_url + end_string + '/').json()
        identity = response['identity'] = req['identity']
    else:
        response['identity'] = 'Error'

    print(response)
    return JsonResponse(response)



def return_stream(request):
    return  render(request, template_name='stream.html')

def generate_stream(request):
    return StreamingHttpResponse(gen(Camera()),
                content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    global true_frame
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
            if identity:
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, identity, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            true_frame = rgb_small_frame

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
