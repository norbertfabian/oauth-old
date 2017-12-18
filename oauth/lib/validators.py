# -*- coding: utf-8 -*-

import re

EMAIL_REGEX = re.compile(r'([^@]+)@([^@]+\.[^@]+)')
PASSWORD_REGEX = re.compile(r'[\w\s]{6,}')

validateEmail = lambda v: EMAIL_REGEX.match(v)
validatePassword = lambda v,l=6: len(v) > l
