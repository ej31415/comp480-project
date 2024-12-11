# COMP480 Project - Benchmark Structures to Optimize User-Data Storage System
*(under construction)*

### Required Packages
- glob2
- numpy
- pandas
- pympler

Implement and benchmark probabilistic querying with the following implementations:

### Bloom Filters
- Naive bloom filter: bit array of size n, with k hash functions; every hashed slot flips the value from 0 to 1
- Counting bloom filter: counter array of size n, with k hash functions: every hashed slots increase or decrease by counts until 0
- Trie-based bloom filter: *TODO: add description*

### Cuckoo Filter
*TODO: add description*

### Consistent Hashing
- Naive binary search tree
- Roughly balanced binary search tree: red-black tree


## Benchmarking

Our metrics for evaluating the performance of the above structures will use:
- time requirement
- space requirement
- false positive rate -- specifically for filters

The same operations will be run with a hash map as a baseline, control group test.
