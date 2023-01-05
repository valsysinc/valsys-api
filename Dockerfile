
FROM python:3.8.9 
ADD . /valsys
WORKDIR /valsys
ENV VALSYS_API_SOCKET=wss://api.valsys.io
ENV VALSYS_API_SERVER=https://api.valsys.io
ENV VALSYS_API_USER=simon.bessey@valsys.io
ENV VALSYS_API_PASSWORD=Absyks_1234

RUN pip install -r requirements.txt
