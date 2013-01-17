"""Copyright 2013 - Per Fagrell"""
from unittest import TestCase
from mock import Mock
from hamcrest import assert_that, is_, contains_string

from py_x.core import Xunit, XunitSuite, XunitTest


def suite_mock(count=2):
    mock = Mock(XunitSuite)
    mock.test_count = count
    return mock


class TestXunitTest(TestCase):
    def test_should_have_name(self):
        test = XunitTest("test_that_I_have_a_name")
        assert_that(test.name, is_("test_that_I_have_a_name"))

    def test_should_allow_you_to_give_test_a_class(self):
        test = XunitTest("test_without_a_class")
        assert_that(test.class_name, is_(""))

        test = XunitTest("test_with_a_class", class_name="classy")
        assert_that(test.class_name, is_("classy"))
        
    def test_should_default_to_report_the_test_took_zero_seconds(self):
        test = XunitTest("test_without_a_time")
        assert_that(test.time, is_(0.0))

    def test_should_allow_a_run_time_to_be_provided_on_creation(self):
        test = XunitTest("test_with_time", time=0.333)
        assert_that(test.time, is_(0.333))

    def test_should_default_to_status_passed(self):
        test = XunitTest("Passing_test")
        assert_that(test.status, is_("passed"))
        assert_that(test.passed, is_(True))

    def test_should_allow_status_to_be_set_to_error(self):
        test = XunitTest("Errord_test", error=True)
        assert_that(test.status, is_("error"))
        assert_that(test.passed, is_(False))

    def test_should_allow_status_to_be_set_to_skipped(self):
        test = XunitTest("skipped_test", skipped=True)
        assert_that(test.status, is_("skipped"))
        assert_that(test.passed, is_(False))

    def test_should_allow_status_to_be_set_to_failed(self):
        test = XunitTest("failed_test", failed=True)
        assert_that(test.status, is_("failed"))
        assert_that(test.passed, is_(False))

class TestXunitSuite(TestCase):
    def test_should_have_an_name(self):
        suite = XunitSuite("tests_for_module_X")
        assert_that(suite.name, is_("tests_for_module_X"))

        suite = XunitSuite("tests_for_project_Y")
        assert_that(suite.name, is_("tests_for_project_Y"))

    def test_should_aggregate_test_results(self):
        suite = XunitSuite("testsuite")
        test1 = Mock(XunitTest)

        assert_that(suite.test_count, is_(0))
        suite.append(test1)
        assert_that(suite.test_count, is_(1))
        suite.append(test1)
        assert_that(suite.test_count, is_(2))

    def test_should_maintain_count_of_passing_tests(self):
        suite = XunitSuite("testsuite")
        test1 = Mock(XunitTest)

        assert_that(suite.number_passing, is_(0))
        suite.append(test1)
        assert_that(suite.number_passing, is_(1))
        suite.append(test1)
        assert_that(suite.number_passing, is_(2))

    def test_should_maintain_count_of_tests_that_had_errors(self):
        suite = XunitSuite("errorsuite")
        test1 = Mock(XunitTest)
        test1.passed = False
        test1.status = "error"
        assert_that(suite.error_count, is_(0))
        
        suite.append(test1)
        assert_that(suite.error_count, is_(1))
        
        test2 = Mock(XunitTest)
        test2.passed = False
        test2.status = "failed"
 
        suite.append(test2)
        assert_that(suite.error_count, is_(1))

    def test_should_maintain_count_of_tests_that_failed(self):
        suite = XunitSuite("failure_suite")
        test1 = Mock(XunitTest)
        test1.passed = False
        test1.status = "failed"

        assert_that(suite.failed_count, is_(0))
        
        suite.append(test1)
        assert_that(suite.failed_count, is_(1))

    def test_should_maintain_count_of_tests_that_were_skipped(self):
        suite = XunitSuite("skip_suite")
        test1 = Mock(XunitTest)
        test1.passed = False
        test1.status = "skipped"

        assert_that(suite.skipped_count, is_(0))
        
        suite.append(test1)
        assert_that(suite.skipped_count, is_(1))

    def test_should_aggregate_run_time_of_tests(self):
        suite = XunitSuite("testsuite")
        test1 = XunitTest("test", time=0.5)

        assert_that(suite.total_time, is_(0.0))
        
        suite.append(test1)
        assert_that(suite.total_time, is_(0.5))
 
        suite.append(test1)
        assert_that(suite.total_time, is_(1.0))


class TestXunit(TestCase):
    def test_should_report_empty_test_run_as_having_zero_tests_taking_zero_seconds(self):
        results = Xunit()
        assert_that(results.total_test_count, is_(0))
        assert_that(results.total_time, is_(0.0))

    def test_should_aggregate_test_counts_from_all_suites(self):
        suite = XunitSuite("name")
        test_mock = Mock(XunitTest)
        suite.append(test_mock)
        suite.append(test_mock)
        results = Xunit()
        
        results.append(suite)
        assert_that(results.total_test_count, is_(2))

        results.append(suite)
        assert_that(results.total_test_count, is_(4))

        
    def test_should_create_valid_xml_document_as_output(self):
        result = Xunit(suite_mock())
        xml = result.to_xml()

        assert_that(xml.splitlines()[0], contains_string('<?xml version="1.0" encoding="UTF-8"?>'))

