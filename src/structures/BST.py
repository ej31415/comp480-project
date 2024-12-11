import logging
import numpy as np
import sys

from sklearn.utils import murmurhash3_32

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class BST:
    """
    BST represents a binary search tree.
    A binary search tree is consisted of a root node, which defines the BST.
    Each node in the tree has a key and two children nodes, where the key of the left child is strictly less than the key of this node
    while the key of the right child is strictly greater than the key of this node. All keys must be unique in the BST.
    One key assumption is that the keys stored in into a BST are comparable by `>` and `<`.
    """
    
    class Node:
        """
        Node represents a single node in the binary search tree.
        A node consists of a key and two children nodes. A parent pointer is kept to support functions.
        """

        def __init__(self, key, value=None, left=None, right=None, parent=None):
            '''Initialize the node to the specified key. The children and parent are set to None by default unless specified.'''
            self.__key = key
            self.__value = value
            self.__left = left
            self.__right = right
            self.__parent = parent

        def __eq__(self, other):
            '''Override equality check to implement hashing.'''
            if not isinstance(other, BST.Node):
                return False
            return self.get_key() == other.get_key()
        
        def __hash__(self):
            '''Override hashing.'''
            return murmurhash3_32(self.__key)
        
        def get_key(self):
            '''Returns the key of this node.'''
            return self.__key
        
        def get_value(self):
            '''Returns the value of this node.'''
            return self.__value
        
        def get_left_child(self):
            '''Returns the left child of this node.'''
            return self.__left
        
        def get_right_child(self):
            '''Returns the right child of this node.'''
            return self.__right
        
        def get_parent(self):
            '''Returns the parent of this node.'''
            return self.__parent
        
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
        
        def size(self)->int:
            return sys.getsizeof(self) + sys.getsizeof(self.__key) + sys.getsizeof(self.__left) + sys.getsizeof(self.__right) + sys.getsizeof(self.__parent)
        
    def __init__(self, root=None):
        '''Initializes the tree by setting the root node to None.'''
        self.__root = root
        logger.info("Initialized a binary search tree...")

    def __eq__(self, other):
        '''Override equality check for hashing.'''
        if not isinstance(other, BST):
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
        if node != None:
            return np.concatenate((self.__traverse_helper(node.get_left_child()), [node], self.__traverse_helper(node.get_right_child())))
        return []

    def get_root(self):
        '''Returns the root node of the BST.'''
        return self.__root
    
    def get_null(self):
        '''Returns the null pointer of the BST.'''
        return None
    
    def get_size(self):
        '''Returns the number of the nodes in the BST.'''
        if self.__root == None:
            return 0
        return self.__root.get_subtree_size()
    
    def get_nodes_as_list(self):
        '''Returns a list of the keys of all nodes in the BST, in order.'''
        curr = self.__root
        node_keys = self.__traverse_helper(curr)
        return node_keys
    
    def min_node(self, node):
        '''Finds and returns the minimum keyed node in the tree rooted at this node.'''
        while node.get_left_child() != None:
            node = node.get_left_child()
        return node
    
    def successor(self, node):
        """Finds and returns the successor of a node.
        This function will only be called internally, so the node is guaranteed to exist.
        """
        if node.get_right_child() != None:
            return node.get_right_child().min_node()
        
        curr = node
        next = curr.get_parent()
        while next != None and curr == next.get_right_child():
            curr = next
            next = next.get_parent()
        return next
    
    def insert(self, item, value=None)->bool:
        """Inserts a given item into the BST as a node.
        If the item is already in the BST, then the insertion fails.
        
        Return a boolean representing successful insertion.
        """
        # Search for appropriate location
        prev = None
        curr = self.__root
        while curr != None:
            prev = curr
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                logger.debug("Insertion FAILED: item already exists")
                return False
        
        # Insert under parent node
        new_node = self.Node(item, value=value)
        if prev != None:
            new_node.set_parent(prev)
            prev_key = prev.get_key()
            if item <= prev_key:
                prev.set_left_child(new_node)
            else:
                prev.set_right_child(new_node)
        else:
            self.__root = new_node
        logger.debug("Inserted item")
        return True

    def query(self, item)->int:
        """Checks the BST for a given item's existence.
        
        Returns 1 if exists, 0 otherwise.
        """
        curr = self.__root
        while curr != None:
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                logger.debug("Item is found")
                return 1
        logger.debug("Item is not found")
        return 0
    
    def get(self, item):
        """Returns the node that stores a given item as the key.
        If the item does not exist in the BST as a a node key, returns None.
        """
        curr = self.__root
        while curr != None:
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                logger.debug("Target node is found")
                return curr
        logger.debug("Target node is NOT found")
        return None
    
    def remove(self, item, subtree=False):
        """Removes the node that contains item as its key.
        `subtree` is an optional boolean parameter that removes either only the node if False or the node and its subtree if True.
        
        If `subtree` is True, the function returns the node with its subtree. Otherwise, only the node is returned.
        If the given item does not exist in the BST as a node key, the function returns None.
        """
        # Search for appropriate location
        curr = self.__root
        while curr != None:
            curr_key = curr.get_key()
            if item < curr_key:
                curr = curr.get_left_child()
            elif item > curr_key:
                curr = curr.get_right_child()
            else:
                break
        
        # Node is not found
        if curr == None:
            logger.debug("Target node is NOT found")
            return None

        # Remove node and maybe its subtree from the BST
        if not subtree:
            if curr.get_left_child() == None:
                self.__transplant(curr, curr.get_right_child())
            elif curr.get_right_child() == None:
                self.__transplant(curr, curr.get_left_child())
            else:
                successor = curr.get_right_child().min_node()
                if successor.get_parent() != curr:
                    self.__transplant(successor, successor.get_right_child())
                    successor.set_right_child(curr.get_right_child())
                    successor.get_right_child().set_parent(successor)
                self.__transplant(curr, successor)
                successor.set_left_child(curr.get_left_child())
                successor.get_left_child().set_parent(successor)
            curr.set_left_child(None)
            curr.set_right_child(None)
        else:
            if curr == curr.get_parent().get_left_child():
                curr.get_parent().set_left_child(None)
            else:
                curr.get_parent().set_right_child(None)
        curr.set_parent(None)
        logger.debug("Target node is removed, removing subtree is %s", subtree)
        return curr

    def size(self)->int:
        return sys.getsizeof(self) + sum([node.size() for node in self.get_nodes_as_list()])