# Main script
import glob
import pandas as pd

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
articles = main_dataframe.iloc[:, 0]
print(f"There are {len(articles)} articles.")

# Set up baseline system
usernames = set([])
data = {}
base = (usernames, data)

# Do operations
# Check memory usage after each operation

# Find total time to do said operations



# Benchmarking

# Set up test system

# Do some operations
# Check memory usage after each operation

# Find total time to do said operations