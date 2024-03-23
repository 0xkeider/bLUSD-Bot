FROM python:3.12.2
ENV PYTHONUNBUFFERED=1

COPY .env .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "./main.py"]