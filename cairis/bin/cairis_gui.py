#!/usr/bin/env python
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

import os
import sys

def main(args=None):
  if args is None:
    args = sys.argv[1:]
    cairisApp = IRISApp()
    cairisApp.MainLoop()

if __name__ == '__main__':
  try:
    import gtk
    gtk.remove_log_handlers()
    from cairis.gui.IRISApp import IRISApp
    from cairis.core.ARM import ARMException
    main()
  except ImportError, e:
    print "Fatal CAIRIS error: " + str(e) 
    sys.exit(-1)
  except ARMException, e:
    print "Fatal CAIRIS error: " + str(e) 
    sys.exit(-1)
