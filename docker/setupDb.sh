#!/bin/bash
set -e
service mysql start
/cairis/cairis/test/initdb.sh
/cairis/cairis/bin/add_cairis_user.py test test
mysql -h localhost -u root <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
