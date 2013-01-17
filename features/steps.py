# -*- coding: utf-8 -*-
from lettuce import step, world, before
from hamcrest import assert_that, is_
import py_x


@before.each_feature
def setup(feature):
    world.CurrentYaml = None
    world.CurrentXml = None


@step(u'Given a yaml test suite like this:')
def given_a_yaml_test_suite_like_this(step):
    world.CurrentYaml = step.multiline

@step(u'Given an empty XunitSuite named "([^"]*)"')
def given_an_empty_xunitsuite_named_suitename(step, suite_name):
    world.suite = py_x.XunitSuite(suite_name)

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
    attribute = status + "_count"
    count = getattr(world.suite, attribute)
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

