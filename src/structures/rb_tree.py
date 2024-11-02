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
    
        def min_node(self):
            '''Finds and returns the minimum keyed node in the tree rooted at this node.'''
            curr = self
            while curr.get_left_child() != None:
                curr = curr.get_left_child()
            return curr        
        
    def __init__(self):
        '''Initializes the tree by setting the root to None.'''
        self.__root = None
        logger.info("Initialized a red-black tree...")

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
    
    def __left_rotate(self, node):
        """Rotates to this node to the left.
        The right child now becomes the parent of this node, replacing this node at its former location.
        """
        right_child = node.get_right_child()
        node.set_right_child(None if right_child.get_left_child() == None else right_child.get_left_child())
        if right_child.get_left_child() != None:
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
        node.set_left_child(None if left_child.get_right_child() == None else left_child.get_right_child())
        if left_child.get_right_child() != None:
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
        while node.get_parent() != None and node.get_parent().get_color() == "red":
            uncle = node.find_uncle()
            if uncle != None and uncle.get_color() == "red":
                node.get_parent().set_color("black")
                uncle.set_color("black")
                node.find_grandparent().set_color("red")
                node = node.find_grandparent()
            elif node == node.get_parent().get_right_child():
                node = node.get_parent()
                self.__left_rotate(node)
            else:
                node.get_parent().set_color("black")
                node.find_grandparent().set_color("red")
                self.__right_rotate(node.find_grandparent())
        self.__root.set_color("black")

    def __remove_fixup(self, node, parent, left):
        '''Helper function to maintain RBTree invariants for node removal.'''
        print(f"Replacing with {None if node == None else node.get_key()}, where left={left} and color={'black' if node == None else node.get_color()}")
        while node != self.__root and (node == None or node.get_color() == "black"):
            if left:
                sibling = parent.get_right_child()
                if sibling != None and sibling.get_color() == "red":
                    sibling.set_color("black")
                    parent.set_color("red")
                    self.__left_rotate(parent)
                    sibling = parent.get_right_child()
                if (sibling.get_left_child() == None or sibling.get_left_child().get_color() == "black") and (sibling.get_right_child() == None or sibling.get_right_child().get_color() == "black"):
                    sibling.set_color("red")
                    node = parent
                    parent = parent.get_parent()
                    if parent != None and parent.get_right_child() == node:
                        left = False
                else:
                    if sibling.get_right_child() == None or sibling.get_right_child().get_color() == "black":
                        sibling.get_left_child().set_color("black")
                        sibling.set_color("red")
                        self.__right_rotate(sibling)
                        sibling = parent.get_right_child()
                    sibling.set_color(parent.get_color())
                    parent.set_color("black")
                    if sibling.get_right_child() != None:
                        sibling.get_right_child().set_color("black")
                    self.__left_rotate(parent)
                    node = self.__root
            else:
                sibling = parent.get_left_child()
                if sibling != None and sibling.get_color() == "red":
                    sibling.set_color("black")
                    parent.set_color("red")
                    self.__right_rotate(parent)
                    sibling = parent.get_left_child()
                if (sibling.get_left_child() == None or sibling.get_left_child().get_color() == "black") and (sibling.get_right_child() == None or sibling.get_right_child().get_color() == "black"):
                    sibling.set_color("red")
                    node = parent
                    parent = parent.get_parent()
                    parent = parent.get_parent()
                    if parent != None and parent.get_right_child() == node:
                        left = False
                else:
                    if sibling.get_left_child() == None or sibling.get_left_child().get_color() == "black":
                        sibling.get_right_child().set_color("black")
                        sibling.set_color("red")
                        self.__left_rotate(sibling)
                        sibling = parent.get_left_child()
                    sibling.set_color(parent.get_color())
                    parent.set_color("black")
                    if sibling.get_left_child() != None:
                        sibling.get_left_child().set_color("black")
                    self.__right_rotate(parent)
                    node = self.__root
        node.set_color("black")
        
    def get_root(self):
        '''Returns the root node of the RBTree.'''
        return self.__root
    
    def get_size(self):
        '''Returns the number of the nodes in the RBTree.'''
        if self.__root == None:
            return 0
        return self.__root.get_subtree_size()
    
    def get_nodes_as_list(self):
        '''Returns a list of the keys of all nodes in the RBTree, in order.'''
        curr = self.__root
        node_keys = self.__traverse_helper(curr)
        return node_keys

    def insert(self, item)->bool:
        """Inserts a given item into the RBTree as a node.
        If the item is already in the RBTree, then the insertion fails.
        
        Return a boolean representing successful insertion.
        """
        # Search for the appropriate location
        prev = None
        curr = self.__root
        while curr != None:
            prev = curr
            if item < curr.get_key():
                curr = curr.get_left_child()
            elif item > curr.get_key():
                curr = curr.get_right_child()
            else:
                logger.debug("Insertion FAILED: item already exists")
                return False
        
        # Create and insert the new node
        new_node = self.Node(item, parent=prev)
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
        while curr != None:
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
        left = True
        prev = None
        curr = self.__root
        while curr != None:
            curr_key = curr.get_key()
            if item < curr_key:
                prev = curr
                curr = curr.get_left_child()
                left = True
            elif item > curr_key:
                prev = curr
                curr = curr.get_right_child()
                left = False
            else:
                break
            
        if curr == None:
            logger.debug("Item is not found")
            return None
        
        # Process removal
        fix_node = curr
        orig_color = curr.get_color()
        if curr.get_left_child() == None:
            fix_node = curr.get_right_child()
            self.__transplant(curr, curr.get_right_child())
            if fix_node != None:
                prev = fix_node.get_parent()
        elif curr.get_right_child() == None:
            fix_node = curr.get_left_child()
            self.__transplant(curr, curr.get_left_child())
            if fix_node != None:
                prev = fix_node.get_parent()
        else:
            successor = curr.get_right_child().min_node()
            x = successor.get_right_child()
            fix_node = x
            prev = successor
            if successor.get_parent() == curr:
                if x != None:
                    x.set_parent(successor)
            else:
                self.__transplant(successor, x)
                successor.set_right_child(curr.get_right_child())
                if successor.get_right_child() != None:
                    successor.get_right_child().set_parent(successor)
            self.__transplant(curr, successor)
            successor.set_left_child(curr.get_left_child())
            successor.get_left_child().set_parent(successor)
            successor.set_color(curr.get_color())
            if fix_node != None:
                prev = fix_node.get_parent()
            orig_color = successor.get_color()

        # Fix the tree
        if orig_color == "black":
            self.__remove_fixup(fix_node, prev, left)
        curr.set_parent(None)
        curr.set_left_child(None)
        curr.set_right_child(None)
        logger.debug("Target node is removed")
        return curr

        
