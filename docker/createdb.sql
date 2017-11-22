create database if not exists `cairis_user`;
grant usage on *.* to 'cairisuser'@'%' identified by 'cairisuser' with max_queries_per_hour 0 max_connections_per_hour 0 max_updates_per_hour 0 max_user_connections 0;
create database if not exists `cairis_default`;
grant all privileges on `cairis_default`.* to 'cairisuser'@'%';
set global max_sp_recursion_depth = 255;
alter database cairis_default default character set utf8;
alter database cairis_default default collate utf8_general_ci;
flush tables;
flush privileges;
