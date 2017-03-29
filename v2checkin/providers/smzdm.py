#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import lxml.html
import pickle
import re
import requests

from v2checkin import config
from v2checkin._compat import urllib_parse
from v2checkin.exception import LoginFailure, CheckinFailure


COOKIES = config.get_config_path('.v2checkin.smzdm.cookies')


class Client:

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = config.AGENT
        self.baseurl = 'https://zhiyou.smzdm.com/'
        self.referer = 'https://www.smzdm.com/'

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
        return urllib_parse.urljoin(self.baseurl, url)

    def get(self, url, **kwargs):
        self.session.headers['Referer'] = self.referer
        response = self.session.get(
            self.__get_url(url),
            **kwargs
        )
        self.referer = response.url
        return response

    def post(self, url, **kwargs):
        self.session.headers['Referer'] = self.referer
        response = self.session.post(
            self.__get_url(url),
            **kwargs
        )
        self.referer = response.url
        return response

    def needs_login(self):
        logging.info('Verifying login')
        page = self.get('/user/info/jsonp_get_current')
        return page.json()['smzdm_id'] == 0

    def login(self, username, password):
        logging.info('Start to login as %s', username)

        payload = {
            'username': username,
            'password': password,
            'rememberme': 1,
            'captcha': '',
            'redirect_to': '',
            'geetest_challenge': '',
            'geetest_validate': '',
            'geetest_seccode': '',
        }
        data = self.post('/user/login/ajax_check', data=payload).json()

        error_code = data['error_code']
        if error_code != 0:
            message = data.get('error_msg', '[Unknown]')
            raise LoginFailure('{}: {}'.format(error_code, message))

        self.__save_cookies()

    def needs_checkin(self, page=None):
        logging.info('Verifying checkin')
        page = self.get('/user/info/jsonp_get_current')
        data = page.json()

        return not data.get('checkin', {}).get('has_checkin', False)

    def checkin(self):
        logging.info('Getting checkin url')
        data = self.get('/user/info/jsonp_get_current').json()
        url = data['checkin']['set_checkin_url']

        logging.info('Start to checkin')
        data = self.get(url).json()

        error_code = data['error_code']
        if error_code != 0:
            message = data.get('error_msg', '[Unknown]')
            raise CheckinFailure()
