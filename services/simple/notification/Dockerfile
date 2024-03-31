FROM python:3-slim
WORKDIR /src
COPY requirements.txt .
ENV PYTHONUNBUFFERED=1
RUN python3 -m pip install -r requirements.txt
CMD ["python", "notifiAMQP.py"]