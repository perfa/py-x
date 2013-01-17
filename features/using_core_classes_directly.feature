Feature: Using core classes directly.
In order to accomodate modes of usage we can't foresee at this time, the 
core classes should be usable directly in a relatively user-friendly manner.
Having these world in a simple manner also helps writing various front-ends,
such as for YAML parsing.

  Scenario: An empty test-suite
    Given an empty XunitSuite named "test_suite_name"
    When I append it to a new Xunit report
    Then I should get a test-suite called "test_suite_name"
    And it should report 0 tests
    And it should report 0 seconds run time

  Scenario: Simple tests
    Given an empty XunitSuite named "test_suite_name"
    And a passed test
    And a error'd test
    And a failed test
    And a skipped test
    When I append it to a new Xunit report
    Then I should get a test-suite called "test_suite_name"
    And it should report 4 tests
    And it should report 1 error
    And it should report 1 failed
    And it should report 1 skipped

   
