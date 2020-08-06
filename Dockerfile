FROM python:3.8
copy config.cfg /app/config.cfg
copy py-ecobee-mqtt.py /app/py-ecobee-mqtt.py
copy requirements.txt /app/requirements.txt
RUN mkdir /app/db
RUN mkdir /app/log
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/py-ecobee-mqtt.py"]