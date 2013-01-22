import os
from unittest import TestCase
from lxml import etree

from mock import Mock
from hamcrest import assert_that, is_, contains_string, has_item, has_length

from py_x.core import Xunit, XunitSuite, XunitTest

XSD_FILE = os.path.join(os.path.dirname(__file__), '..', 'py_x', 'data', 'xunit.xsd')
SCHEMA = etree.XMLSchema(etree.XML(open(XSD_FILE).read()))
PARSER = etree.XMLParser(schema=SCHEMA)


def suite_mock(count=2):
    mock = Mock(XunitSuite)
    mock.name = "test_suite"
    mock.to_xml.return_value = etree.Element("testsuite")
    mock.test_count = count
    return mock

def test_mock(status="passed"):
    test = Mock(XunitTest)
    test.status = status
    test.to_xml.return_value = etree.Element("testcase")
    test.time = 1.5
    return test


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

    def test_should_generate_xml_node_with_testcase_tag(self):
        test = XunitTest("test")
        xml = test.to_xml()
        assert_that(xml.tag, is_("testcase"))
        
    def test_should_report_test_name_in_xml_as_name_attribute(self):
        test = XunitTest("test")
        xml = test.to_xml()
        assert_that(xml.attrib['name'], is_("test"))

        test = XunitTest("Nescobar_aloplop")
        xml = test.to_xml()
        assert_that(xml.attrib['name'], is_("Nescobar_aloplop"))
        
    def test_should_report_test_class_in_xml_as_class_attribute(self):
        test = XunitTest("test")
        xml = test.to_xml()
        # TODO: we don't have a class attribute yet 
        assert_that(xml.attrib['classname'], is_(""))

    def test_should_reporttime_in_xml_as_time_attribute(self):
        test = XunitTest("test")
        xml = test.to_xml()
        assert_that(xml.attrib['time'], is_("0.0"))

        test = XunitTest("test", time=4.4)
        xml = test.to_xml()
        assert_that(xml.attrib['time'], is_("4.4"))


class TestXunitSuite(TestCase):
    def test_should_have_an_name(self):
        suite = XunitSuite("tests_for_module_X")
        assert_that(suite.name, is_("tests_for_module_X"))

        suite = XunitSuite("tests_for_project_Y")
        assert_that(suite.name, is_("tests_for_project_Y"))

    def test_may_have_a_package_name(self):
        suite = XunitSuite("tests_in_package", package="Package1")
        assert_that(suite.package, is_("Package1"))

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

    def test_should_create_testsuite_node_as_xml_output(self):
        suite = XunitSuite("testsuite")
        result = suite.to_xml()

        assert_that(result.tag, is_("testsuite"))

    def test_should_report_name_in_xml_tag_as_name_attribute(self):
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        assert_that(result.attrib['name'], is_("my_name"))
        
        suite = XunitSuite("different_suite")
        result = suite.to_xml()
        assert_that(result.attrib['name'], is_("different_suite"))

    def test_should_report_test_count_in_xml_tag_as_tests_attribute(self):
        test = test_mock()
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        
        assert_that(result.attrib['tests'], is_("0"))

        suite.append(test)
        result = suite.to_xml()
        assert_that(result.attrib['tests'], is_("1"))

    def test_should_report_failure_count_in_xml_tag_as_failures_attribute(self):
        test = test_mock("failed")
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        
        assert_that(result.attrib['failures'], is_("0"))

        suite.append(test)
        result = suite.to_xml()
        assert_that(result.attrib['failures'], is_("1"))

    def test_should_report_error_count_in_xml_tag_as_error_attribute(self):
        test = test_mock("error")
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        
        assert_that(result.attrib['errors'], is_("0"))

        suite.append(test)
        result = suite.to_xml()
        assert_that(result.attrib['errors'], is_("1"))

    def test_should_report_skip_count_in_xml_tag_as_skipped_attribute(self):
        test = test_mock("skipped")
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        
        assert_that(result.attrib['skipped'], is_("0"))

        suite.append(test)
        result = suite.to_xml()
        assert_that(result.attrib['skipped'], is_("1"))

    def test_should_report_total_time_in_xml_tag_as_time_attribute(self):
        test = test_mock()
        suite = XunitSuite("my_name")
        result = suite.to_xml()

        assert_that(result.attrib['time'], is_("0.0"))

        suite.append(test)
        result = suite.to_xml()
        assert_that(result.attrib['time'], is_("1.5"))

    def test_should_report_package_in_xml_tag_as_package_attribute_if_present(self):
        suite = XunitSuite("my_name")
        result = suite.to_xml()
        assert_that('package' in result.attrib, is_(False), "shouldn't have package attribute")
        
        suite = XunitSuite("my_name", package="Pack1")
        result = suite.to_xml()
        assert_that(result.attrib['package'], is_("Pack1"))
         
    def test_should_report_empty_package_if_none_was_provided_and_force_package_is_used(self):
        suite = XunitSuite("my_name")
        result = suite.to_xml(force_package=True)
        assert_that(result.attrib['package'], is_(""))

    def test_should_report_id_in_xml_tag_if_one_is_provided(self):
        suite = XunitSuite("my_name")
        result = suite.to_xml(id=2)
        assert_that(result.attrib['id'], is_("2"))

        result = suite.to_xml(id=8)
        assert_that(result.attrib['id'], is_("8"))

    def test_should_append_tests_to_xml_output(self):
        suite = XunitSuite("my_name")
        test = test_mock()
        suite.append(test)                
        
        xml = suite.to_xml()
        assert_that(xml[0], is_(test.to_xml()))
 
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

        suite.append(test_mock)
        assert_that(results.total_test_count, is_(6))

    def test_should_aggregate_all_suite_names(self):
        suite = XunitSuite("name")
        suite2 = XunitSuite("other name")
        results = Xunit()

        results.append(suite)
        results.append(suite2)
        names = [x.name for x in results.suites]
        assert_that(names, has_item("name"))
        assert_that(names, has_item("other name"))
        
    def test_should_create_testsuite_tag_if_only_one_testsuite_registered(self):
        suite = suite_mock()
        result = Xunit(suite)
        xml = result.to_xml()

        suite.to_xml.assert_called_once()
        assert_that(xml, is_(suite.to_xml()))

    def test_should_create_testsuites_root_tag_if_more_than_one_testsuite_registered(self):
        result = Xunit()
        result.append(suite_mock())
        result.append(suite_mock())
        xml = result.to_xml()

        assert_that(xml.tag, is_("testsuites"))
        assert_that([child for child in xml], has_length(2))

    def test_should_force_package_inclusion_when_converting_multiple_suites_to_xml(self):
        result = Xunit()
        suite = suite_mock()
        result.append(suite)
        result.append(suite_mock())
        xml = result.to_xml()
        
        suite.to_xml.assert_called_once_with(force_package=True, id=0)
 
    def test_should_give_each_suite_an_id_when_converting_multiple_suites_to_xml(self):
        result = Xunit()
        suite = suite_mock()
        suite2 = suite_mock()
        result.append(suite)
        result.append(suite2)
        xml = result.to_xml()
        
        suite.to_xml.assert_called_once_with(force_package=True, id=0)
        suite2.to_xml.assert_called_once_with(force_package=True, id=1)
 
    def test_should_stringify_into_proper_xml_document(self):
        result = Xunit()
        xml = result.to_string()

        assert_that(xml, contains_string('<?xml version="1.0" encoding="UTF-8"?>'))

    def test_should_create_xml_that_is_valid_according_to_the_JUnit_jenkins_schema(self):
        test = XunitTest("test1")
        suite = XunitSuite("suite1")
        suite.append(test)
        result = Xunit()
        result.append(suite)

        try:
            xml = etree.fromstring(result.to_string(), PARSER)
        except etree.XMLSyntaxError as err:
            print(str(err))
            self.fail("Should have parsed without errors")
        else:
            pass

