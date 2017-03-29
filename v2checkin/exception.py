#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import


class CheckinException(Exception):
    pass


class LoginFailure(CheckinException):
    def __init__(self, message=None):
        if message is None:
            Exception.__init__(self, 'Login failed.')
        else:
            Exception.__init__(self, 'Login failed: {}'.format(message))


class CheckinFailure(CheckinException):
    def __init__(self, message=None):
        if message is None:
            message = '[Unknown]'
        Exception.__init__(self, 'Checkin failed: {}'.format(message))


class AccessForbidden(CheckinException):
    def __init__(self):
        Exception.__init__(self, 'Access forbidden. Are you abroad?')
