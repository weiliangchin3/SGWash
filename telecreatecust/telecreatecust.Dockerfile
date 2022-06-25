FROM python:3-slim
WORKDIR /usr/src/app
COPY telecreatecust/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
COPY telecreatecust/telecreatecust.py ./
CMD [ "python", "./telecreatecust.py" ]