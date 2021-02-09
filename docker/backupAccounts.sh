#!/bin/bash

mysql -h cairis-mysql --user=root --password=$1 <<!
select id,email,account,password,dbtoken,name,active,fs_uniquifier,confirmed_at into outfile '/tmp/auth_user' from cairis_user.auth_user;
!
