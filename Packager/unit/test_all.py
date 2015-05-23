#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import unittest
#from somefile import TestSomething

testsuite = unittest.TestSuite()
#testsuite.addTest(unittest.makeSuite(TestSomething))
unittest.TextTestRunner(verbosity=2).run(testsuite)
