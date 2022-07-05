
FROM python:3.8.9 
ADD . /valsys
WORKDIR /valsys
RUN pip install -r requirements.txt
