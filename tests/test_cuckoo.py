import numpy as np
import unittest
import os
import sys
import logging

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.append(src_path)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
# Now import the desired module
from structures.cuckoo_filter import CuckooFilter

class TestCuckoo(unittest.TestCase):

    def setUp(self):
        self.filter = CuckooFilter()

    def test_insert_one(self):
        '''Test inserting a number'''
        self.filter.insert(2)
        self.assertEqual(1, self.filter.query(2))
        logger.info("Test insert one passed")
    
    def test_insert_multi(self):
        '''Test multiple insertions'''
        np.random.seed(123)
        insert_values = [str(val).encode() for val in np.random.choice(range(1, 1000000), size=100000)]# 10% of the range
        for val in insert_values:
            self.filter.insert(val)
        for val in insert_values:
            self.assertEqual(1, self.filter.query(val))
        logger.info("Test insert multi passed")
    
    # def test_remove_one(self):
    #     '''Test removing a number'''
    #     target = 2
    #     self.filter.insert(target)
    #     self.filter.remove(target)
    #     self.assertEqual(0, self.filter.query(target))
    #     logger.info("Test remove one passed")

    # def test_remove_n(self):
    #     '''Test removing n numbers'''
        
    #     np.random.seed(123)
    #     insert_values = str(np.random.choice(range(1, 1000000), size=900000)).encode()
    #     for i in range(len(insert_values)):
    #         success = True
    #         logger.info(f"Testing removing {i} numbers")
    #         for val in insert_values[:i]:
    #             self.filter.insert(val)
    #         for val in insert_values[:i]:
    #             self.filter.remove(val)
    #             cur = self.assertEqual(0, self.filter.query(val))
    #             success = success and cur
    #         if success:
    #             logger.info(f"Successfully removed {i} numbers")
    #         else:
    #             logger.error(f"Failed to remove {i} numbers")
        
        
    
    # def test_remove_multi(self):
    #     '''Test removing multiple numbers'''
    #     np.random.seed(0)
    #     false_positives = 0
    #     success_removes = 0
    #     failed_removes = 0

    #     insert_values = [str(val).encode() for val in np.random.choice(range(1, 1000000), size=100000)]
    #     for val in insert_values:
    #         self.filter.insert(val)
    #     for idx in range(len(insert_values)):
    #         val = insert_values[idx]
    #         if self.filter.remove(val) == True:
    #             logger.debug(f"Successfully removed value {val}")
    #             success_removes += 1
    #         else:
    #             logger.error(f"Failed to remove value {val}")
    #             failed_removes += 1

    #         if self.filter.query(val) == 0:
    #             logger.debug(f"Filter Prediction for {val} removed works")
    #         else:
    #             false_positives += 1
    #     logger.info(f"Total inserts: {len(insert_values)}")

    #     logger.info(f"Successful removes: {success_removes}")
    #     logger.info(f"Failed removes: {failed_removes}")

    #     logger.info(f"False positives: {false_positives}")
    #     logger.info(f"False positives rate: {false_positives/len(insert_values)}")

    #     logger.info(f"Filter configuration: {self.filter.get_config()}")
    #     logger.info(f"remove multi test done")
