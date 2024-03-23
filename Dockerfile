FROM python:3.12.2
ENV PYTHONUNBUFFERED=1

COPY .env .
COPY requirements.txt .
COPY main.py .

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]