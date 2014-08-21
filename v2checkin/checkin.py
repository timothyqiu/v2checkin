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

    stat = client.get_mission_stat()
    if not stat['complete']:
        stat = client.checkin(stat['token'])

    logging.info('{} days of login. Checked in today: {}'.format(
        stat['days'],
        stat['complete'],
    ))


def main():
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
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
