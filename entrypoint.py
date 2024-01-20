#!/usr/bin/python3

# Essentially the same as quick_setup.py, quick_setup_headless.py and server_setup_headless.py

import os
import subprocess
import sys
import traceback

import cairis.tools.quickSetup as qs

dockerConf = os.environ.get('CAIRIS_CFG')

def init(args=None):
    # TODO: MYSQL_* should be replaced with URI in the codebase.
    if os.environ.get('MYSQL_PORT', 3306) != 3306:
        raise NotImplementedError('Changing MYSQL_PORT aka dbport is not fully supported and will break the installation.')
    if os.environ.get('MYSQL_USER', 'root') != 'root':
        raise NotImplementedError('Changing MYSQL_USER aka dbUser to non-root user is not supported.')

    if os.path.exists(dockerConf):
        os.remove(dockerConf)

    qs.quick_setup(
        os.environ.get('MYSQL_HOST'),
        3306,
        os.environ.get('MYSQL_ROOT_PASSWORD'),
        os.environ.get('CAIRIS_TMP', "/tmp"),
        '/cairis',
        dockerConf,
        8000,
        os.environ.get('CAIRIS_LOGLEVEL', "INFO"),
        '/cairis-ui', '/cairis-ui',
        os.environ.get('CAIRIS_USER', ''), os.environ.get('CAIRIS_PASS', ''),
        os.environ.get('CAIRIS_SMTP_SERVER', ''), os.environ.get('CAIRIS_SMTP_PORT', '465'),
        os.environ.get('CAIRIS_SMTP_USER', ''), os.environ.get('CAIRIS_SMTP_PASS', '')
    )

def main(args=None):
    try:
        init()
    except:  # noqa: E722
        traceback.print_exc()
        sys.exit(1)

    subprocess.run(["mod_wsgi-express", "start-server", "/cairis/bin/cairis.wsgi"])

if __name__ == '__main__':
    main()
