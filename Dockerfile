FROM python:3.10.8

ENV PYTHONUNBUFFERED=1

ADD main.py .
ADD .env .

RUN pip install python-dotenv requests discord web3 millify

CMD [ "python", "./main.py" ]