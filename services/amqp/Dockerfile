FROM python:3-slim
WORKDIR /src
COPY amqp_setup/amqp_setup.py .
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python", "amqp_setup.py"]

