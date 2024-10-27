# Work Notes

## Repo Structure
- code is in src/

### src/structures
- all the structures that we will be using (bloom filters, consistent hashing, etc.) will be in src/structures
    - for each, implement at least the following functions:
    ```
    def Insert(self, item)->bool:
        # adds item into self
        # returns success/failure? can decide later
    
    def Query(self, item)->int:
        # gets the count of item stored in self
        # returns the count
    ```
- the following structures will be implemented:
    - cuckoo filter
    - simple bloom filter
    - counting bloom filter
    - trie-based bloom filter
    - simple BST-backed consistent hashing
    - red-black tree-backed consistent hashing

### runner.py
- the main script that will be run
- should start up a storage_system, using a combination of the structures that we implement
- should also store data into said structures

### storage_system.py
- the storage system that we will be using
- essentially an object that uses defined structures to store data
- should support reading in a file that contains the data that we want to store (for now)
