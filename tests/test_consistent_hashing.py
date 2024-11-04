import numpy as np
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../src")
from structures.consistent_hashing import ConsistentHashing

class TestConsistentHashing(unittest.TestCase):

    def setUp(self):
        self.ch = ConsistentHashing()

    def test_insert_one(self):
        '''Test inserting a number'''
        self.ch.insert(1)
        self.assertEqual(1, self.ch.query(1))
    
    def test_insert_multi(self):
        '''Test multiple insertions'''
        np.random.seed(123)
        insert_values = np.random.choice(range(1, 1000000), size=100000)
        for val in insert_values:
            self.ch.insert(val)
        for val in insert_values:
            self.assertEqual(1, self.ch.query(val))

    def test_remove(self):
        keys = np.arange(0, 100, 1)
        for key in keys:
            self.ch.insert(key)
        
        removed_keys = [4, 13, 8, 75, 20, 61]
        for key in removed_keys:
            self.ch.remove(key)
        
        for key in keys:
            if key not in removed_keys:
                self.assertEqual(1, self.ch.query(key))
            else:
                self.assertEqual(0, self.ch.query(key))