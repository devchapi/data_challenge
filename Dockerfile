FROM python:3.10-slim

#working dir
WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Install packages requirements.txt
RUN pip install --no-cache-dir --verbose -r requirements.txt

EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "app.py"]