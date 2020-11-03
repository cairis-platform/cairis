/* 
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
*/

drop database if exists `cairis_user`;
create database if not exists `cairis_user`;

drop database if exists `cairis_owner`;
create database if not exists `cairis_owner`;
create table cairis_owner.db_owner(db varchar(64), owner varchar(32), primary key(db,owner)) engine=innodb;

drop user if exists cairis_test;
create user if not exists 'cairis_test'@'%' identified by 'cairis_test';
grant usage on `cairis_test`.* to 'cairis_test'@'%';
flush privileges;

drop database if exists `cairis_test_default`;
create database if not exists `cairis_test_default`;
grant all privileges on `cairis_test_default`.* to 'cairis_test'@'%';
set global max_sp_recursion_depth = 255;

alter database cairis_test_default default character set utf8mb4;
alter database cairis_test_default default collate utf8mb4_0900_ai_ci;

flush tables;
flush privileges;
