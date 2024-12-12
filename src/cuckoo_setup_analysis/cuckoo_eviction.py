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
LOAD_FACTOR = 0.9
BUCKET_SIZE = 6
EVICT_LIMITS = [i for i in range(200, 2000, 100)]  # Test different eviction limits

# Initialize an empty list to store the results
results = []

def experiment_time_insertion(names):
    # Generate a random dataset for insertion and query
    data = names
    size = len(data)
    num_buckets = int(size / (LOAD_FACTOR * BUCKET_SIZE))

    for max_eviction in EVICT_LIMITS:
        cuckoo = CuckooFilter(num_buckets=num_buckets, bucket_size=BUCKET_SIZE, 
                                fingerprint_size=FINGERPRINT_SIZE, max_evictions=max_eviction)

        start = time.time()
        failed_inserts = 0
        for name in data:
            if not cuckoo.insert(name):
                failed_inserts += 1
        duration = time.time() - start

        results.append({
            "Max Evictions": max_eviction,
            "Failed Inserts": failed_inserts,
            "Duration (seconds)": duration
        })

# Main script
if __name__ == "__main__":
    # Sample dataset
    main_dataframe = pd.DataFrame()
    data_files = glob.glob("data/names/*.txt")
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
    experiment_time_insertion(names)

    # Print the appended result in a readable format
    print("Result for current configuration:")
    for i in range(len(results)):
        for key, value in results[i].items():
            print(f"{key}: {value}")
        print("-" * 50)  # Separator for better readability

    # Convert results into a DataFrame for easier analysis
    results_df = pd.DataFrame(results)

    # Create the subplots for the two graphs
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    # Graph 1: Failed Inserts vs Max Evictions
    axs[0].plot(results_df["Max Evictions"], results_df["Failed Inserts"], marker='o', color='blue', label='Failed Inserts')
    axs[0].set_title("Failed Inserts vs Max Evictions")
    axs[0].set_xlabel("Max Evictions")
    axs[0].set_ylabel("Failed Inserts")
    axs[0].grid(True)
    axs[0].legend()

    # Graph 2: Duration (seconds) vs Max Evictions
    axs[1].plot(results_df["Max Evictions"], results_df["Duration (seconds)"], marker='o', color='red', label='Duration (seconds)')
    axs[1].set_title("Duration (seconds) vs Max Evictions")
    axs[1].set_xlabel("Max Evictions")
    axs[1].set_ylabel("Duration (seconds)")
    axs[1].grid(True)
    axs[1].legend()

    # Adjust layout to avoid overlap and display the plots
    plt.tight_layout()
    plt.show()
