#!/bin/bash
set -e
service mysql start
mysql -h localhost -u root <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
mod_wsgi-express start-server /cairis/cairis/bin/cairis.wsgi --user www-data --group www-data
