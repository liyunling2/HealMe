FROM python:3-slim
WORKDIR /src
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
CMD ["python", "log.py"]