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

import sys
if (sys.version_info > (3,)):
  import http.client
else:
  import httplib
import imghdr
import os
import uuid

from werkzeug.datastructures import FileStorage

from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import CairisHTTPError
from cairis.data.CairisDAO import CairisDAO

__author__ = 'Robin Quetin'


class UploadDAO(CairisDAO):
  accepted_image_types = ['jpg', 'jpeg', 'png', 'bmp', 'gif']

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)
    b = Borg()
    self.image_dir = b.uploadDir

  def upload_image(self, file):
    """
    :type file: FileStorage
    """
    extension = os.path.splitext(file.filename)[1]
    f_name = str(uuid.uuid4()) + extension
    f_path = os.path.join(self.image_dir, f_name)

    try:
      file.save(f_path)
    except IOError:
      raise CairisHTTPError(
        status_code=http.client.CONFLICT,
        status='Unable to save image',
        message='Please check if the static web directory exists ' +
                'and if the application has permission to write in the directory',
      )

    if not os.path.exists(f_path):
      raise CairisHTTPError(
                status_code=http.client.CONFLICT,
                status='Image not found',
                message='The image could not be saved on the server. \
Please check the server configuration to fix this problem.'
       )
    img_format = imghdr.what(f_path)
    if not img_format or img_format not in self.accepted_image_types:
      os.remove(f_name)
      raise CairisHTTPError(
              status_code=http.client.CONFLICT,
              status='Unsupported file type',
              message='The provided image file is not supported by CAIRIS'
      )
    return f_name
