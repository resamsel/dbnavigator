#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import unittest

from os import path
from tests.generator import test_generator, params
from tests.sources import init_sources
from dbnav import grapher

DIR = path.dirname(__file__)
TEST_CASES = map(
    lambda p: path.basename(p),
    glob.glob(path.join(DIR, 'resources/testcase-*')))

init_sources(DIR)


class OutputTestCase(unittest.TestCase):
    def setUp(self):  # noqa
        self.maxDiff = None


def load_suite():
    command = 'dbgraph'
    for tc in TEST_CASES:
        test_name = 'test_%s_%s' % (command, tc.replace('-', '_'))
        test = test_generator(grapher, command, DIR, tc)
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    return suite
