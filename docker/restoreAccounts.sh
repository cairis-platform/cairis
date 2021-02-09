#!/bin/bash

mysql -h cairis-mysql --user=root --password=$1 <<!
load data infile '/tmp/auth_user' into table cairis_user.auth_user;
!
