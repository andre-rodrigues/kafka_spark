FROM python:3

WORKDIR /app

# Install Java
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean;

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./load_kafka_topic_to_csv_file.py" ]
