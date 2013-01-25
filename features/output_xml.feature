Feature: Output is valid XUnit XML.
  The usefulness of a datarepresentation is minimal on its own. Given one or more suites of tests a user should get valid XUnit XML output that will satisfy the many tools that process that sort of XML.

  Scenario: Creating empty suite generates valid testsuite tag
    Given the following yaml:
    """
    test_suite_no_1:

    """
    When I convert it to XML
    Then it is valid according to the schema
    And it contains one test-suite named "test_suite_no_1"

  Scenario: Creating several empty testsuites generates valid testsuites/testsuite tags
    Given the following yaml:
    """
    test_suite_no_1: {} 
    test_suite_no_2: {}
    """
    When I convert it to XML
    Then it is valid according to the schema
    And it has a testsuites node as root
    And it contains one test-suite named "test_suite_no_1"
    And it contains one test-suite named "test_suite_no_2"

  Scenario: A test-suite with tests reports and appends them correctly.
    Given the following yaml:
    """
    test_suite_1:"
    "  test: {}"
    "  errord_test:"
    "    status: error"
    "    message: caused an error"
    "  failed_test:"
    "    status: failed"
    "    message: caused some failure"
    "  skipped_test:" 
    "    status: skipped"
    "    message: not implemented yet
    """
    When I convert it to XML
    Then it is valid according to the schema
    And the test-suite has the following attributes:
      |name      |value  |
      |tests     |4      |
      |errors    |1      |
      |failures  |1      |
      |skipped   |1      |
    And it contains 4 test tags
