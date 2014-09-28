# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from __future__ import absolute_import, unicode_literals


"""Provide fake login views."""


from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import redirect, render

from .. import conf
from . import forms


config = conf.AuthGroupeXConf()


def smart_reverse(request, name):
    """Workaround until Django 1.5."""
    match = resolve(request.path)
    if match.namespace:
        prefix = '%s:' % match.namespace
    else:
        prefix = ''

    return reverse('%s%s' % (prefix, name), current_app=match.app_name)


def endpoint(request):
    """The view receiving the incoming request."""
    form = forms.EndPointForm(data=request.GET or None)

    if form.is_valid():
        next_url = smart_reverse(request, 'fake_fill') + '?' + form.build_query()
        messages.success(request, u"The auth-groupex request was properly signed.")
        return redirect(next_url)

    else:
        messages.error(request, u"The auth-groupex request couldn't be verified.")
        return render(request, 'authgroupex/fake_endpoint_fail.html', {'form': form})


def login_view(request):
    form = forms.LoginForm(data=request.POST or None, fields=config.FIELDS)

    if form.is_valid():
        reply_querystring = form.build_reply(request.GET['challenge'])
        reply_url = request.GET['url']
        separator = '&' if '?' in reply_url else '?'
        messages.success(request, u"Redirecting to %s with a signed request." % reply_url)
        return redirect(reply_url + separator + reply_querystring)

    return render(request, 'authgroupex/fake_fill.html', {
        'form': form,
        'preset_accounts': config.FAKE_ACCOUNTS,
    })
