# Work Notes

## Repo Structure
- code is in src/

### src/structures
- all the structures that we will be using (bloom filters, consistent hashing, etc.) will be in src/structures
    - for each, implement at least the following functions:
    ```
    def insert(self, item)->bool:
        # adds item into self
        # returns success/failure? can decide later
    
    def query(self, item)->int:
        # gets the count of item stored in self
        # returns the count
    
    def size(self):
        # gets the size of this structure
        # make sure to add the space occupied by the private members
        # returns the number of bytes
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

### tests
- all tests will be in this folder
- you might need to add ```sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "../../src")``` before importing from ```src/structures``` because Python is a bit silly
- runtests.bat (Windows) and runtests.sh(Linux/Unix/macOS) will run all the tests and show coverage details
    - not too sure if runtests.sh will work with mac to be honest; never worked with macOS
- test a single unittest: ```python -m unittest test_package.test_module.TestClass.test_method -v```

## Report
- mention that bloom filter false positive can be annoying to users if they get a message that their item to insert fails but their query for item shows that item has not yet been added (for example, try accessing corresponding item element but fails because it is only a bloom filter false positive)