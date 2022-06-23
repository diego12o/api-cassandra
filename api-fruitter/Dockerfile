FROM python:3.8-slim-buster

EXPOSE 5000

WORKDIR /app

COPY . .

RUN pip3 install flask \
cassandra-driver

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]