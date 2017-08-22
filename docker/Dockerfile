FROM ubuntu:zesty
MAINTAINER Shamal Faily <sfaily@bournemouth.ac.uk>
RUN apt-get update && apt-get install -y python-dev build-essential mysql-client graphviz python-pip python-numpy git libmysqlclient-dev docbook python-apt dblatex texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev libxslt1-dev apache2-threaded-dev poppler-utils
COPY requirements.txt /
COPY wsgi_requirements.txt /
RUN pip install -r requirements.txt
RUN pip install -r wsgi_requirements.txt
ENV CAIRIS_SRC=/cairis/cairis
ENV CAIRIS_CFG_DIR=/cairis/docker
ENV CAIRIS_CFG=cairis.cnf
ENV PYTHONPATH=/cairis
RUN mkdir /images
RUN chown www-data /images
RUN chgrp www-data /images
RUN git clone https://github.com/failys/cairis /cairis
COPY cairis.cnf /
COPY setupDb.sh /
COPY createdb.sql /
EXPOSE 8000
CMD ["./setupDb.sh"]
