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
        self.scheme = 'http'
        self.headers = {
            'User-Agent': UA
        }

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
        return self.session.get(url, verify=False, headers=self.headers)

    def post(self, path, payload):
        url = self.format_url(path)
        return self.session.post(
            url, data=payload, verify=False, headers=self.headers
        )

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
        self.session.headers.update({'Referer': self.format_url('/signin')})
        response = self.post('/signin', payload)
        if not response.history:
            raise LoginFailure()
        match = re.search(r'(.*?)://.*', response.url)
        self.scheme = urlparse.urlparse(response.url)[0]
        logging.debug('Protocol: %s', self.scheme)

        self.__save_cookies()

    def parse_mission_stat(self, text):
        pattern = r'已连续登录 (\d+) 天'
        match = re.search(pattern, text)
        if not match:
            raise Exception('Statistics not found.')
        days = int(match.group(1))
        pattern = r'/mission/daily/redeem\?once=(\d+)'
        match = re.search(pattern, text)
        stat = {
            'days': days,
            'complete': match is None
        }
        if match:
            stat['token'] = match.group(1)
        return stat

    def checkin(self, token):
        logging.info('Start to checkin. Good luck, Sir.')
        self.session.headers.update({
            'Referer': self.format_url('/mission/daily')
        })
        self.session.headers.update({'url': '/mission/daily/redeem'})
        response = self.get('/mission/daily/redeem?once={}'.format(token))
        return self.parse_mission_stat(response.text)

    def get_mission_stat(self):
        response = self.get('/mission/daily')
        if re.search(self.format_url('/signin'), response.url):
            raise NotLoggedIn()
        return self.parse_mission_stat(response.text)
