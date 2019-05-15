from django.shortcuts import render
from django.http.response import JsonResponse
from Recognizer.models import User

import face_recognition
import numpy as np
import base64

# Create your views here.
def return_database_info():
    known_names = []
    known_face_encodings = []

    if User.objects.exclude(name='Unknown') != None:
        for user in User.objects.exclude(name='Unknown'):
            known_names.append(user.name)
            known_face_encodings.append(user.face_encoding)

    return known_names, known_face_encodings


def return_recognition_result(request, face_encoding):
    known_names , known_face_encodings = return_database_info()

    decoded_face_encoding = base64.decode(face_encoding)
    decoded_face_encoding = decoded_face_encoding.decode()

    face_encoding = np.fromstring(decoded_face_encoding, sep='@')

    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    # If a match was found in known_face_encodings, just use the first one.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_names[first_match_index]

    response = {}
    response['name'] = name

    return JsonResponse(response)