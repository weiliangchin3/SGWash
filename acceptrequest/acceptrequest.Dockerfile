FROM python:3-slim
WORKDIR /usr/src/app
COPY acceptrequest/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
COPY acceptrequest/acceptrequest.py ./
COPY acceptrequest/invokes.py ./
CMD [ "python", "./acceptrequest.py" ]