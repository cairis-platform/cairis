#!/bin/sh
set -x

export REPOS_DIR=/tmp
export CAIRIS_REPO=$REPOS_DIR/cairis

rm -rf $CAIRIS_REPO

git clone http://github.com/cairis-platform/cairis $CAIRIS_REPO

sudo docker stop CAIRIS
sudo docker stop cairis-mysql
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -q)
sudo docker volume rm $(docker volume ls)
sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest --thread_stack=512K
sudo docker run --name cairis-docs -d -v cairisDocumentation:/tmpDocker -v cairisImage:/images -t shamalfaily/cairis-docs
sudo docker run --name CAIRIS -d --link cairis-mysql:mysql --link cairis-docs:docs -P -p 80:8000 --net=bridge -v cairisDocumentation:/tmpDocker -v cairisImage:/images shamalfaily/cairis

sleep 60

# Make sure the requests and argparse packages are installed before running model_import_web.py or web_cimport.py.
$CAIRIS_REPO/cairis/bin/model_import_web.py --url http://localhost --database NeuroGrid $CAIRIS_REPO/examples/exemplars/NeuroGrid.cairis
$CAIRIS_REPO/cairis/bin/model_import_web.py --url http://localhost --database ACME_Water $CAIRIS_REPO/examples/exemplars/ACME_Water.cairis
$CAIRIS_REPO/cairis/bin/model_import_web.py --url http://localhost --database webinos $CAIRIS_REPO/examples/exemplars/webinos.cairis
