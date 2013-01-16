"""Copyright 2013 - Per Fagrell"""


class Xunit(object):
    """Top-level representation of an Xunit test run. Outputs appropriate XML"""
    def __init__(self, suite):
        self.suites = [suite]
        self.total_test_count = 0
        self.total_time = 0

    @classmethod
    def from_yaml(cls, yaml):
        """Parse provided yaml and instantiate an Xunit object from that"""
        return Xunit(XunitSuite(yaml.split('\n')[0]))


class XunitSuite(object):
    """The status reports of a suite of tests"""
    def __init__(self, name):
        self.name = name
