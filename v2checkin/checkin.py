#!/usr/bin/env python
# vim:set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import sys

from v2checkin._compat import iteritems
from v2checkin.config import get_config
from v2checkin.providers import smzdm, v2ex, xiami
from v2checkin.exception import CheckinException


def checkin(name, config):
    logging.info('Starting checkin routine for %s', name)

    provider = getattr(sys.modules[__name__], name)
    client = provider.Client(cookies=provider.COOKIES)

    username = config['username']
    password = config['password']

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
    except Exception as e:
        logging.fatal(e, exc_info=True)
        sys.exit(1)

    for provider, subconfig in iteritems(config):
        try:
            checkin(provider, subconfig)
        except CheckinException as e:
            logging.error(e)

    sys.exit(0)


if __name__ == '__main__':
    main()
