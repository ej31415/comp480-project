import numpy as np
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../src")
from structures.rb_tree import RBTree

class TestRBTree(unittest.TestCase):

    def setUp(self):
        self.rbtree = RBTree()

    def test_equality(self):
        pointer = self.rbtree
        self.assertEqual(self.rbtree, pointer)
        self.assertEqual(hash(self.rbtree), hash(pointer))

        root = self.rbtree.get_root()
        copy = root
        self.assertEqual(root, copy)
        self.assertEqual(hash(root), hash(copy))

    def test_empty_bst(self):
        self.assertEqual(0, self.rbtree.get_size())
        self.assertCountEqual([], self.rbtree.get_nodes_as_list())
        # self.assertEqual(0, self.rbtree.query(0))
        # self.assertEqual(None, self.rbtree.get(0))
    
    def test_insert_one(self):
        self.rbtree.insert(1)
        self.assertEqual(1, self.rbtree.get_size())
        self.assertCountEqual([1], [n.get_key() for n in self.rbtree.get_nodes_as_list()])
        self.assertCountEqual(["black"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])

    def test_multi_insert(self):
        keys = [11, 2, 14 ,15, 1, 7, 5, 8, 4]
        for key in keys:
            self.rbtree.insert(key)
        self.assertEqual(9, self.rbtree.get_size())
        self.assertCountEqual(np.sort(keys), [n.get_key() for n in self.rbtree.get_nodes_as_list()])
        self.assertCountEqual(["black", "red", "red", "black", "black", "black", "red", "black", "red"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
    
    def test_query(self):
        keys = [11, 2, 14 ,15, 1, 7, 5, 8, 4]
        for key in keys:
            self.rbtree.insert(key)
        self.assertEqual(9, self.rbtree.get_size())
        for key in keys:
            self.assertEqual(1, self.rbtree.query(key))
        self.assertEqual(0, self.rbtree.query(0))
        self.assertEqual(0, self.rbtree.query(3))
        self.assertEqual(0, self.rbtree.query(12))

    def test_removal(self):
        keys = [11, 2, 14 ,15, 1, 7, 5, 8, 4]
        for key in keys:
            self.rbtree.insert(key)
        self.assertEqual(9, self.rbtree.get_size())
        self.assertEqual(7, self.rbtree.get_root().get_key())
        self.assertCountEqual(["black", "red", "red", "black", "black", "black", "red", "black", "red"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
        self.rbtree.remove(15)
        self.assertEqual(8, self.rbtree.get_size())
        self.assertCountEqual(["black", "red", "red", "black", "black", "black", "red", "black"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
        self.rbtree.remove(4)
        self.assertEqual(7, self.rbtree.get_size())
        self.assertCountEqual(["black", "red", "black", "black", "black", "red", "black"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
        self.rbtree.remove(1)
        self.assertEqual(6, self.rbtree.get_size())
        self.assertCountEqual(["black", "red", "black", "black", "red", "black"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
        self.rbtree.remove(11)
        self.assertEqual(5, self.rbtree.get_size())
        self.assertCountEqual(["black", "red", "black", "black", "red"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])
        self.rbtree.remove(7)
        self.assertEqual(4, self.rbtree.get_size())
        self.assertEqual(8, self.rbtree.get_root().get_key())
        self.assertCountEqual(["black", "black", "black", "red"], [n.get_color() for n in self.rbtree.get_nodes_as_list()])

    def test_size(self):
        orig = self.rbtree.size()
        keys = [5, 3, 1, 2, 4, 7, 6, 8, 9]
        for key in keys:
            self.rbtree.insert(key)
        new = self.rbtree.size()
        self.assertEqual(self.rbtree.get_root().get_left_child().size(), self.rbtree.get_root().get_right_child().size())
        self.assertTrue(abs((new - orig) / 9 - self.rbtree.get_root().size()) <= 56)    # one object reference size