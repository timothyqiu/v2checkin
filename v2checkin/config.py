#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import getopt
import json
import logging
import os
import sys


VERSION = '0.2.0'
AGENT = 'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0'


def get_config_path(path):
    if os.path.exists(path):
        return path
    user_home = os.path.expanduser('~')
    v2checkin_home = os.getenv('V2CHECKIN_HOME') or user_home
    return os.path.join(v2checkin_home, path)


V2CHECKIN_DEFAULT_CONFIG = get_config_path('.v2checkin.config')


def load_config(path):
    if os.path.exists(path):
        logging.info('Loading config from %s', path)
        with open(path, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    return config


def check_config(config):
    if not config:
        raise Exception('Config not specified')

    for provider, provider_config in config.iteritems():
        logging.info('Config found for %s', provider)

        if 'username' not in provider_config:
            raise Exception(
                'Username not specified for {}'.format(provider)
            )

        if 'password' not in provider_config:
            raise Exception(
                'Password not specified for {}'.format(provider)
            )


def get_config():
    config_path = V2CHECKIN_DEFAULT_CONFIG
    optlist, args = getopt.getopt(sys.argv[1:], 'c:u:p:', '')

    for key, value in optlist:
        if key == '-c':
            config_path = value

    config = load_config(config_path)

    check_config(config)

    return config
