"""
Visualizes Gene Ontology (GO) term enrichment as horizontal bar charts.

Creates publication-quality plots showing significantly enriched GO terms (p ≤ 0.05)
across GO categories (BP, CC, MF), with bars color-coded by -log(p-value).

Input:
    - CSV file with columns: Term, Count, Pvalue, group. Manually cleaned GO enrichment results with duplicates removed
    - Currently set to: 'tj_3_gsea_nodups.csv' (line 7)
    
Output:
    - High-resolution PNG (300 DPI) with subplots per GO category
    - Currently set to: 'tj_3_goterms_plot.png' (line 115)
    
Features:
    - Top 100 terms per group by gene count
    - Viridis colormap scaled by significance
    - Shared y-axis for cross-group comparison
    - 35-character term truncation for readability
    
Note: Modify input/output filenames to generate plots for me_1, me_3, or tj_1 samples.

Dependencies: pandas, matplotlib, numpy

Data: Available on request.
Citation: https://doi.org/10.1002/csc2.21392
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# Read the CSV file into a DataFrame
df = pd.read_csv('tj_3_gsea_nodups.csv')

# Filter genes with p-value <= 0.05
df = df[df['Pvalue'] <= 0.05]

# Calculate -log(p-value) for better visualization
df['-log(Pvalue)'] = -np.log10(df['Pvalue'])

# Truncate GO Terms to 35 characters for better readability
df['Term'] = df['Term'].apply(lambda x: x[:35] if len(x) > 35 else x)

# Get unique groups from the 'group' column
groups = df['group'].unique()

# Calculate the number of rows for each group
rows_per_group = df.groupby('group').size()

# Calculate width ratios for subplots based on the number of rows in each group
total_rows = rows_per_group.sum()
width_ratios = [rows_per_group[group] / total_rows for group in groups] + [0.02]

# Create a figure with subplots arranged horizontally
fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, len(groups) + 1, width_ratios=width_ratios)

# Create a list of subplots for each group
axs = [fig.add_subplot(gs[i]) for i in range(len(groups))]
cbar_ax = fig.add_subplot(gs[-1])  # Axis for the color bar

# Normalize the -log(p-value) for consistent color mapping across all groups
norm = plt.Normalize(df['-log(Pvalue)'].min(), df['-log(Pvalue)'].max())

# Choose a colormap
cmap = plt.get_cmap('viridis')

# Determine the maximum count across all groups to set a common y-axis limit
max_count = df['Count'].max()

# Increase font sizes
title_fontsize = 14
label_fontsize = 14
tick_fontsize = 14
cbar_label_fontsize = 14
cbar_tick_fontsize = 14

# Generate bar charts for each group
for i, group in enumerate(groups):
    df_group = df[df['group'] == group]
    
    # Select the top 100 rows based on counts
    df_group_top = df_group.nlargest(100, 'Count')
    
    # Get colors for the bars based on the colormap
    colors = cmap(norm(df_group_top['-log(Pvalue)']))

    # Create a bar chart for the current group
    bars = axs[i].bar(df_group_top['Term'], df_group_top['Count'], color=colors)
    
    # Set the title for each subplot
    axs[i].set_title(f'{group}', fontsize=title_fontsize)
    axs[i].set_xlabel('')
    axs[i].set_ylim(0, max_count)  # Set a common y-axis limit
    
    # Remove y-axis labels and ticks for all but the first subplot
    if i > 0:
        axs[i].set_ylabel('')
        axs[i].yaxis.set_ticks([])
    
    # Remove top and right border lines
    axs[i].spines['top'].set_visible(False)
    axs[i].spines['right'].set_visible(False)
    
    # Remove left border lines on subplots 2 and 3 (index 1 and 2)
    if i in [1, 2]:
        axs[i].spines['left'].set_visible(False)

    # Set tick parameters
    axs[i].tick_params(axis='x', labelsize=tick_fontsize)
    axs[i].tick_params(axis='y', labelsize=tick_fontsize)

# Add a color bar to the right of the subplots
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='vertical')
cbar.set_label('-log(p-value)', fontsize=cbar_label_fontsize)
cbar.set_ticks([df['-log(Pvalue)'].min(), df['-log(Pvalue)'].max()])
cbar.set_ticklabels([f"{df['Pvalue'].min():.1e}", f"{df['Pvalue'].max():.1e}"])
cbar.ax.tick_params(labelsize=cbar_tick_fontsize)

# Rotate x-axis labels for better readability
for ax in axs:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=70, ha='right', fontsize=tick_fontsize)

# Label the y-axis on the first subplot
axs[0].set_ylabel('Gene Count', fontsize=label_fontsize)

# Add a single x-axis label for all subplots
fig.text(0.5, 0.01, 'GO terms', ha='center', fontsize=label_fontsize)

# Adjust layout for a better fit
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.subplots_adjust(wspace=0.02)

# Save the plot as a JPEG file
# plt.savefig('tj_3_goterms_plot.jpeg', format='jpeg', dpi=300)
# print('plot saved as "tj_3_goterms_plot.jpeg"')

# Save the plot as a PNG file with 300 DPI
plt.savefig('tj_3_goterms_plot.png', dpi=300)
print('plot saved as "tj_3_goterms_plot.png"')

