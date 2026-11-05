FROM python:3.11

RUN apt-get update
RUN apt-get install -y build-essential curl git vim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt -r requirements-dev.txt

RUN apt-get clean

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.main:app"]
