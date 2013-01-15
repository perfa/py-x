py-x
====

Python module to ease creating XUnit XML.

When integrating various test automation scripts, regression suites and so on with a continuous integration server like Jenkins one would often like to just lean back and let the existing violations plugin setup deal with pass/fail counts and plotting charts. Py-x is a module for simplifying the creation of XUnit compatible test results in XML.

Feeding your results
--------------------
There will be several different ways of reporting test results to the py-x module:
* State-machine style add-a-suite add-a-test add-a-test add-a-test 
* TestSuite and Test mixin classes
* YAML format data - this will also work on the command line.


