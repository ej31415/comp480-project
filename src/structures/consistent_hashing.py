from sklearn.utils import murmurhash3_32

from structures.bst import BST

class ConsistentHashing:
    """
    ConsistentHashing is a structure that seeks to implement the consistent hashing technique, used for data storage
    in distributed systems.
    The underlying tree can be customized to any structure as long as it supports the necessary functions.
    """

    class ServerMock():
        """
        ServerMock mimics the behavior of a server.
        The underlying fields include a tree for data storage, an inbox, and an outbox.
        The inbox is for receiving any requests from a down server.
        The outbox redirects requests to the next server when this server fails.
        """

        def __init__(self, data=None, inbox=None, outbox=None):
            '''Initialized to be online, with an empty inbox and outbox.'''
            self.__data = data
            self.__inbox = inbox
            self.__outbox = outbox
            self.__online = True
        
        def get_data(self):
            return self.__data
        
        def set_inbox(self, inbox):
            self.__inbox = inbox

        def set_outbox(self, outbox):
            self.__outbox = outbox
        
        def check_online(self):
            return self.__online
        
        def insert(self, item)->bool:
            return self.__data.insert(item)
        
        def remove(self, item):
            return self.__data.remove(item)
        
        def search(self, item):
            if not self.__online:
                return self.__outbox.search(item)
            
            start = self
            server = self
            while server != None:
                data = server.get_data()
                result = data.get(item)
                if result == None:
                    server = server.__inbox
                    if server == start:
                        return None
                else:
                    return result
            return None

        def simulate_offline(self):
            self.__online = False
        
        def simulate_online(self):
            self.__online = True
        

    def __init__(self, num_servers=10):
        '''Initializes a list of mock servers with a hash function.'''
        self.__server_ring = []
        for i in range(num_servers):
            self.__server_ring.append(self.ServerMock(data=BST())) # implement with BSTs
        for i in range(num_servers):
            self.__server_ring[i].set_inbox(self.__server_ring[(i - 1) % num_servers])
            self.__server_ring[i].set_outbox(self.__server_ring[(i + 1) % num_servers])

        def generate_hash(seed=0):
            return lambda item: murmurhash3_32(item, seed=seed) % num_servers
        self.__hash_function = generate_hash()
    
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
