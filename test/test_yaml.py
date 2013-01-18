"""Copyright 2013 - Per Fagrell"""
from unittest import TestCase
from hamcrest import assert_that, is_, has_length

from py_x import from_yaml
import py_x


class TestFromYaml(object):
    def test_should_pick_up_title_as_suite_name(self):
        input = """
        - yaml_test_suite:

        """
        result = from_yaml(input)
        
        assert_that(result.total_test_count, is_(0))
        assert_that(result.suites[0].name, is_("yaml_test_suite"))

    def test_should_create_test_suite_for_each_top_level_entry(self):
        input = """
        - yaml_test_suite:

        - xml_test_suite:

        """
        result = from_yaml(input)
        assert_that(result.suites, has_length(2))

    def test_should_create_tests_from_name_attribute_in_sublist(self):
        input = """
        - yaml_test_suite:
            -
              name: my_awesome_test
        """
        result = from_yaml(input)

        assert_that(result.total_test_count, is_(1))
