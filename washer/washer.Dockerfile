FROM python:3-slim
WORKDIR /usr/src/app
COPY washer/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY washer/washer.py ./
CMD [ "python", "./washer.py" ]