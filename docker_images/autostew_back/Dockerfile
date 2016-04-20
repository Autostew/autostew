# This dockerfile is used to run the autostew webserver

FROM ubuntu:14.04
Maintainer Michael Wittig <witmic1@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

COPY dependencies.sh dependencies.sh

# install all dependencies
RUN ./dependencies.sh

COPY run_autostew_back.sh autostew/run_autostew_back.sh

WORKDIR /autostew
VOLUME ["autostew/settings"]

ENV DJANGO_SETTINGS_MODULE=autostew.settings.prod
ENV BRANCH=master
ENV SERVER_ID=1

CMD ./run_autostew_back.sh $BRANCH $SERVER_ID
