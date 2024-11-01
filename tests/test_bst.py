import numpy as np
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../src")
from structures.bst import BST

class TestBST(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
    
    def test_empty_bst(self):
        self.assertEqual(0, self.bst.get_size())
        self.assertCountEqual([], self.bst.get_nodes_as_list())
        self.assertEqual(0, self.bst.query(0))
        self.assertEqual(None, self.bst.get(0))
    
    def test_insert(self):
        self.bst.insert(1)
        self.assertEqual(1, self.bst.get_size())
        self.assertCountEqual([1], [n.get_key() for n in self.bst.get_nodes_as_list()])
        self.assertEqual(0, self.bst.query(0))
        self.assertEqual(1, self.bst.query(1))
    
    def test_multi_insert(self):
        keys = np.arange(0, 100, 1)
        for key in keys:
            self.bst.insert(key)
        self.assertEqual(len(keys), self.bst.get_size())
        self.assertCountEqual(np.sort(keys), [n.get_key() for n in self.bst.get_nodes_as_list()])
        for key in keys:
            self.assertEqual(1, self.bst.query(key))

    def test_query_nonexistent(self):
        node = self.bst.query(0)
        self.assertEqual(0, node)

    def test_get_one(self):
        self.bst.insert(1)
        node = self.bst.get(1)
        self.assertEqual(1, node.get_key())

    def test_get_nonexistent(self):
        node = self.bst.get(0)
        self.assertEqual(None, node)
    
    def test_get_multi(self):
        keys = np.arange(0, 100, 1)
        for key in keys:
            self.bst.insert(key)
        for key in keys:
            node = self.bst.get(key)
            self.assertEqual(key, node.get_key())
            if key > 0:
                self.assertEqual(key - 1, node.get_parent().get_key())

    def test_remove_one(self):
        keys = np.arange(0, 10, 1)
        for key in keys:
            self.bst.insert(key)
        removed_node = self.bst.remove(5)
        self.assertEqual(5, removed_node.get_key())
        self.assertEqual(None, removed_node.get_left_child())
        self.assertEqual(None, removed_node.get_right_child())
        self.assertEqual(None, removed_node.get_parent())
        self.assertCountEqual([0, 1, 2, 3, 4, 6, 7, 8, 9], [n.get_key() for n in self.bst.get_nodes_as_list()])
    
    def test_remove_nonexistent(self):
        node = self.bst.remove(0)
        self.assertEqual(None, node)
    
    def test_remove_subtree(self):
        keys = np.arange(0, 10, 1)
        for key in keys:
            self.bst.insert(key)
        removed_node = self.bst.remove(5, subtree=True)
        removed_tree = BST(removed_node)
        self.assertCountEqual([0, 1, 2, 3, 4], [n.get_key() for n in self.bst.get_nodes_as_list()])
        self.assertCountEqual([5, 6, 7, 8, 9], [n.get_key() for n in removed_tree.get_nodes_as_list()])
    
    def test_remove_all(self):
        keys = np.arange(0, 10, 1)
        for key in keys:
            self.bst.insert(key)
        for key in keys:
            self.bst.remove(key)
        self.assertEqual(None, self.bst.get_root())

    def test_boomerang(self):
        keys = [2, 1, 3]
        for key in keys:
            self.bst.insert(key)
        self.bst.remove(1)
        self.assertCountEqual([2, 3], [n.get_key() for n in self.bst.get_nodes_as_list()])
        self.bst.remove(3)
        self.assertCountEqual([2], [n.get_key() for n in self.bst.get_nodes_as_list()])
    
    def test_balanced(self):
        keys = [5, 3, 1, 2, 4, 7, 6, 8, 9]
        for key in keys:
            self.bst.insert(key)
        keys = np.sort(keys).tolist()
        self.assertCountEqual(keys, [n.get_key() for n in self.bst.get_nodes_as_list()])
        remove_order = [2, 5, 1, 8, 3, 4, 9]
        for value in remove_order:
            keys.remove(value)
            self.bst.remove(value)
            self.assertCountEqual(keys, [n.get_key() for n in self.bst.get_nodes_as_list()])
        
