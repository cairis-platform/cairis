drop database if exists `cairis_user`;
create database if not exists `cairis_user`;

drop user if exists cairis_test;
create user if not exists 'cairis_test'@'%' identified by 'cairis_test';
grant usage on `cairis_test`.* to 'cairis_test'@'%' with max_queries_per_hour 0 max_connections_per_hour 0 max_updates_per_hour 0 max_user_connections 0;
flush privileges;

create database if not exists `cairis_test_default`;
grant all privileges on `cairis_test_default`.* to 'cairis_test'@'%';
set global max_sp_recursion_depth = 255;

alter database cairis_test_default default character set utf8;
alter database cairis_test_default default collate utf8_general_ci;

flush tables;
flush privileges;
