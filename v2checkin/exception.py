#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import


class CheckinException(Exception):
    pass


class LoginFailure(CheckinException):
    def __init__(self):
        Exception.__init__(self, 'Login failed.')


class CheckinFailure(CheckinException):
    def __init__(self):
        Exception.__init__(self, 'Checkin failed.')


class AccessForbidden(CheckinException):
    def __init__(self):
        Exception.__init__(self, 'Access forbidden. Are you abroad?')
