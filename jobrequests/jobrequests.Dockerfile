FROM python:3-slim
WORKDIR /usr/src/app
COPY jobrequests/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY jobrequests/jobrequests.py ./
CMD [ "python", "./jobrequests.py" ]