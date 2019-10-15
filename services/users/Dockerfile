FROM python:3.7.4-slim

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip && \
    pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --deploy --system

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app

CMD ["/usr/src/app/entrypoint.sh"]