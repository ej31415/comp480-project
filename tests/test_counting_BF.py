import numpy as np
import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/structures")))
from counting_bloom_filter import CountingBloomFilter

class TestCountingBloomFilter(unittest.TestCase):

    def setUp(self):
        self.counting_BF = CountingBloomFilter()

    def test_insert_one(self):
        '''Test inserting a number'''
        self.counting_BF.insert(1)
        self.assertEqual(1, self.counting_BF.query(1))
    
    def test_insert_multi(self):
        '''Test multiple insertions'''
        np.random.seed(123)
        insert_values = np.random.choice(range(1, 1000000), size=100000)
        for val in insert_values:
            self.counting_BF.insert(val)
        for val in insert_values:
            self.assertEqual(1, self.counting_BF.query(val))
    
    def test_remove_one(self):
        '''Test removing a number'''
        self.counting_BF.insert(1)
        self.counting_BF.remove(1)
        self.assertEqual(0, self.counting_BF.query(1))

    def test_remove_multi(self):
        '''Test removing multiple numbers'''
        np.random.seed(123)
        insert_values = np.random.choice(range(1, 1000000), size=100000)
        for val in insert_values:
            self.counting_BF.insert(val)
        for val in insert_values:
            orig = self.counting_BF.min_count(val)
            self.counting_BF.remove(val)
            new = self.counting_BF.min_count(val)
            self.assertEqual(1, orig - new)