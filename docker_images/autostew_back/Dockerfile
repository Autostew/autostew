# This dockerfile is used to run the autostew webserver

FROM ubuntu:14.04
Maintainer Michael Wittig <witmic1@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

COPY dependencies.sh dependencies.sh

# install all dependencies
RUN ./dependencies.sh

WORKDIR /autostew
VOLUME ["autostew/settings"]
VOLUME ["autostew_back/settings"]

ENV DJANGO_SETTINGS_MODULE=autostew.settings.prod
ENV SETTINGS_FILE=alpha

CMD /autostew/autostew_back.py -s $SETTINGS_FILE
