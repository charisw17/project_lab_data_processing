import matplotlib.pyplot as plt

from resources.path_util import PATH_DATA_OUT

# Hardcoded data from the provided Excel sheet
variants = ["BG10_WT", "BG10_005", "BG10_009", "BG11gut1Δ_001", "BG11gut1Δ_011"]

absorbance_values = [0.000, 888.161, 779.254, 1690.663, 356.718]

hplc_values = [0.00, 214.28, 432.22, 1050.63, 282.74]

# Create the bar plot
plt.figure(figsize=(8, 6))
bar_width = 0.35
index = range(len(variants))

# Plot bars for absorbance and HPLC values side by side with specified colors
plt.bar([i - bar_width / 2 for i in index], absorbance_values, bar_width, label='Absorbance [ng/mL]', color='#a00000',
        edgecolor='black')
plt.bar([i + bar_width / 2 for i in index], hplc_values, bar_width, label='HPLC [ng/mL]', color='#1a80bb',
        edgecolor='black')

plt.ylabel('Concentration [ng/mL]')
plt.title('Betanin concentration via HPLC vs. Absorbance')
plt.xticks(index, variants, rotation=45)
plt.legend()
plt.tight_layout()

# plt.show()
plt.savefig(PATH_DATA_OUT / "hplc_vs_abs_plot.svg", format='svg')
