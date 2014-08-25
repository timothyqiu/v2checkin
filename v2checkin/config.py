#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import getopt
import json
import logging
import os
import sys


VERSION = '0.1.2'
AGENT = 'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0'


def get_config_path(path):
    if os.path.exists(path):
        return path
    user_home = os.getenv('USERPROFILE') or os.getenv('HOME')
    v2ex_home = os.getenv('V2EX_HOME') or user_home
    return os.path.join(v2ex_home, path)


V2CHECKIN_DEFAULT_CONFIG = get_config_path('.v2checkin.config')


def load_config(path):
    if os.path.exists(path):
        logging.info('Loading config from %s', path)
        with open(path, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    return config


def get_config():
    config_path = V2CHECKIN_DEFAULT_CONFIG
    optlist, args = getopt.getopt(sys.argv[1:], 'c:u:p:', '')

    for key, value in optlist:
        if key == '-c':
            config_path = value

    config = load_config(config_path)

    for key, value in optlist:
        if key == '-u':
            config['username'] = value
        elif key == '-p':
            config['password'] = value

    if not config:
        raise Exception('Config not specified')

    if 'username' not in config:
        raise Exception(
            'Username not found. Check the config file or use the -u option.'
        )

    if 'password' not in config:
        raise Exception(
            'Password not found. Check the config file or use the -p option.'
        )

    return config
