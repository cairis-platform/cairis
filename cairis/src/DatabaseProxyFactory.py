#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DatabaseProxyFactory.py $ $Id: DatabaseProxyFactory.py 249 2010-05-30 17:07:31Z shaf $
from MySQLDatabaseProxy import MySQLDatabaseProxy

activeProxy = MySQLDatabaseProxy

def build():
  return activeProxy()
