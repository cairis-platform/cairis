#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from flask_security import UserMixin, RoleMixin
from .cdb import db

__author__ = 'Robin Quetin, Shamal Faily'

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('auth_role.id')))
#db_owner = db.Table('db_owner', db.Column('db',db.String(64)), db.Column('owner', db.String(32)))
#db_token = db.Table('db_token', db.Column('email',db.String(255), unique=True), db.Column('token',db.String(255)))


class Role(db.Model, RoleMixin):
  __tablename__ = 'auth_role'
  id = db.Column(db.Integer(), primary_key=True) 
  name = db.Column(db.String(80), unique=True) 
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  __tablename__ = 'auth_user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True) 
  account = db.Column(db.String(32), unique=True) 
  password = db.Column(db.String(255))
  name = db.Column(db.String(255)) 
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
