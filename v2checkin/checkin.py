#!/usr/bin/env python
# vim:set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import sys

from .providers.v2ex import V2EX
from .config import get_config


def checkin():
    config = get_config()

    USERNAME = config['username']
    PASSWORD = config['password']
    COOKIES = config['cookies']

    client = V2EX(cookies=COOKIES)

    if client.needs_login():
        client.login(USERNAME, PASSWORD)
        logging.info('Login success')
    else:
        logging.info('Already logged in')

    if client.needs_checkin():
        client.checkin()
        success = not client.needs_checkin()
        logging.info('Checkin result: %s', success)
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
        checkin()
        sys.exit(0)
    except Exception as e:
        logging.fatal(e, exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
