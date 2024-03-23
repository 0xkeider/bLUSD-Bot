FROM python:3.12.2
ENV PYTHONUNBUFFERED=1

COPY .env .
COPY main.py .

RUN pip install python-dotenv requests discord web3 millify

CMD ["python", "./main.py"]

