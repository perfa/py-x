# -*- coding: utf-8 -*-
from lettuce import step
from hamcrest import assert_that, is_
from py_x.core import Xunit

CurrentYaml = None
CurrentXml = None

@step(u'Given a yaml test suite like this:')
def given_a_yaml_test_suite_like_this(step):
    global CurrentYaml
    CurrentYaml = step.multiline

@step(u'When I convert it to XML')
def when_i_convert_it_to_xml(step):
    global CurrentXml
    CurrentXml = Xunit.from_yaml(CurrentYaml)

@step(u'Then I should get a test-suite called "([^"]*)"')
def then_i_should_get_a_test_suite_called_name(step, name):
    assert_that(CurrentXml.suites[0].name, is_(name))

@step(u'And it should report (\d) tests')
def and_it_should_report_x_tests(step, number):
    assert_that(CurrentXml.total_test_count, is_(int(number)))

@step(u'And it should report (\d+) seconds run time')
def and_it_should_report_x_seconds_run_time(step, number):
    assert_that(CurrentXml.total_time, is_(int(number)))

@step(u'And it should report 4 tests')
def and_it_should_report_4_tests(step):
    assert False, 'This step must be implemented'

@step(u'And it should report 1 error')
def and_it_should_report_1_error(step):
    assert False, 'This step must be implemented'

@step(u'And it should report 1 failure')
def and_it_should_report_1_failure(step):
    assert False, 'This step must be implemented'

@step(u'And it should report 1 skipped')
def and_it_should_report_1_skipped(step):
    assert False, 'This step must be implemented'
