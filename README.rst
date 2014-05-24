django-authgroupex
==================

This library provides a Django authentication backend based on Polytechnique.org's auth-groupe-x SSO protocol.


Setup
=====

The django-authgroupex package requires only a minimal pair of settings to work:

.. code-block:: python

    # Enable AuthGroupeX authentication backend
    AUTHENTICATION_BACKENDS = (
        'django_authgroupex.auth.AuthGroupeXBackend',
        'django.contrib.auth.backends.ModelBackend',  # Optional
    )

    # Read secret key from file
    AUTHGROUPEX_KEY = open('authgroupex.key', 'r').readline()


It should also be included in your projects ``urls.py`` file:

.. code-block:: python

    urlpatterns = patterns('',
        # Usual suspects here
        url(r'^xorgauth/', include('django_authgroupex.urls', namespace='authgroupex')),
    )

.. note:: The app **must** be installed under the ``authgroupex`` namespace.



If you're using the ``django.contrib.admin`` app, you may also override its login form:

.. code-block:: python

    from django.contrib import admin
    admin.site.login_template = 'authgroupex/admin_login.html'

.. note:: This setting requires ``django_authgroupex`` to be part of your ``INSTALLED_APPS``.


Configuring django-authgroupex
==============================

django-authgroupex provides the following settings:

Connection
----------

* ``AUTHGROUPEX_KEY``: **Required**, the secret key used to connect to an AuthGroupeX-compatible server.

* ``AUTHGROUPEX_ENDPOINT``: The remote endpoint (an AuthGroupeX-compatible server).
  Default: `https://www.polytechnique.org/auth-groupe-x/utf8`
* ``AUTHGROUPEX_FIELDS``: The list of profile fields to require upon connection; order matters.
  Default: ``('username', 'firstname', 'lastname', 'email')``


Models
------

* ``AUTHGROUPEX_USER_MODEL``: Model storing users.
  Default: ``auth.User``
* ``AUTHGROUPEX_GROUP_MODEL``: Model storing groups.
  Default: ``auth.Group``

.. note:: The ``AuthGroupeXBackend`` authentication backend expects a
          :class:`~django.contrib.auth.AbstractUser` subclass in that model.
          This behaviour can be tuned by writing your own subclass, inheriting from
          :class:`~django_authgroupex.auth.AuthGroupeXMixin`.

Permissions
-----------

django_authgroupex uses the 4 permissions from the AuthGroupeX SSO:

* :data:`~django_authgroupex.auth.PERM_USER`, for simple users
* :data:`~django_authgroupex.auth.PERM_GROUP_MEMBER`, for member of the related ``AUTHGROUPEX_GROUP``
* :data:`~django_authgroupex.auth.PERM_GROUP_ADMIN`, for admins of the related ``AUTHGROUPEX_GROUP``
* :data:`~django_authgroupex.auth.PERM_ADMIN`, for admins of the remote site


These (remote) permissions can be mapped to Django access rights through the following settings:

* ``AUTHGROUPEX_SUPERADMIN_PERMS``: A list of AuthGroupeX permissions that enable the
  ``is_admin`` flag on this server.
  Default: ``()``
* ``AUTHGROUPEX_STAFF_PERMS``: A list of AuthGroupeX permissions that enable the
  ``is_staff`` flag on this server.
* ``AUTHGROUPEX_DISABLE_DEADS``: Whether a user connecting from a "dead" account should
  be switched to ``is_active=False``
  Default: ``False``
* ``AUTHGROUPEX_GROUP``: Name of the AuthGroupeX group to use for a single-group website.
  Default: ``''``
* ``AUTHGROUPEX_MAP_GROUPS``: Dict mapping an AuthGroupeX permission to a list of local group names.
  Default: ``{}``


URLs
----

The usual setup of django-authgroupex is to use
:meth:`~django_authgroupex.views.AuthGroupeXUniqueView.login_view` for authentication,
either as "login" page (thus enabling transparent authentication) or through a
"connect through X.org" link from the usual login page.

This behaviour can be tuned through the following settings:

* ``AUTHGROUPEX_RETURN_URL``: Name of the (local) return url for successful logins.
  Default: ``settings.LOGIN_URL``
* ``AUTHGROUPEX_LOGIN_REDIRECT_URL``: Name of the URL to redirect the user to after a successful login without a ``?next=`` parameter
  Default: ``settings.LOGIN_REDIRECT_URL``

If :meth:`~django_authgroupex.views.AuthGroupeXUniqueView.login_view` is used,
``AUTHGROUPEX_RETURN_URL`` **must** point to that view.

If :meth:`~django_authgroupex.views.AuthGroupeXBaseView.login_begin_view` and
:meth:`~django_authgroupex.views.AuthGroupeXBaseView.login_return_view` are used
``AUTHGROUPEX_RETURN_URL`` **must** point to ``login_return_view``.


Testing
=======

For testing purposes, it is advised to not use a production private key.

django_authgroupex has a special, "fake" mode for such cases.
That fake mode adds a couple of URLs handling a local endpoint where the end user can
choose custom values for requested fields.

Installation requires a couple of extra settings::

    # settings.py
    AUTHGROUPEX_FAKE = True
    AUTHGROUPEX_ENDPOINT = 'authgroupex:fake_endpoint'
    INSTALLED_APPS = (
        '...',
        'django_authgroupex',
    )

The ``AUTHGROUPEX_FAKE`` setting will enable two views for handling fake requests:

- One validates the input (which can also be used to validate external clients)
- The second provides a dynamic form based on ``AUTHGROUPEX_FIELDS``, enabling users to
  select their preferred response.

The ``AUTHGROUPEX_ENDPOINT`` setting should include the namespace at which ``django_authgroupex.urls`` was inserted.
