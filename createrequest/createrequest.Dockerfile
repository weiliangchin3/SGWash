FROM python:3-slim
WORKDIR /usr/src/app
COPY createrequest/requirements.txt ./
COPY createrequest/amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY createrequest/createrequest.py ./
COPY createrequest/invokes.py ./
COPY createrequest/amqp_setup.py ./
CMD [ "python", "./createrequest.py" ]