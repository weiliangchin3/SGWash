FROM python:3.8-slim
WORKDIR /usr/src/app
COPY invoicereq/requirements.txt ./
COPY invoicereq/amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY invoicereq/invoicereq.py ./
COPY invoicereq/emailService.py ./
COPY invoicereq/invoice.py ./
COPY invoicereq/sendEmailAPI.py ./
COPY invoicereq/token_gmail_v1.pickle ./
COPY invoicereq/client_secret.json ./
COPY invoicereq/amqp_setup.py ./

CMD [ "python", "./invoicereq.py" ]

# command for cloud
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app