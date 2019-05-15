FROM python:3.7

WORKDIR /usr/src/FaceRecogBackend

COPY requirements.txt ./
RUN apt-get update && apt-get install -y cmake
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000/tcp
EXPOSE 8000/udp

#CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]
