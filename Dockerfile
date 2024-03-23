FROM python:3.12.2

ENV PYTHONUNBUFFERED=1

COPY .env .
COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]