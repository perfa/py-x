"""Copyright 2013 - Per Fagrell"""
from lxml import etree


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
        """Create the XML representation of this Xunit object hierarchy."""
        if len(self.suites) == 1:
            return self.suites[0].to_xml()

        node = etree.Element("testsuites") 
        for idx, suite in enumerate(self.suites):
            node.append(suite.to_xml(force_package=True, id=idx))
        return node

    def to_string(self):
        """Create a string containing the XML representation of this 
        Xunit object hierarchy."""
        res = '<?xml version="1.0" encoding="UTF-8"?>\n'
        res += etree.tostring(self.to_xml(), pretty_print=True)
        return res
        
class XunitSuite(object):
    """The status reports of a suite of tests"""
    def __init__(self, name, package=""):
        self.name = name
        self.package = package
        self._test_count = 0
        self._tests = []

    def to_xml(self, force_package=False, id=None):
        """Create the XML representation of this Xunit test-suite"""
        node = etree.Element("testsuite")
        node.attrib['name'] = str(self.name)
        node.attrib['tests'] = str(self.test_count)
        node.attrib['failures'] = str(self.failed_count)
        node.attrib['errors'] = str(self.error_count)
        node.attrib['skipped'] = str(self.skipped_count)
        node.attrib['time'] = str(self.total_time)
        node.attrib['hostname'] = 'localhost'
        if id is not None:
            node.attrib['id'] = str(id)
        if self.package:
            node.attrib['package'] = str(self.package)
        elif force_package:
            node.attrib['package'] = ""
        return node

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
