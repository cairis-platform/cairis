FROM debian:bookworm-slim
# Pin to Bookworm (Python 3.11). CAIRIS uses imghdr, which was removed in Python 3.13+.
LABEL maintainer="Shamal Faily <admin@cairis.org>"
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    default-mysql-client \
    graphviz \
    python3-pip \
    python3-numpy \
    python3-mysqldb \
    git \
    default-libmysqlclient-dev \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    libmagic1 \
    apache2 \
    apache2-dev \
    poppler-utils \
    python3-setuptools \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY docker/requirements.txt docker/wsgi_requirements.txt /
RUN pip3 install wheel --break-system-packages \
    && pip3 install -r requirements.txt --break-system-packages
RUN pip3 install -r wsgi_requirements.txt --break-system-packages

ENV CAIRIS_SRC=/cairis/cairis \
    CAIRIS_CFG_DIR=/cairis/docker \
    CAIRIS_CFG=/cairis.cnf \
    PYTHONPATH=/cairis

RUN mkdir /tmpDocker /images

#Clonning the repo
RUN git clone --depth 1 -b master https://github.com/cairis-platform/cairis /cairis
#creating folder here and moving the files and folder

RUN mkdir /cairisTmp &&\
    mv /cairis/cairis /cairisTmp/cairis &&\
    rm -rf /cairis/ &&\
    mv /cairisTmp/ /cairis/

COPY \
    docker/cairis.cnf \
    docker/setupDb.sh \
    docker/createdb.sql \
    docker/addAccount.sh \
    /
COPY cairis/bin/installUI.sh /cairis/cairis/bin/installUI.sh
COPY docker/register_user.html /cairis/cairis/daemon/templates/security

RUN chmod +x /cairis/cairis/bin/installUI.sh \
    && /cairis/cairis/bin/installUI.sh

RUN apt-get remove --purge -y git \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["./setupDb.sh"]
