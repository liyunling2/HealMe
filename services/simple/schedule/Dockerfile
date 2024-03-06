FROM python:3-slim
WORKDIR /src
COPY requirements.txt .
# COPY . .
RUN python3 -m pip install -r requirements.txt
CMD ["python", "run.py"]