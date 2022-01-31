FROM python:3.10-slim

WORKDIR /App
COPY ./cluefulbot ./cluefulbot
COPY ./requirements.txt .
COPY ./main.py .

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]