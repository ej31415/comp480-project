import random
from sklearn.utils import murmurhash3_32
import logging
import sys

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
class CuckooFilter:
    def __init__(self, bucket_size=4, num_buckets=1e6//4, fingerprint_size=2, max_evictions=500):
        self.bucket_size = bucket_size
        self.num_buckets = int(num_buckets)  # Ensure num_buckets is an integer
        self.fingerprint_size = fingerprint_size
        self.max_evictions = max_evictions
        self.buckets = [[] for _ in range(self.num_buckets)]
        self.count = 0
        logger.info(f"CuckooFilter initialized with {self.num_buckets} buckets, "
                    f"bucket size {self.bucket_size}, and fingerprint size {self.fingerprint_size} bytes.")
    
    def get_config(self):
        return {
            "bucket_size": self.bucket_size,
            "num_buckets": self.num_buckets,
            "fingerprint_size": self.fingerprint_size,
            "max_evictions": self.max_evictions
        }

    def _hash(self, item):
        """Hash function using MurmurHash3 (32-bit)."""
        res = murmurhash3_32(item, positive=True)
        logger.debug(f"Hashed item {item} with seed to {res}")
        return res

    def _fingerprint(self, item):
        """Generates a fingerprint of the item."""
        item = str(item).encode()  # Ensure the item is bytes
        fp = self._hash(item) & ((1 << (self.fingerprint_size * 8)) - 1)
        byte_fp = fp.to_bytes(self.fingerprint_size, 'little')[:self.fingerprint_size]
        logger.debug(f"Generated fingerprint {byte_fp} for item {item}")
        return byte_fp

    def _bucket_index(self, item, fp=None):
        """Computes the primary bucket index."""
        if fp is None:
            fp = self._fingerprint(item)
        index = self._hash(fp.hex()) % self.num_buckets
        logger.debug(f"Primary bucket index for fingerprint {fp} is {index}")
        return index

    def _alternate_index(self, index, fp):
        """Calculates the alternate index."""
        alt_index = (index ^ self._hash(fp.hex())) % self.num_buckets
        logger.debug(f"Alternate index for fingerprint {fp} and index {index} is {alt_index}")
        return alt_index

    def insert(self, item):
        """Inserts an item into the filter."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        if len(self.buckets[index1]) < self.bucket_size:
            self.buckets[index1].append(fp)
            self.count += 1
            logger.debug(f"Item {item} inserted into bucket {index1}")
            return True
        if len(self.buckets[index2]) < self.bucket_size:
            self.buckets[index2].append(fp)
            self.count += 1
            logger.debug(f"Item {item} inserted into bucket {index2}")
            return True

        # Handle evictions
        index = random.choice([index1, index2])
        for evict_count in range(self.max_evictions):
            evicted_fp = random.choice(self.buckets[index])
            self.buckets[index].remove(evicted_fp)
            self.buckets[index].append(fp)

            fp = evicted_fp
            index = self._alternate_index(index, fp)

            if len(self.buckets[index]) < self.bucket_size:
                self.buckets[index].append(fp)
                self.count += 1
                logger.debug(f"Item {item} inserted after {evict_count + 1} evictions")
                return True

        logger.warning(f"Item {item} failed to insert after {self.max_evictions} evictions")
        return False

    def query(self, item):
        """Checks if an item might be in the filter."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        found = fp in self.buckets[index1] or fp in self.buckets[index2]
        logger.debug(
        f"Query for {item}: {'Found' if found else 'Not found'} "
        f"(Bucket1: {index1}, Present: {fp in self.buckets[index1]}), "
        f"(Bucket2: {index2}, Present: {fp in self.buckets[index2]})"
    )
        return int(found)

    def remove(self, item):
        """Deletes an item from the filter, if it exists."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        removed = False
        if fp in self.buckets[index1]:
            self.buckets[index1].remove(fp)
            removed = True
            logger.debug(f"Item {item} removed from bucket 1: {index1}")
        if fp in self.buckets[index2]:
            self.buckets[index2].remove(fp)
            removed = True
            logger.debug(f"Item {item} removed from bucket 2: {index2}")
        
        if not removed:
            logger.error(f"Item {item} not found for removal")
        return removed
    
    # def size(self):
    #     """Gets the memory size of the counting bloom filter."""
    #     logger.debug("Getting CountingBloomFilter size")
    #     return (
    #         sys.getsizeof(self) + # Size of the object itself
    #         sys.getsizeof(self.buckets) + # Size of the bucket list
    #         self.num_buckets * sys.getsizeof([]) + # Per-bucket overhead
    #         self.count * self.fingerprint_size # Size of all fingerprints
    #     )


# Example usage
if __name__ == "__main__":
    cf = CuckooFilter(bucket_size=4, num_buckets=100, fingerprint_size=16, max_evictions=500)
    
    # Insert items
    print(cf.insert("apple"))  # Should return True
    print(cf.insert("banana"))  # Should return True
    print(cf.insert("cherry"))  # Should return True
    
    # Look up items
    print(cf.query("apple"))   # Should return 1
    print(cf.query("banana"))  # Should return 1
    print(cf.query("grape"))   # Should return 0 (if not inserted)
    
    # Delete items
    print(cf.remove("banana"))  # Should return True
    print(cf.query("banana"))  # Should return 0 after deletion
