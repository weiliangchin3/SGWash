FROM python:3-slim
WORKDIR /usr/src/app
COPY job/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
COPY job/job.py ./
COPY job/invokes.py ./
CMD [ "python", "./job.py" ]