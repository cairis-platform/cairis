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

import logging
import os
import urllib
from StringIO import StringIO
import jsonpickle
from cairis.web_tests.CairisTests import CairisTests

__author__ = 'Robin Quetin'


class UploadTests(CairisTests):
    logger = logging.getLogger(__name__)

    def test_image_upload(self):
        method = 'test_image_upload'
        name, request = urllib.urlretrieve('http://high-resolution-photos.com/stock_photos/royalty_free_3.jpg')
        if name and os.path.exists(name):
            fs_image = open(name, 'rb')
            image_bytes = fs_image.read()
            rv = self.app.post('/api/upload/image?session_id=test', data={
                'file': (StringIO(image_bytes), name),
            })
            self.logger.info('[%s] Response data: %s', method, rv.data)
            json_dict = jsonpickle.decode(rv.data)
            self.assertTrue(json_dict.has_key('filename'), 'Image was not saved on the server')
        else:
            self.fail('Image could not be downloaded from the Internet.')

    def test_big_image_upload(self):
        method = 'test_big_image_upload'
        self.logger.info('[%s] Downloading a big image. This could take a while...', method)
        name, request = urllib.urlretrieve('http://upload.wikimedia.org/wikipedia/commons/d/d4/Nature_landscape_ukraine_poltava_(8093169218).jpg')
        if name and os.path.exists(name):
            fs_image = open(name, 'rb')
            image_bytes = fs_image.read()
            rv = self.app.post('/api/upload/image?session_id=test', data={
                'file': (StringIO(image_bytes), name),
            })
            self.logger.info('[%s] Response data: %s', method, rv.data)
