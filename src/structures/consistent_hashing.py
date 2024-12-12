import logging
import pandas as pd
import sys

from sklearn.utils import murmurhash3_32
from structures.bst import BST
from structures.rb_tree import RBTree

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
            if not isinstance(other, ConsistentHashing.ServerMock):
                return False
            return self.__id == other.__id and self.__online == other.__online
        
        def __hash__(self):
            '''Override hashing.'''
            return murmurhash3_32(self.__id)
        
        def get_id(self):
            return self.__id
        
        def get_data(self):
            return self.__data
        
        def insert(self, item):
            self.__data.add(item)
        
        def remove(self, item):
            self.__data.remove(item)
        
        # def size(self):
        #     def recursive_sizeof(item):
        #         size = sys.getsizeof(item)
        #         if isinstance(item, (list, tuple, set)):
        #             for i in item:
        #                 size += recursive_sizeof(i)
        #         return size
        #     return sys.getsizeof(self.__id) + recursive_sizeof(self.__data) + sys.getsizeof(self.__online)
        
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
                return int(hash(item) % ring_size)
            return func
    
        self.__hash_function = generate_hash()
        self.__ring = pd.Series([None] * ring_size)
        self.__servers = {}

        match tree:
            case "":
                self.__server_storage = None
            case "bst":
                self.__server_storage = BST()
            case "rbt":
                self.__server_storage = RBTree()
            case _:
                raise Exception(f"Tree type is invalid.")

        for i in range(num_servers):
            server = self.ServerMock(int(i * ring_size / num_servers))
            position = self.__hash_function(server)
            self.__ring[position] = server
            self.__servers[i] = position
            if self.__server_storage != None:
                self.__server_storage.insert(position, value=server)
        
        logger.debug(f"Initialized consistent hashing with size {ring_size} and {num_servers} servers and storage with {tree if tree != '' else 'nothing'}")

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
                    return self.__server_storage.min_node(curr).get_key()
            else:                           # Case 3: curr is left child of prev
                return prev.get_key()
        else:                               # linear probing with list
            cnt = 0
            while cnt < self.__ring.size:
                if type(self.__ring[hash]) is self.ServerMock and self.__ring[hash].check_online():
                    return hash
                hash = (hash + 1) % self.__ring.size
                cnt += 1
            raise Exception("Overlapping ring space.")
        
    def __find_next_server_index(self, position) -> int:
        check_pos = (position + 1) % self.__ring.size
        while check_pos != position:
            if (type(self.__ring[check_pos]) == self.ServerMock and self.__ring[check_pos].check_online()):
                return check_pos
            check_pos = (check_pos + 1) % self.__ring.size
        return -1
    
    def get_ring(self):
        return self.__ring
    
    def get_server_sizes(self):
        lengths = []
        for k in self.__servers.keys():
            lengths.append(len(self.__ring[self.__servers[k]].get_data()))
        return lengths
    
    def find(self, item)->int:
        hash = self.__hash_function(item)
        cnt = 0
        while cnt < self.__ring.size:
            if self.__ring[hash] == item:
                return hash
            hash = (hash + 1) % self.__ring.size
            cnt += 1
        return -1

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
    
    # def size(self)->int:
    #     def recursive_sizeof(item):
    #         size = sys.getsizeof(item)
    #         if isinstance(item, (list, tuple, set)):
    #             for i in item:
    #                 size += recursive_sizeof(i)
    #         if isinstance(item, dict):
    #             for k in item.keys():
    #                 size += recursive_sizeof(k)
    #                 size += recursive_sizeof(item[k])
    #         if isinstance(item, self.ServerMock):
    #             size += item.size()
    #         if isinstance(item, pd.Series):
    #             for _, i in item.items():
    #                 size += recursive_sizeof(i)
    #         return size
    #     return sys.getsizeof(self) + sys.getsizeof(self.__hash_function) + recursive_sizeof(self.__ring) + recursive_sizeof(self.__servers) +  0 if self.__server_storage == None else self.__server_storage.size()
    
    def simulate_offline(self, id):
        '''Downs the server with the given `id`.'''
        position = self.__servers[id]
        if position == None:
            raise Exception("Given server position is out of range!")
        
        server = self.__ring[position]
        if not server.check_online():
            logger.warning("The specified server is already down.")
            return
        server_next = None
        
        # Find the next server
        if self.__server_storage == None:
            check_pos = self.__find_next_server_index(position)
            if check_pos == -1:
                raise Exception("Next server not found.")
            server_next = self.__ring[check_pos]
        else:
            node = self.__server_storage.get(position)
            succ = self.__server_storage.successor(node)
            if succ == None:
                succ = self.__server_storage.min_node(self.__server_storage.get_root())
            if node == succ:
                raise Exception("No available server!")
            server_next = self.__ring[succ.get_key()]
            self.__server_storage.remove(position)
        
        for item in server.get_data().copy():
            server.remove(item)
            server_next.insert(item)
        
        server.simulate_offline()

        logger.info(f"Server {id} is offline={not server.check_online()}")
    
    def simulate_online(self, id):
        '''Bring a server back online.'''
        position = self.__servers[id]
        if position == None:
            raise Exception("Given server position is out of range!")
        
        server = self.__ring[position]
        if not type(server) is self.ServerMock:
            raise Exception("Server position has been replaced.")
        if server.check_online():
            logger.warning("The specified server is already online.")
            return
        server_next = None
        server_next_idx = -1
        
        if self.__server_storage == None:
            check_pos = self.__find_next_server_index(position)
            if check_pos == -1:
                raise Exception("Next server not found.")
            server_next = self.__ring[check_pos]
            server_next_idx = check_pos
        else:
            self.__server_storage.insert(position, value=server)
            node = self.__server_storage.get(position)
            succ = self.__server_storage.successor(node)
            if succ == None:
                succ = self.__server_storage.min_node(self.__server_storage.get_root())
            if node == succ:
                raise Exception("No available server!")
            server_next = self.__ring[succ.get_key()]
        
        for item in server_next.get_data().copy():
            idx = self.find(item)
            if position < server_next_idx and not (idx > position and idx < server_next_idx):
                server_next.remove(item)
                server.insert(item)
            elif position > server_next_idx and not (idx > position or idx < server_next_idx):
                server_next.remove(item)
                server.insert(item)
        
        server.simulate_online()

        logger.info(f"Server {id} is online={server.check_online()}")



def little_test():
    '''
    Sanity check for consistent hashing implementation.
    '''
    ring_size = 10
    servers = 2

    print("Make new Consistent Hashing")
    ch = ConsistentHashing(ring_size=ring_size, num_servers=servers)
    ch.insert(1)
    ch.insert(8)
    ch.insert(3)
    ch.insert(10)
    print(f"Internal: {ch.get_ring()}")
    print(ch.get_server_sizes())
    ch.simulate_offline(1)
    print(ch.get_server_sizes())
    ch.remove(3)
    ch.remove(1)
    print(ch.get_server_sizes())
    ch.simulate_online(1)
    print(ch.get_server_sizes())

# little_test()