import logging
import numpy as np
import sys

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
    All `None` nodes are considered to be black.
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

        def __eq__(self, other):
            '''Override equality check to implement hashing.'''
            if type(other) != type(self):
                return False
            return self.get_key() == other.get_key()
        
        def __hash__(self):
            '''Override hashing.'''
            return hash(self.get_key())
        
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

        def get_subtree_size(self, none)->int:
            '''Returns the number of nodes in the subtree rooted at this node.'''
            count = 1
            if self.__left != none:
                count += self.__left.get_subtree_size(none)
            if self.__right != none:
                count += self.__right.get_subtree_size(none)
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

        def size(self)->int:
            return sys.getsizeof(self) + sys.getsizeof(self.__key) + sys.getsizeof(self.__left) + sys.getsizeof(self.__right) + sys.getsizeof(self.__parent) + sys.getsizeof(self.__color)  
        
    def __init__(self):
        '''Initializes the tree by setting the root to None.'''
        self.__null = self.Node(key=None, color="black")
        self.__root = self.__null
        logger.info("Initialized a red-black tree...")

    def __eq__(self, other):
        '''Override equality check for hashing.'''
        if not type(other) is RBTree:
            return False
        return self.get_root() == other.get_root()
    
    def __hash__(self):
        '''Override hashing.'''
        return hash(self.get_root())

    def __transplant(self, u, v):
        """Transplant replaces the subtree rooted at node `u` with the subtree rooted at node `v`.
        This function will only be called internally, so both `u` and `v` are guaranteed to exist.
        """
        if u.get_parent() == None:
            self.__root = v
        elif u == u.get_parent().get_left_child():
            u.get_parent().set_left_child(v)
        else:
            u.get_parent().set_right_child(v)
        
        if v != None:
            v.set_parent(u.get_parent())

    def __traverse_helper(self, node):
        '''Gets the keys of all nodes into a list, using inorder traversal.'''
        if node != self.__null:
            return np.concatenate((self.__traverse_helper(node.get_left_child()), [node], self.__traverse_helper(node.get_right_child())))
        return []
    
    def __left_rotate(self, node):
        """Rotates to this node to the left.
        The right child now becomes the parent of this node, replacing this node at its former location.
        """
        right_child = node.get_right_child()
        node.set_right_child(right_child.get_left_child())
        if right_child.get_left_child() != self.__null:
            right_child.get_left_child().set_parent(node)
        right_child.set_parent(node.get_parent())
        if node.get_parent() == None:
            self.__root = right_child
        elif node == node.get_parent().get_left_child():
            node.get_parent().set_left_child(right_child)
        else:
            node.get_parent().set_right_child(right_child)
        right_child.set_left_child(node)
        node.set_parent(right_child)

    def __right_rotate(self, node):
        """Rotates to this node to the right.
        The left child now becomes the parent of this node, replacing this node at its former location.
        """
        left_child = node.get_left_child()
        node.set_left_child(left_child.get_right_child())
        if left_child.get_right_child() != self.__null:
            left_child.get_right_child().set_parent(node)
        left_child.set_parent(node.get_parent())
        if node.get_parent() == None:
            self.__root = left_child
        elif node == node.get_parent().get_left_child():
            node.get_parent().set_left_child(left_child)
        else:
            node.get_parent().set_right_child(left_child)
        left_child.set_right_child(node)
        node.set_parent(left_child)

    def __insert_fixup(self, node):
        '''Helper function to maintain RBTree invariants for node insertion.'''
        while node.get_parent() != None and node.find_grandparent() != None and node.get_parent().get_color() == "red":
            if node.get_parent() == node.find_grandparent().get_left_child():
                uncle = node.find_uncle()
                if uncle.get_color() == "red":
                    node.get_parent().set_color("black")
                    uncle.set_color("black")
                    node.find_grandparent().set_color("red")
                    node = node.find_grandparent()
                else:
                    if node == node.get_parent().get_right_child():
                        node = node.get_parent()
                        self.__left_rotate(node)
                    node.get_parent().set_color("black")
                    node.find_grandparent().set_color("red")
                    self.__right_rotate(node.find_grandparent())
            else:
                uncle = node.find_uncle()
                if uncle.get_color() == "red":
                    node.get_parent().set_color("black")
                    uncle.set_color("black")
                    node.find_grandparent().set_color("red")
                    node = node.find_grandparent()
                else:
                    if node == node.get_parent().get_left_child():
                        node = node.get_parent()
                        self.__right_rotate(node)
                    node.get_parent().set_color("black")
                    node.find_grandparent().set_color("red")
                    self.__left_rotate(node.find_grandparent())
        self.__root.set_color("black")

    def __remove_fixup(self, node):
        '''Helper function to maintain RBTree invariants for node removal.'''
        while node != self.__root and node.get_color() == "black":
            parent = node.get_parent()
            if node == parent.get_left_child():
                sibling = parent.get_right_child()
                if sibling.get_color() == "red":
                    sibling.set_color("black")
                    parent.set_color("red")
                    self.__left_rotate(parent)
                    sibling = node.get_parent().get_right_child()
                if sibling.get_left_child().get_color() == "black" and sibling.get_right_child().get_color() == "black":
                    sibling.set_color("red")
                    node = node.get_parent()
                else:
                    parent = node.get_parent()
                    if sibling.get_right_child().get_color() == "black":
                        sibling.get_left_child().set_color("black")
                        sibling.set_color("red")
                        self.__right_rotate(sibling)
                        sibling = parent.get_right_child()
                    sibling.set_color(parent.get_color())
                    parent.set_color("black")
                    sibling.get_right_child().set_color("black")
                    self.__left_rotate(parent)
                    node = self.__root
            else:
                sibling = parent.get_left_child()
                if sibling != None and sibling.get_color() == "red":
                    sibling.set_color("black")
                    parent.set_color("red")
                    self.__right_rotate(parent)
                    sibling = node.get_parent().get_left_child()
                if sibling.get_left_child().get_color() == "black" and sibling.get_right_child().get_color() == "black":
                    sibling.set_color("red")
                    node = node.get_parent()
                else:
                    parent = node.get_parent()
                    if sibling.get_left_child().get_color() == "black":
                        sibling.get_right_child().set_color("black")
                        sibling.set_color("red")
                        self.__left_rotate(sibling)
                        sibling = parent.get_left_child()
                    sibling.set_color(parent.get_color())
                    parent.set_color("black")
                    sibling.get_left_child().set_color("black")
                    self.__right_rotate(parent)
                    node = self.__root
        node.set_color("black")
        
    def get_root(self):
        '''Returns the root node of the RBTree.'''
        return self.__root
    
    def get_null(self):
        '''Returns the sentinel node of the RBTree.'''
        return self.__null
    
    def get_size(self):
        '''Returns the number of the nodes in the RBTree.'''
        if self.__root == self.__null:
            return 0
        return self.__root.get_subtree_size(self.__null)
    
    def get_nodes_as_list(self):
        '''Returns a list of the keys of all nodes in the RBTree, in order.'''
        curr = self.__root
        node_keys = self.__traverse_helper(curr)
        return node_keys
    
    def min_node(self, node):
        '''Finds and returns the minimum keyed node in the tree rooted at this node.'''
        while node.get_left_child() != self.__null:
            node = node.get_left_child()
        return node 

    def insert(self, item)->bool:
        """Inserts a given item into the RBTree as a node.
        If the item is already in the RBTree, then the insertion fails.
        
        Return a boolean representing successful insertion.
        """
        # Search for the appropriate location
        prev = None
        curr = self.__root
        while curr != self.__null:
            prev = curr
            if item < curr.get_key():
                curr = curr.get_left_child()
            elif item > curr.get_key():
                curr = curr.get_right_child()
            else:
                logger.debug("Insertion FAILED: item already exists")
                return False
        
        # Create and insert the new node
        new_node = self.Node(item, left=self.__null, right=self.__null, parent=prev)
        if prev == None:
            self.__root = new_node
        elif item < prev.get_key():
            prev.set_left_child(new_node)
        else:
            prev.set_right_child(new_node)
        self.__insert_fixup(new_node)
        logger.debug("Inserted item")
        return True
    
    def query(self, item)->int:
        """Checks the BST for a given item's existence.
        
        Returns 1 if exists, 0 otherwise.
        """
        curr = self.__root
        while curr != self.__null:
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                logger.debug("Item is found")
                return 1
        logger.debug("Item is not not found")
        return 0
    
    def remove(self, item):
        """Removes the node that contains item as its key.
        If the given item does not exist in the BST as a node key, the function returns None.
        """
        # Search for the node to remove
        curr = self.__root
        while curr != self.__null:
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                break
            
        if curr == self.__null:
            logger.debug("Item is not found")
            return None
        
        # Process removal
        original_color = curr.get_color()
        fix_node = curr
        if curr.get_left_child() == self.__null:
            self.__transplant(curr, curr.get_right_child())
            fix_node = curr.get_right_child()
            curr.set_right_child(None)
        elif curr.get_right_child() == None:
            self.__transplant(curr, curr.get_left_child())
            fix_node = curr.get_left_child()
            curr.set_left_child(None)
        else:
            x = self.min_node(curr.get_right_child())
            original_color = x.get_color()
            fix_node = x.get_right_child()
            if x.get_parent() == curr:
                fix_node.set_parent(x)
            else:
                self.__transplant(x, x.get_right_child())
                x.set_right_child(curr.get_right_child())
                x.get_right_child().set_parent(x)
            self.__transplant(curr, x)
            x.set_left_child(curr.get_left_child())
            x.get_left_child().set_parent(x)
            x.set_color(curr.get_color())
        
        if original_color == "black":
            self.__remove_fixup(fix_node)
        
    def size(self)->int:
        return sys.getsizeof(self) + sum([node.size() for node in self.get_nodes_as_list()])