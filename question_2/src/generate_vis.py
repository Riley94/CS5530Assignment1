import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# build directory paths
base_path = os.path.join(os.path.dirname(__file__), '..')
raw_data_path = os.path.join(base_path, 'data_raw/StudentsPerformance.csv')
clean_data_path = os.path.join(base_path, 'data_clean/data_cleaned.csv')
scatter_matrix_path = os.path.join(base_path, 'results/scatter_matrix.png')
hist_path = os.path.join(base_path, 'results/numerical_data_hist.png')

raw_data = pd.read_csv(raw_data_path)
data_mapped = raw_data.copy()
mapping_data = []

for col in raw_data.columns:
    if (raw_data[col].dtype == 'object'):
        # map the unique values to integers from 0 to n
        unique_values = raw_data[col].unique()
        mapping = dict(zip(unique_values, range(len(unique_values))))
        data_mapped[col] = data_mapped[col].replace(mapping)
        mapping_data.append({ col : mapping })

data_mapped.to_csv(clean_data_path, index=False)

plt.figure(figsize=(20, 20))
plt.suptitle('Histograms of Numerical Columns')
for i, col in enumerate(raw_data.select_dtypes(include=['int64']).columns):
    plt.subplot(3, 3, i + 1)
    raw_data[col].plot(kind='hist', title=col)
    plt.xlabel(col)
    plt.ylabel('Number of Students')

# replace x axis labels with column names
plt.savefig(hist_path)

# had to rename the column to avoid issues with the '/' character
data_mapped.rename(columns={'race/ethnicity': 'race_ethnicity'}, inplace=True)

for mapping in mapping_data:
    for key in mapping:
        if key == 'race/ethnicity':
            mapping['race_ethnicity'] = mapping[key]
            del mapping[key]
            break

colors = ['blue', 'orange', 'green', 'purple', 'pink']
for data in mapping_data:
    for key, value in data.items():
        plt.figure(figsize=(10, 6))
        for (category, index), color in zip(value.items(), colors[:len(value)]):
            # Create a histogram for each category
            plt.hist(data_mapped[data_mapped[key] == index][key], label=category, color=color, bins=10, rwidth=0.8)

        plt.xticks([]) # Remove x-axis labels
        plt.legend() # Show legend to differentiate categories
        plt.title(f'Distribution of {key}')
        plt.ylabel('Frequency')
        plt.savefig(f'{base_path}/results/{key}_dist.png')

pd.plotting.scatter_matrix(raw_data, figsize=(20, 20), diagonal='kde')
plt.savefig(scatter_matrix_path)

# Set up color palette for the score types
color_palette = {'math score': 'skyblue', 'reading score': 'lightgreen', 'writing score': 'salmon'}
score_vars = ['math score', 'reading score', 'writing score']
categorical_vars = data_mapped.drop(score_vars, axis=1).columns
# using raw data again to keep class labels
data_for_boxplot = raw_data.copy()
data_for_boxplot.rename(columns={'race/ethnicity': 'race_ethnicity'}, inplace=True)

# Loop through each categorical variable to create a separate boxplot
for cat_var in categorical_vars:
    plt.figure(figsize=(10, 6))
    # Melting the dataframe to long format for easy plotting with seaborn
    df_melted = pd.melt(data_for_boxplot, id_vars=[cat_var], value_vars=score_vars, var_name='Score Type', value_name='Score')
    sns.boxplot(x=cat_var, y='Score', hue='Score Type', data=df_melted, palette=color_palette)
    plt.title(f'Distribution of {cat_var} w.r.t. Scores')
    plt.legend(title='Score Type')
    plt.tight_layout()
    plt.savefig(f'{base_path}/results/{cat_var}_boxplot.png')

# Loop through each categorical variable to create a separate violin plot
for cat_var in categorical_vars:
    plt.figure(figsize=(10, 6))
    df_melted = pd.melt(data_for_boxplot, id_vars=[cat_var], value_vars=score_vars, var_name='Score Type', value_name='Score')
    sns.violinplot(x=cat_var, y='Score', hue='Score Type', data=df_melted, palette=color_palette)
    plt.title(f'Distribution of {cat_var} w.r.t. Scores')
    plt.legend(title='Score Type')
    plt.tight_layout()
    plt.savefig(f'{base_path}/results/{cat_var}_violin.png')


