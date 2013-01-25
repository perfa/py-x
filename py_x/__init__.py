import yaml
from py_x.core import Xunit, XunitSuite, XunitTest

__author__ = "Per Fagrell"


def from_yaml(yaml_input):
    """Parse provided yaml and instantiate an Xunit object from that"""
    report_description = yaml.load(yaml_input)
    report = Xunit()

    for test_suite, data in report_description.items():
        suite = XunitSuite(test_suite)
        report.append(suite)

        if data is None:
            continue

        for test, test_data in data.items():
            test_result = XunitTest(test)
            if test_data and 'status' in test_data:
                test_result.status = test_data['status']
            suite.append(test_result)

    return report


