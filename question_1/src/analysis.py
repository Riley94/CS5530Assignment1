import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

data = pd.read_csv('../data_clean/data_clean.csv')
data.hist(bins=15, figsize=(10, 10))
plt.savefig('../results/distribution.png')

pd.plotting.scatter_matrix(data, figsize=(10, 10), diagonal='kde')
plt.savefig('../results/scatter_matrix.png')

t_scores = pd.DataFrame(columns=['Variable', 'T-Statistic', 'P-Value'])

# Perform t-test on variables of data_no_na
for column_name in data:
    if column_name != 'Frailty':
        variable = data[column_name]
        target = data['Frailty']
        t_statistic, p_value = ttest_ind(variable, target)
        t_scores.loc[len(t_scores.index)] = [column_name, t_statistic, p_value]

t_scores.to_csv('../results/results.txt', index=False)