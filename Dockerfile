FROM homeassistant/home-assistant:latest

WORKDIR /tools

ADD . /tools
RUN pip install pycat
RUN apt install netcat

RUN python manage.py collectstatic --noinput -c
