# Main script
import glob
import pandas as pd

from tqdm import tqdm
import time
import logging
import os
import random
import math
import matplotlib.pyplot as plt
from pympler import asizeof

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def load_names_from_files(path):
    """
    Load names from files in the given path.
    
    path: str, path to the data files
    return: list of unique names
    """
    main_dataframe = pd.DataFrame()
    data_files = glob.glob(path)
    data_list = []
    for file in data_files:
        sub_data = pd.read_csv(file, sep=',', names=["Name", "Sex", "Frequency"])
        data_list.append(sub_data)
    main_dataframe = pd.concat(data_list, axis=0)
    names = main_dataframe.iloc[:, 0]
    print(f"There are {len(names)} names.")
    names = names.unique()
    print(f"There are {len(names)} unique names.")
    return list(names)

def perform_insertion(filter_obj, data):
    failed_inserts = 0
    for name in data:
        if not filter_obj.insert(name):
            failed_inserts += 1
    return failed_inserts

def perform_query_false_positive(filter_obj, not_inserted):
    false_positives = 0
    for name in not_inserted:
        if filter_obj.query(name):
            false_positives += 1
    return false_positives

def perform_removal(filter_obj, data):
    failed_removals = 0
    for name in data:
        if not filter_obj.delete(name):
            failed_removals += 1
    return failed_removals


# Collect results in the format: {"filter": "Cuckoo", "size": ..., "load_factor": ..., "metric": ..., "value": ...}
results = []
from structures.cuckoo_filter import CuckooFilter
from structures.simple_bloom_filter import BloomFilterSimple
from structures.counting_bloom_filter import CountingBloomFilter

TEST_SPLIT = 0.2  # Test split ratio
results = []
load_factors = [0.1, 0.5, 0.9]  # Varying load factors
sub_size_ratios = [0.1, 0.5, 0.9, 1]  # Varying sub-sizes

# Helper function to collect data
def collect_data(filter_name, metric, value, size, load_factor):
    res = {
        "filter": filter_name,
        "size": size,
        "load_factor": load_factor,
        "metric": metric,
        "value": value,
    }
    print(res)
    results.append(res)

# Helper function to plot graphs
def plot_graphs(results):
    metrics = ["insertion_time", "query_time", "false_positive_rate", "memory_usage"]
    filters = set([r["filter"] for r in results])
    sizes = sorted(set([r["size"] for r in results]))
    load_factors = sorted(set([r["load_factor"] for r in results]))
    
    # Plot grouped by filter size
    for metric in metrics:
        plt.figure(figsize=(12, 8))
        for size in sizes:
            subset = [r for r in results if r["size"] == size and r["metric"] == metric]
            for filter_name in filters:
                data = [r for r in subset if r["filter"] == filter_name]
                x = [r["load_factor"] for r in data]
                y = [r["value"] for r in data]
                plt.plot(x, y, marker='o', label=f"{filter_name} (Size={size})")
        plt.title(f"{metric.replace('_', ' ').capitalize()} by Load Factor (Grouped by Size)")
        plt.xlabel("Load Factor")
        plt.ylabel(metric.replace('_', ' ').capitalize())
        plt.legend()
        plt.grid()
        plt.savefig(f"{metric}_by_size.png")
        plt.show()

    # Plot grouped by load factor
    for metric in metrics:
        plt.figure(figsize=(12, 8))
        for load_factor in load_factors:
            subset = [r for r in results if r["load_factor"] == load_factor and r["metric"] == metric]
            for filter_name in filters:
                data = [r for r in subset if r["filter"] == filter_name]
                x = [r["size"] for r in data]
                y = [r["value"] for r in data]
                plt.plot(x, y, marker='o', label=f"{filter_name} (Load Factor={load_factor})")
        plt.title(f"{metric.replace('_', ' ').capitalize()} by Size (Grouped by Load Factor)")
        plt.xlabel("Filter Size")
        plt.ylabel(metric.replace('_', ' ').capitalize())
        plt.legend()
        plt.grid()
        plt.savefig(f"{metric}_by_load_factor.png")
        plt.show()

# Modify `insert_filter` and `query_filter_false_positive` to collect data
def insert_filter(filter_name, filter_obj, data, size, load_factor):
    start = time.time()
    failed_inserts = 0
    for name in data:
        if not filter_obj.insert(name):
            failed_inserts += 1
    duration = time.time() - start
    memory_usage = asizeof.asizeof(filter_obj)
    collect_data(filter_name, "insertion_time", duration, size, load_factor)
    collect_data(filter_name, "memory_usage", memory_usage, size, load_factor)
    return duration, memory_usage

def query_filter_false_positive(filter_name, filter_obj, not_inserted, load_factor):
    start = time.time()
    false_positives = sum(filter_obj.query(name) for name in not_inserted)
    duration = time.time() - start
    false_positive_rate = false_positives / len(not_inserted)
    collect_data(filter_name, "query_time", duration, len(not_inserted), load_factor)
    collect_data(filter_name, "false_positive_rate", false_positive_rate, len(not_inserted), load_factor)
    return false_positive_rate, duration

def run_experiment(names, load_factors, sub_size_ratios):
    for size_ratio in sub_size_ratios:
        print(f"Size ratio out of the whole dataset: {size_ratio}")
        cur_size = int(size_ratio * len(names))
        data = random.sample(list(names), int ((1-TEST_SPLIT) * (cur_size)) )#insert data
        test = [] # not inserted data for false positive rate
        while len(test) < cur_size * TEST_SPLIT:
            name = random.choice(names)
            if name not in data:
                test.append(name)
        print(f"Data size: {len(data)}, Test size: {len(test)}")
        data_size = len(data)
        
        for load_factor in load_factors:
            # Set up Cuckoo Filter parameters
            bucket_size = 6
            fingerprint_size = 6 
            num_buckets = int(data_size / (load_factor * bucket_size))
            #setup filters
            false_positive_rate = 0.05
            bucket_size = 6
            
            # Calculate fingerprint size and number of buckets
            fingerprint_size = 2*8
            num_buckets = int(data_size / (load_factor * bucket_size))

            # Initialize Cuckoo Filter
            cuckoo = CuckooFilter(num_buckets=num_buckets, bucket_size=bucket_size, fingerprint_size=fingerprint_size)
            bf = BloomFilterSimple(false_positive_rate=false_positive_rate, key_num=int(data_size/load_factor))
            cbf = CountingBloomFilter(false_positive_rate=false_positive_rate, key_num=int(data_size/load_factor))

            #######
            # insert into filters
            #######
            insert_filter("Cuckoo", cuckoo, data, data_size, load_factor)
            insert_filter("Bloom", bf, data, data_size, load_factor)
            insert_filter("Counting Bloom", cbf, data, data_size, load_factor)

            #######
            # query filters
            #######

            query_filter_false_positive("Cuckoo", cuckoo, test, load_factor)
            query_filter_false_positive("Bloom", bf, test, load_factor)
            query_filter_false_positive("Counting Bloom", cbf, test, load_factor)

# Run experiments and plot graphs
run_experiment(load_names_from_files("data/names/*.txt"), load_factors, sub_size_ratios)
plot_graphs(results)


            

    
    








  
