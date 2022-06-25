FROM python:3-slim
WORKDIR /usr/src/app
COPY request/requirements.txt ./
COPY request/amqp.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY request/request.py ./
COPY request/invokes.py ./
COPY request/amqp_setup.py ./
CMD [ "python", "./request.py" ]