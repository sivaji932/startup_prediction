FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r reqiurements.txt

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]