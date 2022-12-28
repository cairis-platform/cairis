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
DEFUSER=$2
DEFPASSWD=$3
HOMEDIR=$4

if [ -z $1 ]
then
  ROOTPW=my-secret-pw
fi

if [ -z $2 ]
then
  DEFUSER=test@test.com
fi

if [ -z $3 ]
then
  DEFPASSWD=test
fi

if [ -z $3 ]
then
  HOMEDIR=$HOME
fi

CAIRIS_ROOT=$HOMEDIR/cairis
export CAIRIS_SRC=$CAIRIS_ROOT/cairis

echo "ROOTPW: " $ROOTPW "DEFUSER: " $DEFUSER "DEFPASSWD: " $DEFPASSWD

sudo systemctl stop cairis
sudo systemctl disable cairis

sudo apt-get -y install python3-dev build-essential mysql-server mysql-client graphviz docbook dblatex python3-pip python3-mysqldb python3-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python3-setuptools pandoc

sudo rm -rf $CAIRIS_ROOT
git clone https://github.com/cairis-platform/cairis $CAIRIS_ROOT
sudo -E $CAIRIS_ROOT/cairis/bin/installUI.sh

sudo pip3 install wheel
sudo pip3 install -r $CAIRIS_ROOT/requirements.txt

echo -e "[mysqld]\nthread_stack = 256K\nmax_sp_recursion_depth = 255\nlog_bin_trust_function_creators = 1" | sudo tee /etc/mysql/conf.d/mysql.cnf

CMD1='flush privileges; set global log_bin_trust_function_creators = 1; flush privileges;  use mysql; update user set plugin="mysql_native_password" where User="root"; flush privileges; alter user "root"@"localhost" identified by "'
CMD2='"'
CMD="$CMD1$ROOTPW$CMD2"

sudo service mysql stop
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo /usr/bin/mysqld_safe --skip-grant-tables &
sleep 10
mysql -u root --execute="$CMD"
sudo pkill mysqld_safe
sudo pkill mysqld
sudo service mysql start
sleep 10

export PYTHONPATH=$CAIRIS_ROOT
$CAIRIS_ROOT/cairis/bin/quick_setup_headless.py --rootDir=$CAIRIS_ROOT/cairis --dbRootPassword=$ROOTPW --logLevel=debug --user=$DEFUSER --password=$DEFPASSWD --configFile=$HOMEDIR/cairis.cnf

SVCFILE="[Unit]\nDescription=cairisd\n\n[Service]\nEnvironment=\"FLASK_APP=$CAIRIS_ROOT/cairis/daemon:create_app\"\nEnvironment=\"FLASK_ENV=development\"\nUser=$USERNAME\nWorkingDirectory=$CAIRIS_ROOT\nEnvironment=\"CAIRIS_CFG=$HOMEDIR/cairis.cnf\"\nEnvironment=\"PYTHONPATH=\${PYTHONPATH}:$CAIRIS_ROOT\"\nExecStart=flask run --host 0.0.0.0 --port 7071\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target"

echo -e $SVCFILE | sudo tee /etc/systemd/system/cairis.service

sudo systemctl enable /etc/systemd/system/cairis.service

echo "alias update_cairis=\"sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && curl -s https://cairis.org/quickInstall.sh | bash -s $ROOTPW $DEFUSER $DEFPASSWD $HOMEDIR\"" >> $HOMEDIR/.bashrc

sudo shutdown -Fr now
