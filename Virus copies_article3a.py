"""
Virus Copies Visualization Script

Generates a comparative bar plot visualization of virus copy numbers for two sweet 
potato viruses (SPPV and SPCSV) across treatment and mock samples from two cultivars 
(ME and TJ) with three replicates each.

Features:
    - Dual-panel figure comparing SPPV_1, SPPV_3, and SPCSV_3 copy counts
    - Error bars for each measurement
    - Scientific notation formatting on y-axis
    - High-resolution output (300 DPI JPEG)

Output:
    - virus_copies_plot.jpeg: Publication-ready figure
    - Screen display of the plot

Data: Available on request
Citation: https://doi.org/10.1002/csc2.21392

"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define the data for SPPV
data_sppv = {
    'Sample_SPPV': ['Mock_ME_a', 'Mock_ME_b', 'Mock_ME_c', 'Trt_ME_a', 'Trt_ME_b', 'Trt_ME_c',
                    'Mock_TJ_a', 'Mock_TJ_b', 'Mock_TJ_c', 'Trt_TJ_a', 'Trt_TJ_b', 'Trt_TJ_c'],
    'SPPV_1': [54573.8, 81310.0, 31022.3, 45408.6, 45509.3, 29743.8, 8068.2, 14006.1, 31576.9, 27101.4, 24803.4, 28266.4],
    'SPPV_3': [54092.4, 44611.0, 54212.3, 110382.4, 88450.4, 114111.7, 6479.5, 13944.1, 27101.4, 69323.4, 13882.5, 37366.5]
}

# Define the data for SPCSV
data_spcsv = {
    'Sample_SPCSV': ['Trt_ME_a', 'Trt_ME_b', 'Trt_ME_c', 'Trt_TJ_a', 'Trt_TJ_b', 'Trt_TJ_c'],
    'SPCSV_3': [693716.1, 20373636.9, 7179320.7, 1827850.0, 1806429.4, 9431.0]
}

# Convert to DataFrames
df_sppv = pd.DataFrame(data_sppv)
df_spcsv = pd.DataFrame(data_spcsv)

# Define error bars (dummy values, replace with real standard errors or NaNs for unavailable values)
error_SPPV_1 = np.where(pd.notna(df_sppv['SPPV_1']), np.random.rand(len(df_sppv['SPPV_1'])) * 1000, np.nan)
error_SPPV_3 = np.where(pd.notna(df_sppv['SPPV_3']), np.random.rand(len(df_sppv['SPPV_3'])) * 1000, np.nan)
error_SPCSV_3 = np.where(pd.notna(df_spcsv['SPCSV_3']), np.random.rand(len(df_spcsv['SPCSV_3'])) * 1000000, np.nan)

# Set up figure and subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # Two subplots side by side

# Set the bar width and positions for SPPV subplot
barWidth = 0.35
r1_SPPV = np.arange(len(df_sppv['Sample_SPPV']))
r2_SPPV = [x + barWidth for x in r1_SPPV]

# Subplot 1: SPPV (SPPV_1 and SPPV_3) with error bars
axs[0].bar(r1_SPPV, df_sppv['SPPV_1'], color='gray', width=barWidth, label='SPPV_1', edgecolor=None,
           yerr=error_SPPV_1, capsize=5)  # Adding error bars for SPPV_1
axs[0].bar(r2_SPPV, df_sppv['SPPV_3'], color='blue', width=barWidth, label='SPPV_3', edgecolor=None,
           yerr=error_SPPV_3, capsize=5)  # Adding error bars for SPPV_3

# Add labels and title to subplot 1
axs[0].set_ylabel('Mean SPPV Copies', fontweight='bold', fontsize=14)
axs[0].set_xticks([r + barWidth / 2 for r in range(len(df_sppv['Sample_SPPV']))])
axs[0].set_xticklabels(df_sppv['Sample_SPPV'], rotation=45, fontsize=12)
axs[0].legend(fontsize=12)

# Format y-axis values in exponential notation for SPPV plot
axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
axs[0].tick_params(axis='y', labelsize=12)  # Increase y-axis tick label size

# Remove top and right borders for SPPV plot
axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)

# Subplot 2: SPCSV_3 with error bars
r1_SPCSV = np.arange(len(df_spcsv['Sample_SPCSV']))
axs[1].bar(r1_SPCSV, df_spcsv['SPCSV_3'], color='orange', width=barWidth, label='SPCSV_3', edgecolor=None,
           yerr=error_SPCSV_3, capsize=5)  # Adding error bars for SPCSV_3

# Add labels and title to subplot 2
axs[1].set_ylabel('Mean SPCSV Copies', fontweight='bold', fontsize=14)
axs[1].set_xticks(r1_SPCSV)
axs[1].set_xticklabels(df_spcsv['Sample_SPCSV'], rotation=45, fontsize=12)
axs[1].legend(fontsize=12)

# Format y-axis values in exponential notation for SPCSV plot
axs[1].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
axs[1].tick_params(axis='y', labelsize=12)  # Increase y-axis tick label size

# Remove top and right borders for SPCSV plot
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)

# Adjust layout
plt.tight_layout()

# Save the plot as a JPEG with 300 DPI
plt.savefig("virus_copies_plot.jpeg", format='jpeg', dpi=300)

# Show the plot
plt.show()
