#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import lxml.html
import pickle
import re
import requests
import urlparse


UA = 'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0'


class NotLoggedIn(Exception):
    def __init__(self):
        Exception.__init__(self, 'Not logged in.')


class LoginFailure(Exception):
    def __init__(self):
        Exception.__init__(self, 'Login failed.')


class V2EX:

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = UA
        self.scheme = 'http'
        self.referer = 'http://www.v2ex.com/'

        if 'cookies' in kwargs:
            self.cookies = kwargs['cookies']
            self.__load_cookies()

    def __load_cookies(self):
        try:
            with open(self.cookies, 'r') as f:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                self.session.cookies = cookies
        except:
            pass

    def __save_cookies(self):
        try:
            with open(self.cookies, 'w') as f:
                pickle.dump(
                    requests.utils.dict_from_cookiejar(self.session.cookies),
                    f
                )
        except:
            pass

    def format_url(self, url):
        return '{}://www.v2ex.com{}'.format(self.scheme, url)

    def get(self, path):
        url = self.format_url(path)
        self.session.headers['Referer'] = self.referer
        response = self.session.get(url, verify=False)
        self.referer = response.url
        return response

    def post(self, path, **kwargs):
        url = self.format_url(path)
        self.session.headers['Referer'] = self.referer
        response = self.session.post(url, verify=False, **kwargs)
        self.referer = response.url
        return response

    def needs_login(self):
        logging.info('Verifying login')
        page = self.get('/settings')
        return len(page.history) > 0

    def login(self, username, password):
        logging.info('Start to login as %s', username)
        response = self.get('/signin')
        response.raise_for_status()

        tree = lxml.html.fromstring(response.text)
        once = tree.xpath('//input[@name="once"]/@value')
        if not once:
            raise Exception('Cannot find login token')
        token = once[0]

        payload = {
            'u': username,
            'p': password,
            'once': token,
            'next': '/',
        }
        response = self.post('/signin', data=payload)
        if not response.history:
            raise LoginFailure()
        self.scheme = urlparse.urlparse(response.url)[0]
        logging.debug('Protocol: %s', self.scheme)

        self.__save_cookies()

    def needs_checkin(self):
        logging.info('Verifying checkin')
        page = self.get('/mission/daily')
        tree = lxml.html.fromstring(page.text)
        action = tree.xpath('//input/@onclick')[0]
        return '/mission/daily' in action

    def checkin(self):
        logging.info('Getting checkin token')
        page = self.get('/mission/daily')
        tree = lxml.html.fromstring(page.text)
        action = tree.xpath('//input/@onclick')[0]
        match = re.match(r".+?=\s*'(.+)'", action)

        logging.info('Checking in')
        self.get(match.group(1))
