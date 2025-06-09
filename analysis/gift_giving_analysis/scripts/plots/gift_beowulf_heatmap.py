import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
file_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions/beowulf_freq_pairs.xlsx"
df = pd.read_excel(file_path)

# Replace names
replace_map = {
    "Good supernaturals": "G. supernat.",
    "Evil supernaturals": "E. supernat."
}

# Split pairs into giver and recipient
df[["giver", "recipient"]] = df["pair"].str.split(" → ", expand=True)
df["giver"] = df["giver"].replace(replace_map)
df["recipient"] = df["recipient"].replace(replace_map)

# Ordered categories
categories = ["Rulers", "Heroes", "Commoners", "G. supernat.", "E. supernat." ]

# Create heatmap matrix
heatmap_data = pd.DataFrame(index=categories, columns=categories, dtype=float)
for _, row in df.iterrows():
    giver = row["giver"]
    recipient = row["recipient"]
    freq = row["relative_frequency"] * 100
    heatmap_data.loc[giver, recipient] = freq
heatmap_data = heatmap_data.fillna(0)

# Custom x-axis positions
x_positions = np.arange(len(categories))
x_labels = ["Rulers", "Heroes", "Commoners", "G. supernat.", "E. supernat." ]

# Plot heatmap in orange tones
plt.figure(figsize=(10, 8))
ax = sns.heatmap(
    heatmap_data,
    annot=heatmap_data.applymap(lambda x: f"{x:.1f}%" if x > 0 else ""),
    fmt="",
    cmap="Oranges",
    linewidths=0.5,
    cbar_kws={'label': 'Relative Frequency (%)'},
    linecolor='lightgrey',
    square=True
)

plt.xlabel("Recipient Category", fontsize=14)
plt.ylabel("Giver Category", fontsize=14)

# Move x-axis labels slightly
plt.xticks(ticks=x_positions + 0.3, labels=x_labels, fontsize=12)
plt.yticks(rotation=0, fontsize=12)

# Set colorbar fontsize
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)
cbar.set_label('Relative Frequency (%)', fontsize=14)

plt.title("Heatmap of Gift-Giving Interactions in Beowulf", fontsize=16, pad=20)
plt.tight_layout()
plt.savefig("D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/graphs/gift_beowulf_heatmap.png", dpi=300)
plt.close()
