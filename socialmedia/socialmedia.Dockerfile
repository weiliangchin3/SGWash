FROM python:3-slim
WORKDIR /usr/src/app
COPY socialmedia/requirements.txt ./
COPY socialmedia/uploadimg.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
COPY socialmedia/socialmedia.py ./
CMD [ "python", "./socialmedia.py" ]