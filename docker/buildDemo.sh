#!/bin/sh
set -x

export REPOS_DIR=/tmp
export CAIRIS_REPO=$REPOS_DIR/cairis

rm -rf $CAIRIS_REPO

git clone http://github.com/failys/cairis $CAIRIS_REPO

sudo docker stop CAIRIS
sudo docker stop cairis-mysql
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -q)
sudo docker volume rm $(docker volume ls)
sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
sudo docker run --name cairis-docs -d -v cairisDocumentation:/tmpDocker -v cairisImage:/images -t shamalfaily/cairis-docs
sudo docker run --name CAIRIS -d --link cairis-mysql:mysql --link cairis-docs:docs -P -p 80:8000 --net=bridge -v cairisDocumentation:/tmpDocker -v cairisImage:/images shamalfaily/cairis

sleep 60

# Make sure the requests and argparse packages are installed before running model_import_web.py or web_cimport.py.
$CAIRIS_REPO/cairis/bin/model_import_web.py --url http://localhost --database NeuroGrid --image_dir $CAIRIS_REPO/examples/exemplars/NeuroGrid --rich_pic NeuroGridContext.jpg $CAIRIS_REPO/examples/exemplars/NeuroGrid/NeuroGrid.xml
$CAIRIS_REPO/cairis/bin/web_cimport.py --url http://localhost --database NeuroGrid --type locations $CAIRIS_REPO/examples/exemplars/NeuroGrid/ComLab.xml
$CAIRIS_REPO/cairis/bin/model_import_web.py --url http://localhost --database ACME_Water --image_dir $CAIRIS_REPO/examples/exemplars/ACME_Water --rich_pic stcsContext.jpg $CAIRIS_REPO/examples/exemplars/ACME_Water/ACME_Water.xml
$CAIRIS_REPO/cairis/bin/web_cimport.py --url http://localhost --database ACME_Water --type locations $CAIRIS_REPO/examples/exemplars/ACME_Water/PooleWWTW.xml

# Uncomment below lines if you want to add webinos to the live demo
#rm -rf $WEBINOS_DESIGN_DATA_REPO
#export WEBINOS_DESIGN_DATA_REPO=$REPOS_DIR/webinos-design-data
#git clone http://github.com/webinos/webinos-design-data $WEBINOS_DESIGN_DATA_REPO

# The regeneration script converts spreadsheets and dot files to CAIRIS models, but you need to install some pre-requisite packages first.  These install fine on Linux, but are problematic to install on Mac OS X.  I haven't tested this script on Windows.
# sudo pip install --upgrade pydot certifi openpyxl requests jsonpickle argparse urllib uno

#$WEBINOS_DESIGN_DATA_REPO/scripts/regenerate_webservices.sh
