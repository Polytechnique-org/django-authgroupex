# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django_authgroupex import auth as groupex_auth
from django_authgroupex import conf as groupex_conf

# test data for groups
LOCAL_GROUP_MEMBERS = 'members'
LOCAL_GROUP_ADMINS = 'admins'

GROUPS_DICT = {
    groupex_auth.PERM_GROUP_MEMBER: [LOCAL_GROUP_MEMBERS],
    groupex_auth.PERM_GROUP_ADMIN: [LOCAL_GROUP_ADMINS],
}

class AuthGroupeXBackendTestCase(TestCase):
    def setUp(self):
        super(AuthGroupeXBackendTestCase, self).setUp()
        # need to override manually, @override_settingsis bypassed by Appconf
        self.config = groupex_conf.AuthGroupeXConf()
        self.config.MAP_GROUPS = GROUPS_DICT
        self.backend = groupex_auth.AuthGroupeXBackend(config=self.config)
        # local groups
        self.group_members = Group.objects.create(name=LOCAL_GROUP_MEMBERS)
        self.group_admins = Group.objects.create(name=LOCAL_GROUP_ADMINS)

    def test_create_new_user(self):
        """If the user never authenticated before, it must be created."""
        auth_data = {
            'username': 'aurelie.dupond.1985',
            'firstname': "Aurélie",
            'lastname': "Dupond",
            'promo': 1985,
            'email': 'aurelie.dupond@polytechnique.org',
        }
        auth_result = groupex_auth.AuthResult(success=True, data=auth_data)
        user = self.backend.authenticate(authgroupex=auth_result)
        self.assertIsNotNone(user)

        user_from_db = User.objects.get(username='aurelie.dupond.1985')
        self.assertEqual(user, user_from_db)
        # ensure data is valid as well
        self.assertEqual(user.first_name, "Aurélie")
        self.assertEqual(user.last_name, "Dupond")
        self.assertEqual(user.email, 'aurelie.dupond@polytechnique.org')

    def test_coming_back(self):
        """If the user is returning, we should not create a new one."""
        auth_data = {
            'username': 'jean.marcel.1986',
            'firstname': "Jean",
            'lastname': "Marcel",
            'promo': 1986,
            'email': 'jean.marcel@polytechnique.org',
        }
        auth_result = groupex_auth.AuthResult(success=True, data=auth_data)
        user1 = self.backend.authenticate(authgroupex=auth_result)
        user2 = self.backend.authenticate(authgroupex=auth_result)
        self.assertEqual(user1, user2)

    def test_no_groups(self):
        """A user with no groups from X.org must be in none here."""
        auth_data = {
            'username': 'no.group.1985',
            'firstname': "No",
            'lastname': "Group",
            'promo': 2000,
            'email': 'no.group@polytechnique.org',
        }
        auth_result = groupex_auth.AuthResult(success=True, data=auth_data)
        user = self.backend.authenticate(authgroupex=auth_result)
        self.assertNotIn(self.group_members, user.groups.all())
        self.assertNotIn(self.group_admins, user.groups.all())

    def test_member(self):
        """A member on X.org must a member here."""
        auth_data = {
            'username': 'member.group.1985',
            'firstname': "Member",
            'lastname': "Group",
            'promo': 2001,
            'email': 'member.group@polytechnique.org',
            'grpauth': 'membre',
        }
        auth_result = groupex_auth.AuthResult(success=True, data=auth_data)
        user = self.backend.authenticate(authgroupex=auth_result)
        self.assertIn(self.group_members, user.groups.all())
        self.assertNotIn(self.group_admins, user.groups.all())

    def test_admin(self):
        """An admin on X.org must a member and an admin here."""
        auth_data = {
            'username': 'admin.group.1985',
            'firstname': "Admin",
            'lastname': "Group",
            'promo': 2002,
            'email': 'admin.group@polytechnique.org',
            'grpauth': 'admin',
        }
        auth_result = groupex_auth.AuthResult(success=True, data=auth_data)
        user = self.backend.authenticate(authgroupex=auth_result)
        self.assertIn(self.group_members, user.groups.all())
        self.assertIn(self.group_admins, user.groups.all())

