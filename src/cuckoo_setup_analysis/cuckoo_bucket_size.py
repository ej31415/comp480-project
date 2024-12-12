import random
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pympler import asizeof
from structures.cuckoo_filter import CuckooFilter

# Constants
FINGERPRINT_SIZE = 4
TEST_SPLIT = 0.2
LOAD_FACTOR = 0.9  # Fixed load factor
BUCKET_SIZES = [i for i in range(2,7)] 

# Initialize an empty list to store the results
results = []

# Helper function to query items from the filter and calculate false positive rate
def query_filter_false_positive(filter_obj, test):
    start = time.time()
    false_positives = 0
    
    # Query items from the filter
    for name in test:
        if filter_obj.query(name):
            false_positives += 1
    duration = time.time() - start
    # Calculate the false positive rate
    false_positive_rate = false_positives / len(test)
    return false_positive_rate, duration

# Experiment: False Positive and Memory Tradeoff for Cuckoo Filter with Fingerprint Size
def experiment_false_positive_memory(names):
    # Generate a random dataset for insertion and query
    data = random.sample(list(names), int ((1-TEST_SPLIT) * len(names)) )#insert data
    test = [name for name in names if name not in data] # not inserted data for false positive rate
    print(f"Data size: {len(data)}, Test size: {len(test)}")

    size = len(data)

    for bucket_size in BUCKET_SIZES:
        num_buckets = int(size / (LOAD_FACTOR * bucket_size))

        cuckoo = CuckooFilter(num_buckets=num_buckets, bucket_size=bucket_size, fingerprint_size=FINGERPRINT_SIZE)

        # Insert items into the cuckoo filter
        start = time.time()
        failed_inserts = 0
        for name in data:
            if not cuckoo.insert(name):
                failed_inserts += 1
        insertion_duration = time.time() - start

        # Query a separate set of not inserted items to calculate false positive rate        
        false_positive_rate, query_duration = query_filter_false_positive(cuckoo, test)

        # Store results
        results.append({
            "Bucket Size": bucket_size,
            # "Failed Inserts": failed_inserts,
            "Insertion Success Rate": 1 - (failed_inserts / len(data)),
            "Insertion Time (seconds)": insertion_duration,
            "Query Time (seconds)": query_duration,
            "False Positive Rate": false_positive_rate,
            "Memory Usage (bytes)": asizeof.asizeof(cuckoo)
        })

        

# Main script
if __name__ == "__main__":
    # Sample dataset
    main_dataframe = pd.DataFrame()
    data_files = glob.glob("data/names/*.txt") # run script from comp480-project/ directory
    data_list = []
    for file in data_files:
        sub_data = pd.read_csv(file, sep=',', names=["Name", "Sex", "Frequency"])
        data_list.append(sub_data)
    main_dataframe = pd.concat(data_list, axis=0)
    names = main_dataframe.iloc[:, 0]
    print(f"There are {len(names)} names.")
    names = names.unique()
    print(f"There are {len(names)} unique names.")
    
    # Run experiment
    experiment_false_positive_memory(names)

    # Print the appended result in a readable format
    print("Result for current configuration:")
    for i in range(len(results)):
        for key, value in results[i].items():
            print(f"{key}: {value}")
        print("-" * 50)  # Separator for better readability

    # Convert results into a DataFrame for easier analysis
    results_df = pd.DataFrame(results)

    
    # Create subplots (2 rows, 2 columns)
    fig, axs = plt.subplots(2, 2, figsize=(18, 10))
    
    # Plot 1: Insertion Success Rate vs Bucket Size
    axs[0, 0].plot(results_df["Bucket Size"], results_df["Insertion Success Rate"], marker='o', color='r', label='Insertion Success Rate')
    axs[0, 0].set_title('Insertion Success Rate vs Bucket Size')
    axs[0, 0].set_xlabel('Bucket Size')
    axs[0, 0].set_ylabel('Insertion Success Rate')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Plot 2 : Insertion Time vs Bucket Size
    axs[0, 1].plot(results_df["Bucket Size"], results_df["Insertion Time (seconds)"], marker='o', color='b', label='Insertion Time')
    axs[0, 1].set_title('Insertion Time vs Bucket Size')
    axs[0, 1].set_xlabel('Bucket Size')
    axs[0, 1].set_ylabel('Insertion Time (seconds)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Plot 3: Query Time vs Bucket Size
    axs[1, 0].plot(results_df["Bucket Size"], results_df["Query Time (seconds)"], marker='o', color='g', label='Query Time')
    axs[1, 0].set_title('Query Time vs Bucket Size')
    axs[1, 0].set_xlabel('Bucket Size')
    axs[1, 0].set_ylabel('Query Time (seconds)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Plot 4: Memory Usage (bytes) vs Bucket Size
    axs[1, 1].plot(results_df["Bucket Size"], results_df["Memory Usage (bytes)"], marker='o', color='y', label='Memory Usage')
    axs[1, 1].set_title('Memory Usage vs Bucket Size')
    axs[1, 1].set_xlabel('Bucket Size')
    axs[1, 1].set_ylabel('Memory Usage (bytes)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Adjust layout to avoid overlap
    plt.tight_layout()
    plt.show()
