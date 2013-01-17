"""Copyright 2013 - Per Fagrell """
import yaml
from py_x.core import Xunit, XunitSuite, XunitTest

def from_yaml(yaml_input):
    """Parse provided yaml and instantiate an Xunit object from that"""
    report_description = yaml.load(yaml_input)
    return Xunit(XunitSuite(yaml.split('\n')[0]))


