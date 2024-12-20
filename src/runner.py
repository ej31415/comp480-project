# Main script
import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from pympler import asizeof

from structures.simple_bloom_filter import BloomFilterSimple
from structures.counting_bloom_filter import CountingBloomFilter
from structures.cuckoo_filter import CuckooFilter
from structures.consistent_hashing import ConsistentHashing
from storage_system import System

# Read data
main_dataframe = pd.DataFrame()
data_files = glob.glob("data/names/*.txt")
data_list = []
for file in data_files:
	sub_data = pd.read_csv(file, sep=',', names=["Name", "Sex", "Frequency"])
	data_list.append(sub_data)
main_dataframe = pd.concat(data_list, axis=0)
names = main_dataframe.iloc[:, 0]
names = names.unique()
print(f"There are {len(names)} unique names.")

main_dataframe = pd.read_csv("data/medium_articles.csv")
articles = main_dataframe.iloc[:, 0].unique()
print(f"There are {len(articles)} articles.")

def benchmark_insertion():
	# Set up baseline system
	usernames = set([])
	data = set([])
	base = (usernames, data)

	# Do operations

	start_times = []
	end_times = []

	start_mem = asizeof.asizeof(base) / 1000
	end_mems = [start_mem]

	periods = 10
	part_names = math.ceil(names.size / periods)
	part_articles = math.ceil(articles.size / periods)
	for period in range(periods):
		print(f"Evaluating period {period + 1}...")
		start_times.append(time.time())
		i, j = period * part_names, period * part_articles
		while i < (period + 1) * part_names and i < names.size:
			base[0].add(names[i])
			i += 1
		while j < (period + 1) * part_articles and j < articles.size:
			base[1].add(articles[j])
			j += 1
		end_times.append(time.time())
		end_mems.append(asizeof.asizeof(base) / 1000)
		print(f"Inserted {len(base[0])} usernames and {len(base[1])} items.")


	# Find total time to do said operations
	base_time = end_times[len(end_times) - 1] - start_times[0]
	print(f"Base took a total of {base_time} time.")

	# Find total memory usage
	base_mem = end_mems[len(end_mems) - 1] - start_mem
	print(f"Base took a total of {base_mem} memory.")

	# Plot and save
	total_time = []
	for p in range(periods):
		total_time.append((total_time[p - 1] if p > 0 else 0) + end_times[p] - start_times[p])
	plt.plot(range(1, 11), total_time, color="blue")
	plt.title("Python Set Insertion Times")
	plt.xlabel("Sections")
	plt.ylabel("Time from Start (seconds)")
	plt.savefig("plots/base-time.png")
	plt.clf()

	plt.plot(range(0, 11), end_mems, color="orange")
	plt.title("Python Set Insertion Memory")
	plt.xlabel("Sections")
	plt.ylabel("Memory Usage (KB)")
	plt.savefig("plots/base-mem.png")
	plt.clf()


	# Benchmarking

	# Set up test system
	systems = {}

	fp_rates = [0.01, 0.005, 0.001, 0.0005, 0.0001]
	trees = ["", "bst", "rbt"]
	lookup_table = {
		"simple_bloom": "Simple Bloom Filter",
		"counting_bloom": "Counting Bloom Filter",
		"cuckoo_filter": "Cuckoo Filter",
		"simple": "Naive Ring",
		"bst": "Binary Search Tree Supported",
		"rbt": "Red-Black Tree Supported"
	}

	print("Initializing Systems")
	overheads = {}
	for rate in fp_rates:
		print(f"Rate {rate}")
		for tree in trees:
			print(f"Tree {tree}")
			start = time.time()
			systems[f"simple_bloom({rate})-{'simple' if tree=='' else tree}_ch"] = System(BloomFilterSimple(false_positive_rate=rate, key_num=103600), ConsistentHashing(ring_size=1000000, num_servers=10000, tree=tree))
			end = time.time()
			overheads[f"simple_bloom({rate})-{'simple' if tree=='' else tree}_ch"] = end - start
			start = time.time()
			systems[f"counting_bloom({rate})-{'simple' if tree=='' else tree}_ch"] = System(CountingBloomFilter(false_positive_rate=rate, key_num=103600), ConsistentHashing(ring_size=1000000, num_servers=10000, tree=tree))
			end = time.time()
			overheads[f"counting_bloom({rate})-{'simple' if tree=='' else tree}_ch"] = end - start
			start = time.time()
			systems[f"cuckoo_filter({rate})-{'simple' if tree=='' else tree}_ch"] = System(CuckooFilter(bucket_size=6, num_buckets=20370, fingerprint_size=6, max_evictions=500), ConsistentHashing(ring_size=1000000, num_servers=10000, tree=tree))
			end = time.time()
			overheads[f"cuckoo_filter({rate})-{'simple' if tree=='' else tree}_ch"] = end - start

	# Do some operations
	print("Begin benchmarking")
	for name, system in systems.items():
		start_times = []
		end_times = []

		start_mem = asizeof.asizeof(system) / 1000
		end_mems = [start_mem]

		periods = 10
		part_names = math.ceil(names.size / periods)
		part_articles = math.ceil(articles.size / periods)
		for period in range(periods):
			print(f"Evaluating period {period + 1}...")
			start_times.append(time.time())
			i, j = period * part_names, period * part_articles
			while i < (period + 1) * part_names and i < names.size:
				system.add_user(names[i])
				i += 1
			while j < (period + 1) * part_articles and j < articles.size:
				system.add_item(articles[j])
				j += 1
			end_times.append(time.time())
			end_mems.append(asizeof.asizeof(system) / 1000)


		# Find total time to do said operations
		op_time = end_times[len(end_times) - 1] - start_times[0]
		print(f"{name} took a total of {op_time} time.")

		# Find total memory usage
		mem = end_mems[len(end_mems) - 1] - start_mem
		print(f"{name} took a total of {mem} memory.")

		# Plot and save
		total_time = []
		for p in range(periods):
			total_time.append((total_time[p - 1] if p > 0 else 0) + end_times[p] - start_times[p])
		plt.plot(range(1, 11), total_time, color="blue")
		plt.title(f"{lookup_table[name[:name.index('(')]]} {name[name.index('('):name.index(')') + 1]} x {lookup_table[name.split('-')[1].split('_')[0]]} Insertion Times")
		plt.xlabel("Sections")
		plt.ylabel("Time from Start (seconds)")
		plt.savefig(f"plots/{name}-time.png")
		plt.clf()

		plt.plot(range(0, 11), end_mems, color="orange")
		plt.title(f"{lookup_table[name[:name.index('(')]]} {name[name.index('('):name.index(')') + 1]} x {lookup_table[name.split('-')[1].split('_')[0]]} Insertion Memory")
		plt.xlabel("Sections")
		plt.ylabel("Memory Usage (KB)")
		plt.savefig(f"plots/{name}-mem.png")
		plt.clf()

	print(overheads)

def benchmark_consistent_hashing_simulation(fail_probability=0.2, time_steps=1000, cycle_times=1000):
	print("Initializing Systems")
	simple = ConsistentHashing(ring_size=1000000, num_servers=10000, tree='')
	bst = ConsistentHashing(ring_size=1000000, num_servers=10000, tree="bst")
	rbt = ConsistentHashing(ring_size=1000000, num_servers=10000, tree="rbt")

	for article in articles:
		simple.insert(article)
		bst.insert(article)
		rbt.insert(article)
	
	print(f"Benchmark Consistent Hashing where servers go offline/online with probability {fail_probability} at each time step, for {time_steps} steps.")
	up_server_ids = set()
	for i in range(10000):
		up_server_ids.add(i)
	down_server_ids = set()
	performance_times = [[], [], []]
	for _ in range(time_steps):
		if np.random.random() >= fail_probability:
			continue

		sim_off = True
		if len(down_server_ids) > 0 and np.random.random() < 0.5:
			sim_off = False
		
		if sim_off:
			server_id = up_server_ids.pop()

			start = time.time()
			simple.simulate_offline(server_id)
			end = time.time()
			performance_times[0].append((0 if len(performance_times[0]) == 0 else performance_times[0][len(performance_times[0]) - 1]) + (end - start))

			start = time.time()
			bst.simulate_offline(server_id)
			end = time.time()
			performance_times[1].append((0 if len(performance_times[1]) == 0 else performance_times[1][len(performance_times[1]) - 1]) + (end - start))

			start = time.time()
			rbt.simulate_offline(server_id)
			end = time.time()
			performance_times[2].append((0 if len(performance_times[2]) == 0 else performance_times[2][len(performance_times[2]) - 1]) + (end - start))

			down_server_ids.add(server_id)
		else:
			server_id = down_server_ids.pop()

			start = time.time()
			simple.simulate_online(server_id)
			end = time.time()
			performance_times[0].append((0 if len(performance_times[0]) == 0 else performance_times[0][len(performance_times[0]) - 1]) + (end - start))

			start = time.time()
			bst.simulate_online(server_id)
			end = time.time()
			performance_times[1].append((0 if len(performance_times[1]) == 0 else performance_times[1][len(performance_times[1]) - 1]) + (end - start))

			start = time.time()
			rbt.simulate_online(server_id)
			end = time.time()
			performance_times[2].append((0 if len(performance_times[2]) == 0 else performance_times[2][len(performance_times[2]) - 1]) + (end - start))

			up_server_ids.add(server_id)

	length = len(performance_times[0])	
	plt.plot(range(length), performance_times[0], label="Simple Ring")
	plt.plot(range(length), performance_times[1], label="Binary Search Tree Supported")
	plt.plot(range(length), performance_times[2], label="Red-Black Tree Supported")
	plt.title("Random Online/Offline Simulations")
	plt.xlabel("Operation")
	plt.ylabel("Cumulative Time (seconds)")
	plt.legend()
	plt.savefig("plots/consistent_hashing_rand_sim.png")
	plt.clf()


	print("Reinitializing Systems")
	simple = ConsistentHashing(ring_size=1000000, num_servers=10000, tree='')
	bst = ConsistentHashing(ring_size=1000000, num_servers=10000, tree="bst")
	rbt = ConsistentHashing(ring_size=1000000, num_servers=10000, tree="rbt")

	for article in articles:
		simple.insert(article)
		bst.insert(article)
		rbt.insert(article)
	
	print(f"Benchmark Consistent Hashing where servers fail and restart {cycle_times} times.")
	performance_times = [0, 0, 0]
	for _ in range(cycle_times):
		server_id = np.random.randint(0, 10000)

		start = time.time()
		simple.simulate_offline(server_id)
		simple.simulate_online(server_id)
		end = time.time()
		performance_times[0] += (end - start)

		start = time.time()
		bst.simulate_offline(server_id)
		bst.simulate_online(server_id)
		end = time.time()
		performance_times[1] += (end - start)

		start = time.time()
		rbt.simulate_offline(server_id)
		rbt.simulate_online(server_id)
		end = time.time()
		performance_times[2] += (end - start)

	types = ["Simple Ring", "Binary Search Tree Supported", "Red-Black Tree Supported"]
	plt.figure(figsize=(12, 5))
	plt.bar(types, performance_times)
	plt.title(f"{cycle_times} Online/Offline Simulations")
	plt.xlabel("Consistent Hashing Type")
	plt.ylabel("Cumulative Time (seconds)")
	plt.savefig("plots/consistent_hashing_set_sim.png")
	plt.clf()

benchmark_insertion()
# benchmark_consistent_hashing_simulation()