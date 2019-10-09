# Base image
FROM python:3.7.4-alpine

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add and install requirements pip
# COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install -r requirements.txt

# Add and install requiremenets pipenv
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock
RUN pipenv install --deploy --system

# Add app
COPY . /usr/src/app

# Run server
CMD python manage.py run -h 0.0.0.0