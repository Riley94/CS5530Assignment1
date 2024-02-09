import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# Set file paths
base_path = os.path.join(os.path.dirname(__file__), '..')
data_path = os.path.join(base_path, 'data_clean/data_clean.csv')
dist_path = os.path.join(base_path, 'results/distribution.png')
scatter_path = os.path.join(base_path, 'results/scatter_matrix.png')
results_path = os.path.join(base_path, 'results/results.txt')

data = pd.read_csv(data_path)
data.hist(bins=15, figsize=(10, 10))
plt.savefig(dist_path)

pd.plotting.scatter_matrix(data, figsize=(10, 10), diagonal='kde')
plt.savefig(scatter_path)

t_scores = pd.DataFrame(columns=['Variable', 'T-Statistic', 'P-Value'])

# Perform t-test
for column_name in data:
    if column_name != 'Frailty':
        variable = data[column_name]
        target = data['Frailty']
        t_statistic, p_value = ttest_ind(variable, target)
        t_scores.loc[len(t_scores.index)] = [column_name, t_statistic, p_value]

t_scores.to_csv(results_path, index=False)
