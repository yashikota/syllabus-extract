FROM mcr.microsoft.com/playwright:v1.42.0-jammy

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

COPY . /
RUN pip3 install -r requirements.txt
