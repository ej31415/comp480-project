# Data storage system
import sys

class System:

    def __init__(self, username_storage, data_storage):
        self.__users = username_storage
        self.__data = data_storage
    
    def add_user(self, name)->bool:
        success = self.__users.insert(name)
        if not success: # TODO split for logging messages later
            return False
        return True
    
    def add_item(self, item)->bool:
        success = self.__data.insert(item)
        if not success: # TODO split for logging messages later
            return False
        return True
    
    def get_item(self, item)->bool:
        success = self.__data.query(item) == 1
        if not success: # TODO split for logging messages later
            return False
        return True
    
    def remove_item(self, item):
        removed_item = self.__data.remove(item)
        if removed_item == None: # TODO split for logging messages later
            return False
        return True
    
    def size(self):
        return sys.getsizeof(self) + self.__users.size() + self.__data.size()