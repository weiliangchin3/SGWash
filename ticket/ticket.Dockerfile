FROM python:3.8-slim

WORKDIR /usr/src/app
COPY ticket/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ticket/ticket.py .
CMD [ "python", "./ticket.py" ]
# command for local container
#CMD ["python", "app.py"]

# command for container hosted on google cloud run
