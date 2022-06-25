FROM python:3-slim
WORKDIR /usr/src/app
COPY customer/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY customer/customer.py ./
CMD [ "python", "./customer.py" ]