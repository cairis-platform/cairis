#!/bin/bash -x

CAIRIS_ROOT=$HOME/cairis
ROOTPW=$1

sudo systemctl stop cairis
sudo systemctl disable cairis

sudo apt-get -y install python3-dev build-essential mysql-server mysql-client graphviz docbook dblatex python3-pip python3-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python3-setuptools pandoc

sudo rm -rf $CAIRIS_ROOT
git clone https://github.com/cairis-platform/cairis $CAIRIS_ROOT

sudo pip3 install -r $CAIRIS_ROOT/requirements.txt

CMD1='flush privileges; use mysql; update user set authentication_string=PASSWORD("'
CMD2='") where User="root"; update user set plugin="mysql_native_password" where User="root";'
CMD="$CMD1$ROOTPW$CMD2"

sudo service mysql stop
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo /usr/bin/mysqld_safe --skip-grant-tables &
sleep 5
mysql -u root --execute="$CMD"
sudo pkill mysqld_safe
sudo pkill mysqld
sudo service mysql start

export PYTHONPATH=$CAIRIS_ROOT
$CAIRIS_ROOT/cairis/bin/quick_setup_headless.py --rootDir=$CAIRIS_ROOT/cairis --dbRootPassword=$ROOTPW --logLevel=debug 
source $HOME/.bashrc

sudo -E $CAIRIS_ROOT/cairis/bin/installUI.sh

SVCFILE="[Unit]\nDescription=cairisd\n\n[Service]\nUser=$USERNAME\nWorkingDirectory=$CAIRIS_ROOT\nEnvironment=\"CAIRIS_CFG=$HOME/cairis.cnf\"\nEnvironment=\"PYTHONPATH=\${PYTHONPATH}:$CAIRIS_ROOT\"\nExecStart=$CAIRIS_ROOT/cairis/bin/cairisd.py runserver\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target"
echo -e $SVCFILE | sudo tee /etc/systemd/system/cairis.service

sudo systemctl enable --now /etc/systemd/system/cairis.service

sudo shutdown -Fr now
