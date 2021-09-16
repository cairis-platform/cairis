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
#  specific language go
#
# Author: Shamal Faily


export UI_REPO=/tmp/cairis-ui
rm -rf $UI_REPO
apt-get install curl
curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt-get update && apt-get install -y yarn
git clone https://github.com/cairis-platform/cairis-ui $UI_REPO
yarn --cwd $UI_REPO install --ignore-engines
yarn --cwd $UI_REPO run build
cp -r $UI_REPO/dist $CAIRIS_SRC
