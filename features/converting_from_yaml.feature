Feature: Converting from YAML
In order to create usable XML from a format that a bit more terse
A user should be able to provide py-x with yaml representing the
test results, and get back the equivalent xUnit XML
So that they can easily create results files that will be parsed
by existing standard solutions such as Jenkins etc.

  Scenario: An empty testsuite
    Given a yaml test suite like this:
       """
       - test_suite_name:

       """
   When I convert it to XML
   Then I should get a test-suite called "test_suite_name"
   And it should report 0 tests
   And it should report 0 seconds run time

  Scenario: Simple tests
    Given a yaml test suite like this:
       """
      "- Various_tests:"
      "   -"
      "     name: passing_test"
      "   -"
      "     name: failing_test"
      "     status: failed"
      "     message: Test failed"
      "   -"
      "     name: errord_test"
      "     status: error"
      "     message: Test error"
      "   -"
      "     name: skipped_test"
      "     status: skipped"
      "     message: Not implemented yet"
      "
        """
      When I convert it to XML
      Then I should get a test-suite called "Various_tests"
      And it should report 4 tests
      And it should report 1 error
      And it should report 1 failed
      And it should report 1 skipped

