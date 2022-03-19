FROM python:3.6-slim

RUN apt-get update 
RUN apt-get install -y docbook \
    docbook-utils \
    dblatex \
    texlive-latex-extra \
    inkscape \
    pandoc \
    git \
    python3-pip

# Installing Flask    
RUN pip3 install Flask

#Creating Library
RUN mkdir /latex

#Copying file to folder latex
COPY LaTeXApi.py /latex
RUN touch __init__.py &&\
    git clone --depth 1 -b master https://github.com/cairis-platform/cairis /cairis

RUN mkdir -p /cairisTmp/cairis

RUN mv /cairis/cairis/config /cairisTmp/cairis &&\
    mv /cairis/cairis/core/armid.py /latex/armid.py &&\
    rm -rf /cairis &&\
    mv /cairisTmp /cairis

RUN apt-get remove --purge -y git
RUN apt-get autoremove -y

EXPOSE 5000

CMD ["./latex/LaTeXApi.py"]
