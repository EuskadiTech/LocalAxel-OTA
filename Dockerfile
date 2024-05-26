FROM python:3
ENV DATA_PATH=/data/

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY OTA/LocalAxel_Dist/start.py start.py
COPY OTA/LocalAxel_Dist/utils.py utils.py

CMD [ "python", "./start.py" ]