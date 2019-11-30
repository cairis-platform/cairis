FROM ubuntu:latest
MAINTAINER Shamal Faily <admin@cairis.org>
RUN apt-get update 
RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN apt-get install -y mysql-client
RUN apt-get install -y graphviz
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-numpy
RUN apt-get install -y python3-mysqldb
RUN apt-get install -y git
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y python-apt
RUN apt-get install -y libxml2-dev
RUN apt-get install -y libxslt1-dev 
RUN apt-get install -y libssl-dev 
RUN apt-get install -y apache2
RUN apt-get install -y apache2-dev
RUN apt-get install -y poppler-utils
RUN apt-get install -y apt-transport-https 
RUN apt-get install -y ca-certificates

RUN pip3 install wheel
COPY requirements.txt /
COPY wsgi_requirements.txt /
RUN pip3 install -r requirements.txt
RUN pip3 install -r wsgi_requirements.txt
ENV CAIRIS_SRC=/cairis/cairis
ENV CAIRIS_CFG_DIR=/cairis/docker
ENV CAIRIS_CFG=cairis.cnf
ENV PYTHONPATH=/cairis

RUN mkdir /tmpDocker
RUN mkdir /images

RUN git clone --depth 1 -b master https://github.com/cairis-platform/cairis /cairis
RUN mkdir /cairisTmp
RUN mv /cairis/cairis /cairisTmp/cairis
RUN rm -rf /cairis/
RUN mv /cairisTmp/ /cairis/

COPY cairis.cnf /
COPY setupDb.sh /
COPY createdb.sql /
COPY addAccount.sh /

RUN /cairis/cairis/bin/installUI.sh

EXPOSE 8000

RUN apt-get remove --purge -y git
RUN apt-get autoremove -y

CMD ["./setupDb.sh"]
