FROM python:2.7-slim

RUN apt-get update 
RUN apt-get install -y docbook
RUN apt-get install -y docbook-utils
RUN apt-get install -y dblatex
RUN apt-get install -y texlive-latex-extra
RUN apt-get install -y inkscape
RUN apt-get install -y git

RUN pip install Flask
RUN mkdir /latex
COPY LaTeXApi.py /latex
RUN touch __init__.py
RUN git clone --depth 1 -b master https://github.com/failys/cairis /cairis

RUN mkdir -p /cairisTmp/cairis
RUN mv /cairis/cairis/config /cairisTmp/cairis
RUN mv /cairis/cairis/web /cairisTmp/cairis
RUN mv /cairis/cairis/core/armid.py /latex/armid.py
RUN rm -rf /cairis
RUN mv /cairisTmp /cairis

RUN apt-get remove --purge -y git
RUN apt-get autoremove -y

EXPOSE 5000

CMD ["./latex/LaTeXApi.py"]
