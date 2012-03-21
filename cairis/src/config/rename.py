#!/usr/bin/python
#$URL$ $Id$

import sys
import string
import os

def moveBack(fileName):
  cmd = 'mv ' + fileName + '.1 ' + fileName
  os.system(cmd)

def rename(fromName,toName,fileName):
  cmd = 'sed \'s/' + fromName + '/' + toName + '/g\' ' + fileName + ' > ' + fileName + '.1'
  os.system(cmd)

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print 'rename <from dimension> <to dimension> <filename>'
    sys.exit(1)
  else:
    fromName = sys.argv[1]
    toName = sys.argv[2]
    fileName = sys.argv[3]

    rename(fromName,toName,fileName)
    moveBack(fileName)

    fromName1 = string.upper(fromName[0]) + fromName[1:]
    toName1 = string.upper(toName[0]) + toName[1:]
    rename(fromName1,toName1,fileName)
    moveBack(fileName)

    fromName2 = string.upper(fromName)
    toName2 = string.upper(toName)
    rename(fromName2,toName2,fileName)
    moveBack(fileName)
