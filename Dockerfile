FROM python:3.10-slim

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential ffmpeg && \
    apt-get clean

WORKDIR /App
COPY ./cluefulbot ./cluefulbot
COPY ./main.py .
COPY ./requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-OO", "-u", "main.py"]
