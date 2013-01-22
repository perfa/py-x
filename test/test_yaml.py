from unittest import TestCase
from hamcrest import assert_that, is_, has_length, contains_string

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

    def test_should_mark_tests_with_failed_status_as_such(self):
        input = """
        - yaml_test_suite:
            -
             name: failing_test
             status: failed
             message: I had a failure
        """
        result = from_yaml(input)

        assert_that(result.suites[0].failed_count, is_(1))

    def test_should_mark_tests_with_error_status_as_such(self):
        input = """
        - yaml_test_suite:
            -
             name: erronous_test
             status: error
             message: I had an error
        """
        result = from_yaml(input)

        assert_that(result.suites[0].error_count, is_(1))


    def test_should_mark_tests_with_skipped_status_as_such(self):
        input = """
        - yaml_test_suite:
            -
             name: known_bad_test
             status: skipped
             message: I'm known bad
        """
        result = from_yaml(input)

        assert_that(result.suites[0].skipped_count, is_(1))
