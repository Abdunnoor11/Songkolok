FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /songkolok/
RUN pip install -r requirements.txt
COPY . /songkolok/
