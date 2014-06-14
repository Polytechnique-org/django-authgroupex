# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from __future__ import absolute_import, unicode_literals

import re
import hashlib

from django import forms
from django import http
from django.core.validators import RegexValidator

# handle changements from python2 to python3
import sys
if sys.version_info[0] <= 2:
    import urlparse as urllib_parse
else:
    from urllib import parse as urllib_parse


from .. import conf


PERM_CHOICES = (
    ('admin', "Admin"),
    ('user', "User"),
)

GROUP_AUTH_CHOICES = (
    ('grpmember', "Group member"),
    ('grpadmin', "Group admin"),
)



validate_hruid = RegexValidator(re.compile(r'^[-\w.]+$'),
    u"Enter a valid hruid containing only letters, numbers, dots ans hyphens", 'invalid')

DEFAULT_FIELDS = {
    'username': forms.CharField(label="Username", required=False, validators=[validate_hruid]),
    'firstname': forms.CharField(label="First name", required=False),
    'lastname': forms.CharField(label="Last name", required=False),
    'perms': forms.ChoiceField(choices=PERM_CHOICES, label="Permissions", required=False),
    'grpauth': forms.ChoiceField(choices=GROUP_AUTH_CHOICES, label="Group access level", required=False),
}


class LoginForm(forms.Form):
    def __init__(self, fields=(), *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for name in fields:
            try:
                form_field = DEFAULT_FIELDS[name]
            except KeyError:
                form_field = forms.CharField(label=name.capitalize(), required=False)
            self.fields[name] = form_field

    def build_reply(self, challenge):
        config = conf.AuthGroupeXConf()

        auth_parts = ['1', challenge, config.KEY]
        reply = http.QueryDict('', mutable=True)

        for field in config.FIELDS:
            value = self.cleaned_data[field]
            reply[field] = value
            auth_parts.append(value)

        auth_parts.append('1')
        auth = ''.join(auth_parts).encode('utf8')

        reply['auth'] = hashlib.md5(auth).hexdigest()

        return reply.urlencode()


long_text = forms.TextInput(attrs={'size': 60})


class EndPointForm(forms.Form):
    url = forms.CharField(max_length=600, widget=long_text, help_text="The return URL")
    challenge = forms.CharField(max_length=64, widget=long_text,
            help_text="A random challenge, crafted specifically for this request")
    _pass = forms.CharField(max_length=64, widget=long_text,
            help_text="Signature : md5(challenge + private_key)")

    def __init__(self, *args, **kwargs):
        super(EndPointForm, self).__init__(*args, **kwargs)
        self.fields['pass'] = self.fields.pop('_pass')

    def clean_url(self):
        return urllib_parse.unquote(self.cleaned_data['url'])

    def clean(self):
        config = conf.AuthGroupeXConf()
        challenge = self.cleaned_data['challenge']
        password = self.cleaned_data['pass']

        expected_pass = hashlib.md5((challenge + config.KEY).encode('ascii')).hexdigest()

        if expected_pass != password:
            raise forms.ValidationError("Expected signature %s, got %s" % (expected_pass, password))
        return self.cleaned_data

    def build_query(self):
        """Build the query part for the 'next' URL."""
        url = self.cleaned_data['url']
        challenge = self.cleaned_data['challenge']

        query = http.QueryDict('', mutable=True)
        query['challenge'] = challenge
        query['url'] = url

        return query.urlencode()
