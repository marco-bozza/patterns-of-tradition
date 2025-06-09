import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# === Paths ===
input_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions"
output_table_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/tables/gift_freq_gift.xlsx"
output_graph_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/graphs/gift_freq_gift.png"

# === Load data ===
beowulf = pd.read_excel(os.path.join(input_path, "beowulf_freq_gift.xlsx"))
lotr = pd.read_excel(os.path.join(input_path, "lotr_freq_gift.xlsx"))

# === Calculate relative frequencies ===
beowulf["rel_freq"] = (beowulf["absolute_frequency"] / beowulf["absolute_frequency"].sum()) * 100
lotr["rel_freq"] = (lotr["absolute_frequency"] / lotr["absolute_frequency"].sum()) * 100

# === Final display order ===
ordered_categories = [
    "Treasures", "Arms", "Hospitality",
    "Transports", "Consorts", "Provisions", "Objects"  
]

df_order = pd.DataFrame({"gift_category": ordered_categories})

# === Merge and reorder data ===
merged = df_order.merge(
    beowulf[["gift_category", "absolute_frequency", "rel_freq"]],
    on="gift_category", how="left"
).merge(
    lotr[["gift_category", "absolute_frequency", "rel_freq"]],
    on="gift_category", how="left",
    suffixes=("_beowulf", "_lotr")
).fillna(0)

# === Save Excel table ===
final_df = merged.copy()
final_df.columns = [
    "Gift category", "Beowulf (abs.)", "Beowulf (%)",
    "LOTR (abs.)", "LOTR (%)"
]
final_df.to_excel(output_table_path, index=False)
print(f"✅ Table saved to: {output_table_path}")

# === Plot horizontal bar chart with correct top-down order ===
bar_width = 0.4
y = np.arange(len(ordered_categories))

# Reverse data for top-to-bottom category order
merged_plot = merged.iloc[::-1]
labels = merged_plot["gift_category"]
beowulf_vals = merged_plot["rel_freq_beowulf"]
lotr_vals = merged_plot["rel_freq_lotr"]

plt.figure(figsize=(10, 6))
plt.barh(y + bar_width/2, beowulf_vals, height=bar_width,
         color="darkorange", edgecolor="black", label="Beowulf")
plt.barh(y - bar_width/2, lotr_vals, height=bar_width,
         color="steelblue", edgecolor="black", label="LOTR")

# Axis labels and formatting
plt.yticks(y, labels, fontsize=12)
# Set x-axis max slightly above the highest value
max_val = max(beowulf_vals.max(), lotr_vals.max())
x_max = min(100, (int(max_val // 5) + 2) * 5)  # round up to next 5%
plt.xticks(np.arange(0, x_max + 1, 5), fontsize=12)
plt.xlim(0, x_max)

plt.xlabel("Relative Frequency (%)", fontsize=14)
plt.ylabel("Gift Category", fontsize=14)
plt.title("Relative Frequency of Gift Categories in Gift-Giving Events", fontsize=16,)

# Add grid lines
for x in np.arange(5, 100, 5):
    plt.axvline(x=x, linestyle="dashed", color="gray", linewidth=0.5)

plt.axvline(x=0, color="black", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(output_graph_path, dpi=300)
plt.close()
print(f"✅ Chart saved to: {output_graph_path}")

