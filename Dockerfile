FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["python", "src/main.py"]