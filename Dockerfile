FROM python:3.10.8

ENV PYTHONUNBUFFERED=1

ADD main.py .
ADD config.py .

RUN pip install requests discord web3 millify

CMD [ "python", "./main.py" ]