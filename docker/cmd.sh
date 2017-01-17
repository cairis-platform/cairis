#!/bin/bash
set -e
service mysql start
mysql -h localhost -u root <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
/cairis/cairis/bin/cairisd.py runserver
