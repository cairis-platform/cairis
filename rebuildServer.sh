#!/bin/bash -x
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


ROOTPW=$1
MAILSVR=$2
MAILPORT=$3
MAILUSER=$4
MAILPASSWD=$5
CAIRIS_ACCOUNT=$6
CAIRIS_HOME=$7

CAIRIS_ROOT=$CAIRIS_HOME/cairis
export CAIRIS_SRC=$CAIRIS_ROOT/cairis

export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config
export CAIRIS_CFG=/home/sfaily/cairis.cnf


sudo systemctl stop cairis
sudo systemctl disable cairis

sudo rm /var/lib/mysql-files/auth_user

mysql -h localhost --user=root --password=$ROOTPW <<!
select id,email,account,password,dbtoken,name,active,confirmed_at into outfile '/var/lib/mysql-files/auth_user' from cairis_user.auth_user;
!

sudo apt-get -y install python3-dev build-essential mysql-server mysql-client graphviz docbook dblatex python3-pip python3-mysqldb python3-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev apache2 apache2-dev poppler-utils python3-setuptools pandoc apt-transport-https ca-certificates

sudo rm -rf $CAIRIS_ROOT
git clone https://github.com/cairis-platform/cairis $CAIRIS_ROOT
sudo -E $CAIRIS_ROOT/cairis/bin/installUI.sh

sudo pip3 install -r $CAIRIS_ROOT/requirements.txt
sudo pip3 install -r $CAIRIS_ROOT/wsgi_requirements.txt

export PYTHONPATH=$CAIRIS_ROOT
$CAIRIS_ROOT/cairis/bin/server_setup_headless.py --rootDir=$CAIRIS_ROOT/cairis --configFile=$CAIRIS_HOME/cairis.cnf --webPort=8000 --dbRootPassword=$ROOTPW --logLevel=debug --mailServer=$MAILSVR --mailPort=$MAILPORT --mailUser=$MAILUSER --mailPasswd=$MAILPASSWD

SVCFILE="[Unit]\nDescription=cairisd\n\n[Service]\nUser=$CAIRIS_ACCOUNT\nWorkingDirectory=$CAIRIS_ROOT\nEnvironment=\"CAIRIS_CFG=$CAIRIS_HOME/cairis.cnf\"\nEnvironment=\"PYTHONPATH=\${PYTHONPATH}:$CAIRIS_ROOT\"\nExecStart=mod_wsgi-express start-server $CAIRIS_ROOT/cairis/bin/cairis.wsgi --user www-data --group www-data\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target"
echo -e $SVCFILE | sudo tee /etc/systemd/system/cairis.service

sudo systemctl enable /etc/systemd/system/cairis.service

mysql -h localhost --user=root --password=$ROOTPW <<!
load data infile '/var/lib/mysql-files/auth_user' into table cairis_user.auth_user;
!

$CAIRIS_ROOT/cairis/bin/reset_cairis_user.py --reload 1 all

sudo shutdown -Fr now
