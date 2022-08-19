FROM ubuntu:latest
MAINTAINER Shamal Faily <admin@cairis.org>
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y build-essential \
    python3-dev \
    mysql-client \ 
    graphviz \
    python3-pip \
    python3-numpy \
    python3-mysqldb \
    git \
    default-libmysqlclient-dev \
    python3-apt \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    apache2 \
    apache2-dev \
    poppler-utils \
    python3-setuptools \
    apt-transport-https \
    ca-certificates

RUN pip3 install wheel
#Installing Python modules
COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY wsgi_requirements.txt /
RUN pip3 install -r wsgi_requirements.txt

#Environment Variable starts from here
ENV CAIRIS_SRC=/cairis/cairis
ENV CAIRIS_CFG_DIR=/cairis/docker
ENV CAIRIS_CFG=/cairis.cnf
ENV PYTHONPATH=/cairis

RUN mkdir /tmpDocker
RUN mkdir /images

#Clonning the repo
RUN git clone --depth 1 -b master https://github.com/cairis-platform/cairis /cairis
#creating folder here and moving the files and folder

RUN mkdir /cairisTmp &&\
    mv /cairis/cairis /cairisTmp/cairis &&\
    rm -rf /cairis/ &&\
    mv /cairisTmp/ /cairis/

COPY cairis.cnf /
COPY setupDb.sh /
COPY createdb.sql /
COPY addAccount.sh /
COPY register_user.html /cairis/cairis/daemon/templates/security

RUN /cairis/cairis/bin/installUI.sh

EXPOSE 8000

RUN apt-get remove --purge -y git
RUN apt-get autoremove -y

CMD ["./setupDb.sh"]
