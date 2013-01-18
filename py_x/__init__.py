"""Copyright 2013 - Per Fagrell """
import yaml
from py_x.core import Xunit, XunitSuite, XunitTest

def from_yaml(yaml_input):
    """Parse provided yaml and instantiate an Xunit object from that"""
    report_description = yaml.load(yaml_input)
    report = Xunit()

    for test_suite in report_description:
        name, data = test_suite.items()[0]
        suite = XunitSuite(name)
        report.append(suite)

        if data is None:
            continue 

        for test in data:
            suite.append(XunitTest(test['name']))

    return report


