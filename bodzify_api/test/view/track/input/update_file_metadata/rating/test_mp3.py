#!/usr/bin/env python

import logging

import pytest

from bodzify_api.test.view.track.input.update_file_metadata.rating.Mp3TestCase import Mp3TestCase
from django.core.management import call_command

logger = logging.getLogger('bodzify_api')


@pytest.fixture(params=[Mp3TestCase])
def child_instance(request, db):
    # Créez une instance de la classe de test
    test_case = request.param()

    call_command('loaddata', 'app_initial_data', 'pytest_user_initial_data')

    # Appellez setUp
    test_case.setUp()

    yield test_case

    # Appellez tearDown après le test
    test_case.tearDown()


def test_max_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_max,
                               value_in_matadata=child_instance.value_max_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_missing_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_on_present_tag_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=True)


def test_min_then_ok(child_instance):
    child_instance._test_value(value=child_instance.value_min,
                               value_in_matadata=child_instance.value_min_in_metadata,
                               additional_data_json=None,
                               file_has_tags=False)


def test_none_then_none(child_instance):
    child_instance._test_value(value=None, additional_data_json=None, file_has_tags=False)
