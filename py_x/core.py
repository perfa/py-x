"""Copyright 2013 - Per Fagrell"""


class Xunit(object):
    """Top-level representation of an Xunit test run. Outputs appropriate XML"""
    def __init__(self, suite=None):
        self.suites = []
        self.total_time = 0
        if suite is not None:
            self.suites += [suite]

    def append(self, test_suite):
        """Add a test-suite and aggregate its results"""
        self.suites.append(test_suite)
    
    @property
    def total_test_count(self):
        """The total number of tests contained in all suites"""
        return sum([suite.test_count for suite in self.suites])

    def to_xml(self):
        """Create a string containing the XML representation of this 
        Xunit object hierarchy."""
        return '<?xml version="1.0" encoding="UTF-8"?>'

    
class XunitSuite(object):
    """The status reports of a suite of tests"""
    def __init__(self, name):
        self.name = name
        self._test_count = 0
        self._tests = []

    def append(self, test):
        """Add a test and aggregate its result"""
        self._tests.append(test)

    @property
    def total_time(self):
        """The total run-time of all the tests in the suite"""
        return 0.0 + sum([x.time for x in self._tests])

    @property
    def test_count(self):
        """The number of tests in the suite"""
        return len(self._tests)

    @property
    def error_count(self):
        """The number of tests that had [an] error[s] in the suite"""
        return len([x for x in self._tests if x.status == "error"])
     
    @property
    def failed_count(self):
        """The number of tests that failed in the suite"""
        return len([x for x in self._tests if x.status == "failed"])
   
    @property
    def skipped_count(self):
        """The number of tests that were skipped in the suite"""
        return len([x for x in self._tests if x.status == "skipped"])

    @property
    def number_passing(self):
        """The number of tests that are marked as 'Passed'"""
        return self.test_count
    
    def __repr__(self):
        return "<XunitSuite[%s] 0x%x>" % (self.name, id(self))

class XunitTest(object):
    """The status report of a single test"""
    def __init__(self, name, class_name="", error=False, failed=False, skipped=False, time=0.0):
        self.name = name
        self.class_name = class_name
        self.status = "passed"
        self.time = time
        if error:
            self.status = "error"
        elif failed:
            self.status = "failed"
        elif skipped:
            self.status = "skipped"

    @property
    def passed(self):
        """True if status is not error, failed or skipped"""
        return self.status == "passed"
