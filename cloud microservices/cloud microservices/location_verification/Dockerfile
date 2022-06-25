FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app.py .

# command for local container
#CMD ["python", "app.py"]

# command for container hosted on google cloud run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app