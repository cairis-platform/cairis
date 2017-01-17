#!/bin/bash
set -e
. .profile
service mysql start
/cairis/cairis/bin/cairisd.py runserver
