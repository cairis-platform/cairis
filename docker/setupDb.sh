#!/bin/bash
set -x
mysql -h cairis-mysql --user=root --password=my-secret-pw < createdb.sql
mysql -h cairis-mysql --user=cairis_test --password=cairis_test --database=cairis_test_default < $CAIRIS_SRC/sql/init.sql
mysql -h cairis-mysql --user=cairis_test --password=cairis_test --database=cairis_test_default < $CAIRIS_SRC/sql/procs.sql
mysql -h cairis-mysql --user=root --password=my-secret-pw <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
chown www-data /images
chgrp www-data /images
chmod 1777 /tmpDocker
mod_wsgi-express start-server /cairis/cairis/bin/cairis.wsgi --user www-data --group www-data
