#!/bin/bash
set -e
service mysql start
/cairis/cairis/bin/cairisd.py runserver
