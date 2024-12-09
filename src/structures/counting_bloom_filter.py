import logging
import math
import numpy as np
import sys

from sklearn.utils import murmurhash3_32

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class CountingBloomFilter:
    """
    CountingBloomFilter implements a counting bloom filter using an integer counter array of size n 
    and k hash functions. This allows insertions and deletions with a controlled false positive rate.
    """

    def __init__(self, false_positive_rate=0.01, key_num=1e6):
        '''Initialize a counting bloom filter with a false positive rate and expected number of keys.'''
        self.__false_positive_rate = false_positive_rate
        self.__key_num = key_num
        self.__generate_counter_array()
        self.__generate_hash_functions()

    def __generate_counter_array(self):
        '''Generates the counter array for the counting bloom filter.'''
        # Calculate the required number of counters to meet the desired false positive rate
        num_counters = math.ceil(self.__key_num * np.log(self.__false_positive_rate) / np.log(0.618))
        self.__counter_array = np.zeros(num_counters, dtype=int)  # Use integer counters instead of bitarray (64 bits per counter for 64 bit systems)
        logger.info("Generated an array of %d counters", len(self.__counter_array))

    def __generate_hash_functions(self):
        '''Generates a set of hash functions for the counting bloom filter.'''
        
        def hash_function_generator(size: int, limit: int) -> list:
            """Generates a list of hash functions that return values within the counter array range."""
            hash_functions = []

            def hash_function(seed=1):
                """Creates a hash function with the specified seed."""
                def f(val) -> int:
                    """Hashes the input and returns an index within the counter array range."""
                    return murmurhash3_32(val, seed, positive=True) % limit
                return f
            
            for i in range(size):
                hash_functions.append(hash_function(i))
            return hash_functions

        # Calculate the number of hash functions
        num_counters = len(self.__counter_array)
        num_hashes = math.floor(num_counters / self.__key_num * np.log(2))
        self.__hash_functions = hash_function_generator(num_hashes, num_counters)
        logger.info("Generated %d hash functions", len(self.__hash_functions))

    def insert(self, item) -> bool:
        """Inserts an item into the counting bloom filter by incrementing the relevant counters."""
        for hash_function in self.__hash_functions:
            index = hash_function(item)
            self.__counter_array[index] += 1
        logger.debug("Inserted item")
        return True

    def remove(self, item) -> bool:
        """Removes an item from the counting bloom filter by decrementing the relevant counters."""
        for hash_function in self.__hash_functions:
            index = hash_function(item)
            if self.__counter_array[index] > 0:
                self.__counter_array[index] -= 1
        logger.debug("Removed item")
        return True

    def query(self, item) -> int:
        """Checks if an item is possibly in the set by verifying if all relevant counters are non-zero."""
        logger.debug("Querying item")
        for hash_function in self.__hash_functions:
            index = hash_function(item)
            if self.__counter_array[index] == 0:
                return 0  # Item is not in the set
        return 1  # Item is possibly in the set

    def size(self) -> int:
        """Gets the memory size of the counting bloom filter."""
        logger.debug("Getting CountingBloomFilter size")
        return (
            sys.getsizeof(self) +
            sys.getsizeof(self.__counter_array) +
            sys.getsizeof(self.__hash_functions) +
            sys.getsizeof(self.__key_num) +
            sys.getsizeof(self.__false_positive_rate)
        )
    
    def min_count(self, item) -> int:
        """Gets the minimum value stored corresponding to an item."""
        logger.debug("Getting min count")
        cnts = np.array([])
        for hash_function in self.__hash_functions:
            index = hash_function(item)
            cnts = np.append(cnts, self.__counter_array[index])
        return min(cnts)

# if __name__ == "__main__":
#     cbf = CountingBloomFilter(false_positive_rate=0.01, key_num=1e6)
#     cbf.insert("apple")
#     print(cbf.query("apple"))  # Should print 1 (exists)
#     cbf.remove("apple")
#     print(cbf.query("apple"))  # Should print 0 (no longer exists)
