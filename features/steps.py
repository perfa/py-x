# -*- coding: utf-8 -*-
import os
from lxml import etree
from lettuce import step, world, before
from hamcrest import assert_that, is_, has_item, has_length
from pkg_resources import resource_string

import py_x

XSD_FILE = resource_string('py_x', '/data/xunit.xsd')
SCHEMA = etree.XMLSchema(etree.XML(XSD_FILE))
PARSER = etree.XMLParser(schema=SCHEMA)


@before.each_feature
def setup(feature):
    world.CurrentYaml = None
    world.CurrentXml = None


@step(u'And the test-suite has the following attributes:')
def and_the_test_suite_has_the_following_attributes(step):
    for attribute_dict in step.hashes:
        name = attribute_dict['name']
        value = attribute_dict['value']
        assert_that(world.e_xml.attrib[name], is_(value),
                   'Expected attribute "%s" to be "%s"' % (name, value))

@step(u'And it contains (\d+) test tags?')
def and_it_contains_x_test_tags(step, count):
    assert_that(world.e_xml.xpath('//testcase'), has_length(int(count)))

@step(u'Given the following yaml:')
def given_the_following_yaml(step):
    world.CurrentYaml = step.multiline

@step(u'Then it is valid according to the schema')
def then_it_is_valid_according_to_the_schema(step):
    xml = world.CurrentXml.to_string() 
    world.e_xml = etree.fromstring(xml, PARSER)

@step(u'And it contains one test-suite named "([^"]*)"')
def and_it_contains_one_test_suite_named_suitename(step, suitename):
    names = [x.attrib["name"] for x in world.e_xml.xpath('//testsuite')]
    assert_that(names, has_item(suitename))

@step(u'Given a yaml test suite like this:')
def given_a_yaml_test_suite_like_this(step):
    world.CurrentYaml = step.multiline

@step(u'Given an empty XunitSuite named "([^"]*)"')
def given_an_empty_xunitsuite_named_suitename(step, suite_name):
    world.suite = py_x.XunitSuite(suite_name)

@step(u'And it has a testsuites node as root')
def and_it_has_a_testsuites_node_as_root(step):
    assert_that(world.e_xml.tag, is_("testsuites"))
        
@step(u'When I append it to a new Xunit report')
def when_i_append_it_to_a_new_xunit_report(step):
    world.CurrentXml = py_x.Xunit(world.suite)
                
@step(u'When I convert it to XML')
def when_i_convert_it_to_xml(step):
    world.CurrentXml = py_x.from_yaml(world.CurrentYaml)

@step(u'Then I should get a test-suite called "([^"]*)"')
def then_i_should_get_a_test_suite_called_name(step, name):
    assert_that(world.CurrentXml.suites[0].name, is_(name))

@step(u'And it should report (\d) tests')
def and_it_should_report_x_tests(step, number):
    assert_that(world.CurrentXml.total_test_count, is_(int(number)))

@step(u'And it should report (\d+) seconds run time')
def and_it_should_report_x_seconds_run_time(step, number):
    assert_that(world.CurrentXml.total_time, is_(int(number)))

@step(u'And it should report 4 tests')
def and_it_should_report_4_tests(step):
    assert_that(world.CurrentXml.total_test_count, is_(4))

@step(u'And it should report 1 (error|skipped|failed)')
def and_it_should_report_1_error(step, status):
    if hasattr(world, "suite"):
        suite = world.suite
    else:
        suite = world.CurrentXml.suites[0]

    attribute = status + "_count"
    count = getattr(suite, attribute)
    assert_that(count, is_(1))
    
@step(u'Given an empty XunitSuite name "([^"]*)"')
def given_an_empty_xunitsuite_name_group1(step, group1):
    assert False, 'This step must be implemented'
    
@step(u'And a (passed|error\'d|failed|skipped) test')
def and_a_passed_test(step, status):
    world.suite.append(py_x.XunitTest("testname", 
                                      failed=status=="failed", 
                                      skipped=status=="skipped",
                                      error=status=="error\'d"))

