import pandas as pd

from sklearn.utils import murmurhash3_32

from structures.bst import BST
from structures.rb_tree import RBTree

class ConsistentHashing:
    """
    ConsistentHashing is a structure that seeks to implement the consistent hashing technique, used for data storage
    in distributed systems.
    The underlying tree can be customized to any structure as long as it supports the necessary functions.
    """

    class ServerMock():
        """
        ServerMock mimics the behavior of a server.
        Id is the hash value assigned to this server by consistent hashing.
        """

        def __init__(self, id, data=None):
            '''Initialized to be online, with an assigned hash value.'''
            self.__id = id
            self.__data = data
            self.__online = True

        def get_id(self):
            return self.__id
        
        def get_data(self):
            return self.__data
        
        def check_online(self):
            return self.__online

        def simulate_offline(self):
            self.__online = False
        
        def simulate_online(self):
            self.__online = True
        

    def __init__(self, ring_size=1000000, num_servers=10, tree=""):
        '''Initializes a list of mock servers with a hash function.

        Mock servers are placed around the ring evenly.
        '''

        def generate_hash(seed = 0):
            def func(item):
                return murmurhash3_32(item, seed=seed) % ring_size
            return func
    
        self.__hash_function = generate_hash()
        self.__ring = pd.Series([None] * ring_size)
        for i in range(num_servers):
            server = self.ServerMock(i * ring_size / num_servers)
            print(type(server))
            self.__ring[self.__hash_function(server)] = server

        match tree:
            case "":
                self.__server_storage = None
            case "bst":
                self.__server_storage = BST()
            case "rbt":
                self.__server_storage = RBTree()
            case _:
                raise Exception(f"Tree type is invalid.")
    
    def __find_server(self, hash):
        if self.__server_storage != None:   # using a BST or variation to store servers
            curr = self.__server_storage.get_root()
            prev = None
            while curr != self.__server_storage.get_null():
                prev = curr
                if hash < curr.get_key():
                    curr = curr.get_left_child()
                elif hash > curr.get_key():
                    curr = curr.get_right_child()
                else:
                    raise Exception(f"Overlapping ring space.")
                
            if prev == None:
                raise Exception(f"Server storage is empty.")
            
            while prev != None and curr == prev.get_right_child():
                curr = prev
                prev = curr.get_parent()
            
            if prev == None:
                if curr.get_key() > hash:   # Case 1: root is successor
                    return curr
                else:                       # Case 2: wrap around
                    return self.min_node(curr)
            else:                           # Case 3: curr is left child of prev
                return prev
        else:                               # linear probing with list
            for slot in self.__ring:
                if type(slot) is self.ServerMock:
                    return slot
            raise Exception("Overlapping ring space.")

    def insert(self, item)->bool:
        server = self.__hash_function(item)
        success = self.__server_ring[server].insert(item)
        return success
    
    def query(self, item)->int:
        server = self.__hash_function(item)
        result = self.__server_ring[server].search(item)
        return 1 if result != None else 0
    
    def remove(self, item):
        server = self.__hash_function(item)
        removed = self.__server_ring[server].remove(item)
        return removed
