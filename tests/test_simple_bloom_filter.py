import numpy as np
import unittest
import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(src_path)
from structures.simple_bloom_filter import BloomFilterSimple

class TestBloomFilterSimple(unittest.TestCase):

    def setUp(self):
        self.bloom_filter = BloomFilterSimple()

    def test_insert_one(self):
        '''Test inserting a number'''
        self.assertTrue(self.bloom_filter.insert(1))
        self.assertEqual(1, self.bloom_filter.query(1))
    
    def test_insert_multi(self):
        '''Test multiple insertions'''
        np.random.seed(123)
        insert_values = [str(val).encode() for val in np.random.choice(range(1, 1000000), size=100000)]
        for val in insert_values:
            self.bloom_filter.insert(val)
        for val in insert_values:
            self.assertEqual(1, self.bloom_filter.query(val))
