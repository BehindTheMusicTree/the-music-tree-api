#!/usr/bin/env python

from bodzify_api.test.view.user.UserViewTestCase import UserViewTestCase


class TestCase(UserViewTestCase):
    def test_create_then_all_lib_track_mixin_created(self):
        # user = self.model_fixture_factory.create_user('jojo')
        assert user.all_lib_track_mixin
