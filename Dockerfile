# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /ordersscript

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# expose ports
EXPOSE 80

# copy project
COPY . .

# run
CMD ['python', '-m', 'flask', 'run']