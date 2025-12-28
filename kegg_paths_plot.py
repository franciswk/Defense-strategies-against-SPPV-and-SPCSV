"""
Visualizes KEGG pathway enrichment as horizontal bar plots.

Purpose:
    Merges KEGG pathway analysis results with a pathway database and creates
    publication-quality plots showing the top enriched pathways by sequence count.

Workflow:
    1. Load KEGG enrichment results (e.g., 'me_1_kegg.csv') and pathway database
    2. Clean pathway IDs (remove 'ko' prefix, zero-pad to 5 digits)
    3. Merge on Pathway ID to retrieve full pathway metadata
    4. Manually curate results in Excel ('me_1_kegg_selected.csv') to remove unwanted pathways
    5. Plot top 50 pathways, color-coded by biological category
    6. Export as PNG at 300 DPI

Input Files:
    - 'kegg_pathways_db.csv': KEGG pathway database with categories
    - '{sample}_kegg.csv': Raw KEGG enrichment results (e.g., me_1_kegg.csv)
    - '{sample}_kegg_selected.csv': Manually curated pathway list (created in Excel)
    
Output Files:
    - '{sample}_kegg_merged.csv': Merged enrichment data with metadata
    - '{sample}_kegg_plot.png': Final visualization at 300 DPI

Note:
    To generate plots for other samples (me_3, tj_1, tj_3), modify the input
    filenames on lines 6 and 45, and output filename on line 101.
   
Dependencies: pandas, seaborn, matplotlib

# Data: Available on request.
# Citation: https://doi.org/10.1002/csc2.21392
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

kegg_db = pd.read_csv('kegg_pathways_db.csv')
print(kegg_db.info())
print(kegg_db.head())
#%%

me_1_kegg = pd.read_csv('me_1_kegg.csv')
print(me_1_kegg.info())
print(me_1_kegg.head())
#%%
# Remove 'ko' from 'Pathway ID' and save the df to file
me_1_kegg['Pathway ID'].replace('ko', '', regex=True, inplace=True)

me_1_kegg['Pathway ID'] = me_1_kegg['Pathway ID'].astype(str).str.zfill(5)

print(me_1_kegg.info())
print(me_1_kegg.head())
#%%
#  DataFrames
df1 = me_1_kegg

df2 = kegg_db

# Convert 'Pathway ID' in df2 to string to match df1
df2['Pathway ID'] = df2['Pathway ID'].astype(str).str.zfill(5)

# Merge the DataFrames on 'Pathway ID'
merged_df = pd.merge(df1, df2, on='Pathway ID', how='inner')

# Select only the required columns
merged_df = merged_df[['Category', 'Sub-category', 'Pathway', 'Pathway ID', 'No. of Seqs']]

# Sort descending by 'No. of Seqs'
merged_df = merged_df.sort_values(by='No. of Seqs', ascending=False)

# Save the result to a CSV file
merged_df.to_csv('me_1_kegg_merged.csv', index=False)

print(merged_df.head())
print(merged_df.info())
#%%
# Plot KEGG pathways enrichment

#Manually remove unwanted pathways in excel and save the file then use it to plot
try:
    me_1_kegg_select = pd.read_csv('me_1_kegg_selected.csv')
except FileNotFoundError:
    raise FileNotFoundError("Error: Prepare the file 'me_1_kegg_selected.csv' in excel first.")
#%%
# Sort the DataFrame by 'No. of Seqs' and select the top 30 rows
merged_df_top30 = me_1_kegg_select.nlargest(50, 'No. of Seqs')

# Define a custom color palette
colors = {
    'Metabolism': '#377eb8',  # blue
    'Genetic Information Processing': '#ff7f00',  # orange
    'Environmental Information Processing': '#4daf4a',  # green
    'Cellular Processes': '#e41a1c',  # red
    'Organismal Systems': '#984ea3',  # purple
}
#%%
'''
plt.figure(figsize=(10, 6))
sns.barplot(data=merged_df_top30, x='Pathway', y='No. of Seqs', hue='Category', dodge=False, palette=colors)
plt.xticks(rotation=90)
plt.xlabel('KEGG Pathway')
plt.ylabel('No. of Seqs')
plt.title('')
plt.legend(title='', bbox_to_anchor=(0.7, 1), loc='upper left', frameon=False)

# Remove the top and right borderlines
sns.despine()

plt.tight_layout()
plt.show()
'''
#%%
plt.figure(figsize=(6, 9))
sns.barplot(data=merged_df_top30, x='No. of Seqs', y='Pathway', hue='Category', dodge=False, palette=colors)
plt.xticks(rotation=90)
plt.xlabel('No. of Sequences')
plt.ylabel('KEGG Pathway')
plt.title('')

# Remove the legend
plt.legend([],[], frameon=False)

# Place the legend on top of the plot
# plt.legend(title='Category', loc='lower left', bbox_to_anchor=(0.5, 1.05), ncol=3, frameon=False)

# Remove the top and right borderlines
sns.despine()

plt.tight_layout()
plt.show()
#%%
plt.savefig('me_1_kegg_plot.png', dpi=300, bbox_inches='tight')
print('plot saved as "me_1_kegg_plot.png"')

