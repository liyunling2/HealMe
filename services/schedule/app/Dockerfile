FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
# COPY . .
RUN python3 -m pip install -r requirements.txt
CMD ["python", "src/run.py"]