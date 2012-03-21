from Borg import Borg
import os
import DatabaseProxyFactory

def initialise():
  dbIniFile = os.environ['IRIS_SRC'] + '/db.ini'
  f = open(dbIniFile,"r")
  txt = f.read()
  vals = txt.split('\n')
  b = Borg()
  b.dbHost = vals[0]
  b.dbPort = int(vals[1])
  b.dbUser = vals[2]
  b.dbPasswd = vals[3]
  b.dbName = vals[4]
  b.dbProxy = DatabaseProxyFactory.build()

  pSettings = b.dbProxy.getProjectSettings()
  b.fontSize = pSettings['Font Size']
  b.apFontSize = pSettings['AP Font Size']
  b.fontName = pSettings['Font Name']

  b.mainFrame = None
