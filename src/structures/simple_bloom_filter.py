import logging
import math
import numpy as np
import sys

from bitarray import bitarray
from sklearn.utils import murmurhash3_32

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class BloomFilterSimple:
    """
    Bloom_Filter_Simple implements a simple bloom filter using a bitarray of size n and k hash functions.
    By default, the false positive rate is set to 0.01, and the expected number of keys is set to 1 million.
    """

    def __init__(self, false_positive_rate=0.01, key_num=1e6):
        '''Initialize a simple bloom filter, with false positive rate set to 0.01 and expected number of keys set to 1 million.'''
        self.__false_positive_rate = false_positive_rate
        self.__key_num = key_num
        self.__generate_bit_array()
        self.__generate_hash_functions()
        logger.info("Initialized a simple bloom filter...")

    def __generate_bit_array(self):
        '''Generates the bit array for the bloom filter during initialization.'''
        # round up for bit array length to favor lower false positive rate
        num_bits = math.ceil(self.__key_num * np.log(self.__false_positive_rate) / np.log(0.618))
        self.__bit_array = bitarray(num_bits)
        logger.debug("Generated an array of size %d", len(self.__bit_array))
    
    def __generate_hash_functions(self):
        '''Generates a set of hash functions for the bloom filter.'''
        
        def hash_function_generator(size: int, limit: int)->list:
            """
            A function that generates a list of size hash functions.
            The hash functions will generate any integer value in range (0, limit).

            Returns a list of hash functions.
            """
            hash_functions = []

            def hash_function(seed=1):
                """Hash function wrapper to set the seed.

                Returns a hash function with the specified seed.
                """
                def f(val)->int:
                    """Wrapper for murmurhash3_32.

                    Returns the hashed value.
                    """
                    return murmurhash3_32(val, seed, positive=True) % limit
                return f
            
            for i in range(size):
                hash_functions.append(hash_function(i))
            return hash_functions
        
        # Round up number of bits and round down the number of hashes to decrease false positive rate.
        num_bits = math.ceil(self.__key_num * np.log(self.__false_positive_rate) / np.log(0.618))
        num_hashes = math.floor(num_bits / self.__key_num * np.log(2))
        self.__hash_functions = hash_function_generator(num_hashes, num_bits)
        logger.debug("Generated and stored %d hash functions", len(self.__hash_functions))

    def insert(self, item)->bool:
        """Inserts a given item to the bloom filter. Performed by flipping all the hasheds lots in the underlying bit array to 1.

        Returns a boolean representing successful insertion.
        An insertion is unsuccessful if the bloom filter thinks that this item has alread been inserted.
        """
        available = False
        for hash_function in self.__hash_functions:
            hashed_key = hash_function(item)
            if self.__bit_array[hashed_key] == 0: # if any hashed bit is 0, we know this item has not yet been inserted
                available = True
            self.__bit_array[hashed_key] = 1
        logger.debug("Inserted item")
        return available
    
    def query(self, item)->int:
        """Checks the bloom filter for a given item's existence.
        
        Returns 1 if exists, 0 otherwise.
        """
        for hash_function in self.__hash_functions:
            hashed_key = hash_function(item)
            if self.__bit_array[hashed_key] == 0:
                logger.debug("Item is not found")
                return 0
        logger.debug("Item is found")
        return 1
    
    def size(self)->int:
        """Gets the size of the bloom filter. 
        Memory usage involves: self, bit array, hash functions, number of keys, false positive rate.
        
        Returns the size value.
        """
        logger.debug("Getting BloomFilterSimple size")
        return sys.getsizeof(self) + sys.getsizeof(self.__bit_array) + sys.getsizeof(self.__hash_functions) + self.__key_num + self.__false_positive_rate
