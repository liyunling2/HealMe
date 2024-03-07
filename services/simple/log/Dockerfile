FROM python:3-slim
WORKDIR /usr
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/log.py ./
CMD [ "python", "src/log.py" ]