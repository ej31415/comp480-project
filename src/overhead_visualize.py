import matplotlib.pyplot as plt
import statistics as stats

overhead_dict = {'simple_bloom(0.01)-simple_ch': 0.15502500534057617, 'counting_bloom(0.01)-simple_ch': 0.21960234642028809, 
                 'cuckoo_filter(0.01)-simple_ch': 0.15420961380004883, 'simple_bloom(0.01)-bst_ch': 0.32874512672424316, 
                 'counting_bloom(0.01)-bst_ch': 0.37714505195617676, 'cuckoo_filter(0.01)-bst_ch': 0.3141458034515381, 
                 'simple_bloom(0.01)-rbt_ch': 0.48389148712158203, 'counting_bloom(0.01)-rbt_ch': 0.394808292388916, 
                 'cuckoo_filter(0.01)-rbt_ch': 0.4068722724914551, 'simple_bloom(0.005)-simple_ch': 0.24600982666015625, 
                 'counting_bloom(0.005)-simple_ch': 0.14870595932006836, 'cuckoo_filter(0.005)-simple_ch': 0.13397765159606934, 
                 'simple_bloom(0.005)-bst_ch': 0.4509999752044678, 'counting_bloom(0.005)-bst_ch': 0.2985408306121826, 
                 'cuckoo_filter(0.005)-bst_ch': 0.2827451229095459, 'simple_bloom(0.005)-rbt_ch': 0.4070308208465576, 
                 'counting_bloom(0.005)-rbt_ch': 0.3768925666809082, 'cuckoo_filter(0.005)-rbt_ch': 0.5500130653381348, 
                 'simple_bloom(0.001)-simple_ch': 0.14011478424072266, 'counting_bloom(0.001)-simple_ch': 0.15001916885375977, 
                 'cuckoo_filter(0.001)-simple_ch': 0.13294672966003418, 'simple_bloom(0.001)-bst_ch': 0.3081173896789551, 
                 'counting_bloom(0.001)-bst_ch': 0.48752737045288086, 'cuckoo_filter(0.001)-bst_ch': 0.3294816017150879, 
                 'simple_bloom(0.001)-rbt_ch': 0.3612501621246338, 'counting_bloom(0.001)-rbt_ch': 0.43514418601989746, 
                 'cuckoo_filter(0.001)-rbt_ch': 0.45097923278808594, 'simple_bloom(0.0005)-simple_ch': 0.12832975387573242, 
                 'counting_bloom(0.0005)-simple_ch': 0.1567668914794922, 'cuckoo_filter(0.0005)-simple_ch': 0.34525537490844727, 
                 'simple_bloom(0.0005)-bst_ch': 0.28846001625061035, 'counting_bloom(0.0005)-bst_ch': 0.3768002986907959, 
                 'cuckoo_filter(0.0005)-bst_ch': 0.32976508140563965, 'simple_bloom(0.0005)-rbt_ch': 0.4179952144622803, 
                 'counting_bloom(0.0005)-rbt_ch': 0.3918025493621826, 'cuckoo_filter(0.0005)-rbt_ch': 0.40941286087036133, 
                 'simple_bloom(0.0001)-simple_ch': 0.1490936279296875, 'counting_bloom(0.0001)-simple_ch': 0.3768043518066406, 
                 'cuckoo_filter(0.0001)-simple_ch': 0.15735530853271484, 'simple_bloom(0.0001)-bst_ch': 0.3793802261352539, 
                 'counting_bloom(0.0001)-bst_ch': 0.3348507881164551, 'cuckoo_filter(0.0001)-bst_ch': 0.3364531993865967, 
                 'simple_bloom(0.0001)-rbt_ch': 0.44635987281799316, 'counting_bloom(0.0001)-rbt_ch': 0.4251275062561035, 
                 'cuckoo_filter(0.0001)-rbt_ch': 0.3926384449005127
                 }

fp_rates = [0.01, 0.005, 0.001, 0.0005, 0.0001]
simple_bloom_simple_ch = []
simple_bloom_bst_ch = []
simple_bloom_rbt_ch = []
counting_bloom_simple_ch = []
counting_bloom_bst_ch = []
counting_bloom_rbt_ch = []

for k, v in overhead_dict.items():
    if "simple_bloom" in k and "simple_ch" in k:
        simple_bloom_simple_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    elif "simple_bloom" in k and "bst_ch" in k:
        simple_bloom_bst_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    elif "simple_bloom" in k and "rbt_ch" in k:
        simple_bloom_rbt_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    elif "counting_bloom" in k and "simple_ch" in k:
        counting_bloom_simple_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    elif "counting_bloom" in k and "bst_ch" in k:
        counting_bloom_bst_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    elif "counting_bloom" in k and "rbt_ch" in k:
        counting_bloom_rbt_ch.append((float(k[k.index('(') + 1: k.index(')')]), v))
    else:
        print("No match.")

simple_bloom_simple_ch.sort()
simple_bloom_bst_ch.sort()
simple_bloom_rbt_ch.sort()
counting_bloom_simple_ch.sort()
counting_bloom_bst_ch.sort()
counting_bloom_rbt_ch.sort()

# Graph false positive rate changes for each
plt.plot([x[0] for x in simple_bloom_simple_ch], [x[1] for x in simple_bloom_simple_ch], label="Simple Bloom x List")
plt.plot([x[0] for x in simple_bloom_bst_ch], [x[1] for x in simple_bloom_bst_ch], label="Simple Bloom x BST")
plt.plot([x[0] for x in simple_bloom_rbt_ch], [x[1] for x in simple_bloom_rbt_ch], label="Simple Bloom x RBT")
plt.plot([x[0] for x in counting_bloom_simple_ch], [x[1] for x in counting_bloom_simple_ch], label="Counting Bloom x List")
plt.plot([x[0] for x in counting_bloom_bst_ch], [x[1] for x in counting_bloom_bst_ch], label="Counting Bloom x BST")
plt.plot([x[0] for x in counting_bloom_rbt_ch], [x[1] for x in counting_bloom_rbt_ch], label="Counting Bloom x RBT")
plt.title("Overhead Times vs False Positive Rate for Each Structure")
plt.xlabel("False Positive Rate")
plt.ylabel("Time (seconds)")
plt.legend(loc="upper right")
plt.savefig("plots/overhead1.png")
plt.clf()

simple_bloom_simple_ch = []
simple_bloom_bst_ch = []
simple_bloom_rbt_ch = []
counting_bloom_simple_ch = []
counting_bloom_bst_ch = []
counting_bloom_rbt_ch = []

for k, v in overhead_dict.items():
    if "simple_bloom" in k and "simple_ch" in k:
        simple_bloom_simple_ch.append(v)
    elif "simple_bloom" in k and "bst_ch" in k:
        simple_bloom_bst_ch.append(v)
    elif "simple_bloom" in k and "rbt_ch" in k:
        simple_bloom_rbt_ch.append(v)
    elif "counting_bloom" in k and "simple_ch" in k:
        counting_bloom_simple_ch.append(v)
    elif "counting_bloom" in k and "bst_ch" in k:
        counting_bloom_bst_ch.append(v)
    elif "counting_bloom" in k and "rbt_ch" in k:
        counting_bloom_rbt_ch.append(v)
    else:
        print("No match.")

labs = ["Simple Bloom x List", "Simple Bloom x BST", "Simple Bloom x RBT", "Counting Bloom x List", "Counting Bloom x BST", "Counting Bloom x RBT"]
avgs = [stats.fmean(simple_bloom_simple_ch), stats.fmean(simple_bloom_bst_ch), stats.fmean(simple_bloom_rbt_ch), stats.fmean(counting_bloom_simple_ch), stats.fmean(counting_bloom_bst_ch), stats.fmean(counting_bloom_rbt_ch)]

# Graph average times for each
plt.figure(figsize=(15, 5))
plt.bar(labs, avgs)
plt.title("Average Overhead Times for Each Structure")
plt.xlabel("Structure")
plt.ylabel("Average Time (seconds)")
plt.savefig("plots/overhead2.png")
plt.clf()