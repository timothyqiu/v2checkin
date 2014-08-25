#!/usr/bin/env python
# vim: set fileencoding=utf-8

from __future__ import unicode_literals
from __future__ import absolute_import


class LoginFailure(Exception):
    def __init__(self):
        Exception.__init__(self, 'Login failed.')


class CheckinFailure(Exception):
    def __init__(self):
        Exception.__init__(self, 'Checkin failed.')
