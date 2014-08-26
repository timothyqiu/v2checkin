#!/usr/bin/env python
# vim:set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import sys

from .providers import v2ex
from .config import get_config


def checkin(client, username, password):
    if client.needs_login():
        client.login(username, password)
        logging.info('Login success')
    else:
        logging.info('Already logged in')

    if client.needs_checkin():
        client.checkin()
        logging.info('Checkin success')
    else:
        logging.info('Already checked in')


def main():
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        filemode='a+')
    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'FATAL')

    try:
        config = get_config()

        USERNAME = config['username']
        PASSWORD = config['password']

        client = v2ex.Client(cookies=v2ex.COOKIES)
        checkin(client, USERNAME, PASSWORD)

        sys.exit(0)
    except Exception as e:
        logging.fatal(e, exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
