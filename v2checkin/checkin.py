#!/usr/bin/env python
# vim:set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import pickle
import requests
import sys

from .v2ex import V2EX, NotLoggedIn
from .config import get_config


def format_stat(stat):
    return '{} days of login. Checked in today: {}'.format(
        stat['days'],
        stat['complete']
    )


def do_checkin(v2ex):
    stat = v2ex.get_mission_stat()
    logging.info(format_stat(stat))
    if not stat['complete']:
        stat = v2ex.checkin(stat['token'])
        logging.info(format_stat(stat))


def checkin():
    config = get_config()

    USERNAME = config['username']
    PASSWORD = config['password']
    COOKIES = config['cookies']

    session = requests.Session()

    v2ex = V2EX(session)

    try:
        with open(COOKIES, 'r') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            session.cookies = cookies
    except:
        pass

    try:
        do_checkin(v2ex)
    except NotLoggedIn as e:
        logging.info(e)

        v2ex.login(USERNAME, PASSWORD)

        with open(COOKIES, 'w') as f:
            pickle.dump(
                requests.utils.dict_from_cookiejar(session.cookies),
                f
            )

        do_checkin(v2ex)


def main():
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=LOG_DATEFMT,
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
