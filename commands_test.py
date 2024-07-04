#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import commands

"""
TODO: Pull test data from external dataset, rather than
using examples in the test file.

TODO: Individual tests for rules in the engine.
"""

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.good_vpp_data = {
            "name": "Ampharos",
            "revenue_percentage": 0.5,
            "daily_fee": 4
        }
    def tests_working(self):
        print("Tests working")

    def test_good_vpp(self):
        """
        A basic sytax and good path check.
        """
        # Setup
        new_vpp = self.good_vpp_data
        vpps_before = len(commands.VPPS)
        # Execute
        commands.create_vpp(**new_vpp)
        # Assert
        vpps_after = len(commands.VPPS)
        number_is_correct = vpps_after - vpps_before == 1
        if not number_is_correct:
            raise Exception("Number of VPPS did not increment by 1")

    def test_bad_vpp(self):
        """
        Fails to instantiate a VPP with a bad revenue percentage.
        """
        # Setup
        new_vpp = dict(**self.good_vpp_data)
        new_vpp["revenue_percentage"] = 1.5
        # Execute/Assert
        self.assertRaises(Exception, commands.create_vpp, **new_vpp)
        
        
        

if __name__ == "__main__":
    unittest.main()
