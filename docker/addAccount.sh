#!/bin/bash

export CAIRIS_SRC=/cairis/cairis
export PYTHONPATH=/cairis
export CAIRIS_CFG=/cairis.cnf

USERNAME=$1
PASSWD=$2
FULLNAME=$3

$CAIRIS_SRC/bin/add_cairis_user.py $USERNAME $PASSWD $FULLNAME
