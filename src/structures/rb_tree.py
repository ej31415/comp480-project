import logging
import numpy as np

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class RBTree:
    """
    RBTree represents a red-black tree.
    A red-black tree consists of a root node, which defines the red-black tree, similar to a binary search tree.
    Each node in the tree has a key and two children nodes, where the key of the left child is strictly less than the key of this node
    while the key of the right child is strictly greater than the key of this node. All keys must be unique in the RBTree.
    One key assumption is that the keys stored in into a RBTree are comparable by `>` and `<`.
    The five invariants are: (1) every node is either red or blcak, (2) root is black, (3) every leaf, considered None, is black,
    (4) both children of a red node are black, (5) for each node, all simple paths to descendent leaves contain the same number of black nodes.
    """

    class Node:
        """
        Node represents a single node in the red-black tree.
        A node consists of a key and two children nodes. A parent pointer is kept to support functions.
        The color of a ndoe is either red or black.
        """

        def __init__(self, key, color="red", left=None, right=None, parent=None):
            '''Initialize the node to the specified key. The children and parent are set to None by default while the color is red.'''
            self.__key = key
            self.__color = color
            self.__left = left
            self.__right = right
            self.__parent = parent
        
        def get_key(self):
            '''Returns the key of this node.'''
            return self.__key
        
        def get_color(self):
            '''Returns the color of this node.'''
            return self.__color
        
        def get_left_child(self):
            '''Returns the left child of this node.'''
            return self.__left
        
        def get_right_child(self):
            '''Returns the right child of this node.'''
            return self.__right
        
        def get_parent(self):
            '''Returns the parent of this node.'''
            return self.__parent
        
        def set_color(self, color):
            """Sets this node's color. The color should either be red or black.
            If the color is not "red" or "black," an exception will be raised."""
            if color != "red" and color != "black":
                raise Exception("invalid color of red-black tree node")
            self.__color = color
        
        def set_left_child(self, node):
            '''Sets this node's left child.'''
            self.__left = node
        
        def set_right_child(self, node):
            '''Sets this node's right child.'''
            self.__right = node
        
        def set_parent(self, node):
            '''Sets this node's parent.'''
            self.__parent = node

        def get_subtree_size(self)->int:
            '''Returns the number of nodes in the subtree rooted at this node.'''
            count = 1
            if self.__left != None:
                count += self.__left.get_subtree_size()
            if self.__right != None:
                count += self.__right.get_subtree_size()
            return count
        
        def find_grandparent(self):
            '''Finds and returns the grandparent node, if one exists.'''
            if self.get_parent() == None:
                return None
            return self.get_parent().get_parent()
        
        def find_sibling(self):
            '''Finds and returns the sibling node, if one exists.'''
            if self.get_parent() == None:
                return None
            if self == self.get_parent().get_left_child():
                return self.get_parent().get_right_child()
            return self.get_parent().get_left_child()
        
        def find_uncle(self):
            '''Finds and returns the unclode node, if one exists.'''
            if self.get_parent() == None:
                return None
            return self.get_parent().find_sibling()
        
