import numpy as np
import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../src")
from structures.cuckoo_filter import CuckooFilter

class TestCuckoo(unittest.TestCase):

    def setUp(self):
        self.filter = CuckooFilter()

    def test_insert_one(self):
        '''Test inserting a number'''
        self.filter.insert(1)
        self.assertEqual(1, self.filter.query(1))
    
    def test_insert_multi(self):
        '''Test multiple insertions'''
        np.random.seed(123)
        insert_values = np.random.choice(range(1, 1000000), size=100000)
        for val in insert_values:
            self.filter.insert(val)
        for val in insert_values:
            self.assertEqual(1, self.filter.query(val))
    
    def test_remove_one(self):
        '''Test removing a number'''
        self.filter.insert(1)
        self.filter.remove(1)
        self.assertEqual(0, self.filter.query(1))
    
    def test_remove_multi(self):
        '''Test removing multiple numbers'''
        np.random.seed(123)
        insert_values = np.random.choice(range(1, 1000000), size=100000)
        for val in insert_values:
            self.filter.insert(val)
        for val in insert_values:
            self.filter.remove(val)
            self.assertEqual(0, self.filter.query(val))
    