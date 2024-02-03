
FROM python:3.9-slim

WORKDIR /gateway/flaskr/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "flaskr/app.py"]
