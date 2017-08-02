#!/bin/bash
set -x
mysql -h cairis-mysql --user=root --password=my-secret-pw < createdb.sql
mysql -h cairis-mysql --user=cairisuser --password=cairisuser --database=cairis_default < $CAIRIS_SRC/sql/init.sql
mysql -h cairis-mysql --user=cairisuser --password=cairisuser --database=cairis_default < $CAIRIS_SRC/sql/procs.sql
/cairis/cairis/bin/add_cairis_user.py test test
mysql -h cairis-mysql --user=root --password=my-secret-pw <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
mod_wsgi-express start-server /cairis/cairis/bin/cairis.wsgi --user www-data --group www-data
