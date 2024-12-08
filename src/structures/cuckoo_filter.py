import random
from sklearn.utils import murmurhash3_32
import logging
import sys

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class CuckooFilter:
    def __init__(self, bucket_size=4, num_buckets=1e6//4, fingerprint_size=8, max_evictions=500):
        """
        Initializes a Cuckoo Filter.
        
        :param bucket_size: Number of slots in each bucket.
        :param num_buckets: Total number of buckets.
        :param fingerprint_size: Size of each fingerprint in bits.
        :param max_evictions: Maximum number of evictions before insertion fails.
        """
        self.bucket_size = bucket_size
        self.num_buckets = num_buckets
        self.fingerprint_size = fingerprint_size // 8  # Convert bits to bytes
        self.max_evictions = max_evictions
        self.buckets = [[] for _ in range(int(num_buckets))]
        self.count = 0

    def _hash(self, item, seed=0):
        """Hash function using MurmurHash3 (32-bit)."""
        return murmurhash3_32(item, seed=seed, positive=True)
    
    def _fingerprint(self, item):
        """Generates a fingerprint of the item, using only the required bits."""
        fp = self._hash(item)& ((1 << (self.fingerprint_size * 8)) - 1)
        return fp.to_bytes(self.fingerprint_size, 'little')[:self.fingerprint_size]

    def _bucket_index(self, item, fp=None) -> int:
        """Computes the primary bucket index for an item or fingerprint."""
        if fp is None:
            fp = self._fingerprint(item)
        return int(self._hash(fp.hex()) % self.num_buckets)

    def _alternate_index(self, index, fp) -> int:
        """Calculates the alternate index using the fingerprint and initial bucket index."""
        return int((index ^ self._hash(fp.hex())) % self.num_buckets)

    def insert(self, item):
        """Inserts an item into the filter."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        # Attempt to insert into either bucket
        if len(self.buckets[index1]) < self.bucket_size:
            self.buckets[index1].append(fp)
            self.count += 1
            return True
        if len(self.buckets[index2]) < self.bucket_size:
            self.buckets[index2].append(fp)
            self.count += 1
            return True

        # Handle evictions if both buckets are full
        index = random.choice([index1, index2])
        for _ in range(self.max_evictions):
            # Evict a random fingerprint from the chosen bucket
            evicted_fp = random.choice(self.buckets[index])
            self.buckets[index].remove(evicted_fp)
            self.buckets[index].append(fp)

            # Update fp and index for the evicted fingerprint
            fp = evicted_fp
            index = self._alternate_index(index, fp)

            # Insert the new fingerprint if there's space
            if len(self.buckets[index]) < self.bucket_size:
                self.buckets[index].append(fp)
                self.count += 1
                return True
        
        # Insertion failed due to too many evictions
        return False

    def query(self, item):
        """Checks if an item might be in the filter."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        # Check both buckets for the fingerprint
        return int(fp in self.buckets[index1] or fp in self.buckets[index2])

    def remove(self, item):
        """Deletes an item from the filter, if it exists."""
        fp = self._fingerprint(item)
        index1 = self._bucket_index(item)
        index2 = self._alternate_index(index1, fp)

        # Remove the fingerprint from either bucket if found
        if fp in self.buckets[index1]:
            self.buckets[index1].remove(fp)
            self.count -= 1
            return True
        if fp in self.buckets[index2]:
            self.buckets[index2].remove(fp)
            self.count -= 1
            return True
        return False
    
    def size(self):
        """Gets the memory size of the counting bloom filter."""
        logger.debug("Getting CountingBloomFilter size")
        return (
            sys.getsizeof(self) + # Size of the object itself
            sys.getsizeof(self.buckets) + # Size of the bucket list
            self.num_buckets * sys.getsizeof([]) + # Per-bucket overhead
            self.count * self.fingerprint_size # Size of all fingerprints
        )


# Example usage
if __name__ == "__main__":
    cf = CuckooFilter(bucket_size=4, num_buckets=100, fingerprint_size=8, max_evictions=500)
    
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
