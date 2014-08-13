#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import getopt
import json
import logging
import os
import sys


def get_config_path(path):
    if os.path.exists(path):
        return path
    user_home = os.getenv('USERPROFILE') or os.getenv('HOME')
    v2ex_home = os.getenv('V2EX_HOME') or user_home
    return os.path.join(v2ex_home, path)


V2CHECKIN_DEFAULT_CONFIG = get_config_path('.v2checkin.config')
V2CHECKIN_DEFAULT_COOKIES = get_config_path('.v2checkin.cookies')


def get_config():
    try:
        config_path = V2CHECKIN_DEFAULT_CONFIG
        optlist, args = getopt.getopt(sys.argv[1:], 'c:u:p:', '')

        for key, value in optlist:
            if key == '-c':
                config_path = value

        if os.path.exists(config_path):
            logging.info('loading config from %s', config_path)
            with open(config_path, 'r') as f:
                try:
                    config = json.load(f)
                except Exception as e:
                    logging.error('found an error in config: %s', e.message)
        else:
            config = {}

        for key, value in optlist:
            if key == '-u':
                config['username'] = value
            elif key == '-p':
                config['password'] = value
    except getopt.GetoptError as e:
        print >>sys.stderr, e
        sys.exit(2)

    if not config:
        logging.error('config not specified')
        sys.exit(2)

    if 'username' not in config:
        logging.error(
            'Username not found. Check the config file or use the -u option.')
        sys.exit(2)

    if 'password' not in config:
        logging.error(
            'Password not found. Check the config file or use the -p option.')
        sys.exit(2)

    config['cookies'] = config.get('cookies', V2CHECKIN_DEFAULT_COOKIES)

    return config
