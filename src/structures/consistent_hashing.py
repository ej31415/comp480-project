import pandas as pd
from bst import BST
from rb_tree import RBTree

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

        def __init__(self, id):
            '''Initialized to be online, with an assigned hash value.'''
            self.__id = id
            self.__data = set() # just throwing everything in a set for now
            self.__online = True

        def __eq__(self, other):
            '''Override equality check to implement hashing.'''
            if type(other) != type(self):
                return False
            return self.__id == other.__id and self.__online == other.__online
        
        def __hash__(self):
            '''Override hashing.'''
            return hash(self.__id)

        def get_id(self):
            return self.__id
        
        def get_data(self):
            return self.__data
        
        def insert(self, item):
            self.__data.add(item)
        
        def remove(self, item):
            self.__data.remove(item)
        
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
                return hash(item) % ring_size
            return func
    
        self.__hash_function = generate_hash()
        self.__ring = pd.Series([None] * ring_size)
        for i in range(num_servers):
            server = self.ServerMock(i * ring_size / num_servers)
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
    
    def get_ring(self):
        return self.__ring

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
                    return curr.get_key()
                else:                       # Case 2: wrap around
                    return self.min_node(curr).get_key()
            else:                           # Case 3: curr is left child of prev
                return prev.get_key()
        else:                               # linear probing with list
            cnt = 0
            while cnt < self.__ring.size:
                if type(self.__ring[hash]) is self.ServerMock:
                    return hash
                hash = (hash + 1) % self.__ring.size
                cnt += 1
            raise Exception("Overlapping ring space.")

    def insert(self, item)->bool:
        hash = self.__hash_function(item)
        cnt = 0
        while cnt < self.__ring.size:
            if self.__ring[hash] == None:
                self.__ring[hash] = item
                self.__ring[self.__find_server(hash)].insert(item)
                return True
            hash = (hash + 1) % self.__ring.size
            cnt += 1
        return False
    
    def query(self, item)->int:
        hash = self.__hash_function(item)
        cnt = 0
        while cnt < self.__ring.size:
            if self.__ring[hash] == item:
                return 1
            hash = (hash + 1) % self.__ring.size
            cnt += 1
        return 0
    
    def remove(self, item):
        hash = self.__hash_function(item)
        cnt = 0
        while cnt < self.__ring.size:
            if self.__ring[hash] == item:
                self.__ring[hash] = None
                self.__ring[self.__find_server(hash)].remove(item)
                return item
            hash = (hash + 1) % self.__ring.size
            cnt += 1
        return None


def little_test():
    '''
    Sanity check for consistent hashing implementation.
    '''
    ring_size = 10
    servers = 2

    print("Make new Consistent Hashing")
    ch = ConsistentHashing(ring_size=ring_size, num_servers=servers)
    print(f"Internal: {ch.get_ring()}")
    ch.insert(1)
    print(f"Internal: {ch.get_ring()}")
    ch.insert(8)
    print(f"Internal: {ch.get_ring()}")
    ch.insert(3)
    print(f"Internal: {ch.get_ring()}")
    ch.insert(10)
    print(f"Internal: {ch.get_ring()}")
    ch.remove(3)
    print(f"Internal: {ch.get_ring()}")
    ch.remove(1)
    print(f"Internal: {ch.get_ring()}")

# little_test()

