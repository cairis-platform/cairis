#!/bin/bash
set -x

mysql --user=cairis_test --password=cairis_test --database=cairis_test_default < /sql/init.sql
mysql --user=cairis_test --password=cairis_test --database=cairis_test_default < /sql/procs.sql
mysql --user=root --password=my-secret-pw <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!

# Set status
touch /var/lib/mysql/db_init_done
