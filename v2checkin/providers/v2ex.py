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

from .. import config
from ..exception import LoginFailure, CheckinFailure


COOKIES = config.get_config_path('.v2checkin.v2ex.cookies')


class Client:

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = config.AGENT
        self.baseurl = 'https://www.v2ex.com/'
        self.referer = self.baseurl

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

    def __get_url(self, url):
        return urlparse.urljoin(self.baseurl, url)

    def get(self, url, **kwargs):
        self.session.headers['Referer'] = self.referer
        response = self.session.get(
            self.__get_url(url),
            verify=False,
            **kwargs
        )
        self.referer = response.url
        return response

    def post(self, url, **kwargs):
        self.session.headers['Referer'] = self.referer
        response = self.session.post(
            self.__get_url(url),
            verify=False,
            **kwargs
        )
        self.referer = response.url
        return response

    def needs_login(self):
        logging.info('Verifying login')
        page = self.get('/settings')
        return len(page.history) > 0

    def login(self, username, password):
        logging.info('Start to login as %s', username)
        page = self.get('/signin')
        tree = lxml.html.fromstring(page.text)
        u = tree.xpath('//input[@class="sl" and @type="text"]/@name')[0]
        p = tree.xpath('//input[@class="sl" and @type="password"]/@name')[0]
        token = tree.xpath('//input[@name="once"]/@value')[0]

        payload = {
            u: username,
            p: password,
            'once': token,
            'next': '/',
        }
        page = self.post('/signin', data=payload)
        if not page.history:
            tree = lxml.html.fromstring(page.text)
            message = tree.xpath('string(//div[@id="Main"]/div/div[@class="problem"])')
            raise LoginFailure(message)

        self.__save_cookies()

    def needs_checkin(self, page=None):
        logging.info('Verifying checkin')
        if not page:
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

        logging.info('Start to checkin')
        page = self.get(match.group(1))

        if self.needs_checkin(page):
            raise CheckinFailure()
