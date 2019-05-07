FROM python:3.7

WORKDIR /usr/src/FaceRecogInterface

COPY requirements.txt ./
RUN apt-get update && apt-get install -y cmake
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001/tcp
EXPOSE 8001/udp

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8001", "--noreload" ]
