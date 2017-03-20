#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import lxml.html
import pickle
import requests

from .. import config
from .._compat import urllib_parse
from ..exception import LoginFailure, AccessForbidden


COOKIES = config.get_config_path('.v2checkin.xiami.cookies')


class Client:

    def __init__(self, **kwargs):
        self.__session = requests.Session()
        self.__session.headers['User-Agent'] = config.AGENT
        self.__baseurl = 'http://www.xiami.com/'
        self.__referer = self.__baseurl

        if 'cookies' in kwargs:
            self.__cookies = kwargs['cookies']
            self.__load_cookies()

    def __load_cookies(self):
        try:
            with open(self.__cookies, 'r') as f:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                self.__session.cookies = cookies
        except:
            pass

    def __save_cookies(self):
        try:
            with open(self.__cookies, 'w') as f:
                pickle.dump(
                    requests.utils.dict_from_cookiejar(self.__session.cookies),
                    f
                )
        except:
            pass

    def __get_url(self, url):
        return urllib_parse.urljoin(self.__baseurl, url)

    def get(self, url, **kwargs):
        response = self.__session.get(
            self.__get_url(url),
            **kwargs
        )
        self.__session.headers['Referer'] = response.url
        return response

    def post(self, url, **kwargs):
        response = self.__session.post(
            self.__get_url(url),
            **kwargs
        )
        self.__session.headers['Referer'] = response.url
        return response

    def needs_login(self):
        logging.info('Verifying login')
        page = self.get('http://www.xiami.com/index/home')
        try:
            return not page.json()['data']['userInfo']
        except ValueError as e:
            if '虾米音乐在您所处的国家或地区暂时无法使用' in page.text:
                raise AccessForbidden()
            else:
                raise e

    def login(self, username, password):
        logging.info('Start to login as %s', username)
        page = self.get('https://login.xiami.com/member/login')
        tree = lxml.html.fromstring(page.text)
        token = tree.xpath('//input[@name="_xiamitoken"]/@value')[0]

        payload = {
            '_xiamitoken': token,
            'email': username,
            'password': password,
            'havenald': '',
            'from': 'web',
            'done': 'http://www.xiami.com',
            'submit': '登 录',
        }
        page = self.post('https://login.xiami.com/member/login', data=payload)
        if not page.json()['status']:
            raise LoginFailure()

        self.__save_cookies()

    def needs_checkin(self):
        logging.info('Verifying checkin')
        page = self.get('http://www.xiami.com/index/home')
        return page.json()['data']['userInfo']['is'] == 0

    def checkin(self):
        logging.info('Start to checkin')
        self.get('http://www.xiami.com/index/home')
        self.post('http://www.xiami.com/task/signin')
