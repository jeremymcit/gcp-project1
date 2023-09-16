FROM python:3.10.7-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY project1-flet.py project1-flet.py

RUN pip3 install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3", "project1-flet.py"]