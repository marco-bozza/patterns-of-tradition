import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# === Paths ===
base_input = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions"
output_graph = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/graphs/gift_freq_recipient.png"
output_table = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/tables/gift_freq_recipient.xlsx"

# === Load data ===
beo = pd.read_excel(os.path.join(base_input, "beowulf_freq_recipient.xlsx"))
lotr = pd.read_excel(os.path.join(base_input, "lotr_freq_recipient.xlsx"))

# === Normalize labels ===
rename_map = {
    "Good supernaturals": "G. supernat.",
    "Evil supernaturals": "E. supernat."
}
beo["recipient_category"] = beo["recipient_category"].replace(rename_map)
lotr["recipient_category"] = lotr["recipient_category"].replace(rename_map)

# === Calculate relative frequency ===
beo["rel_freq"] = (beo["absolute_frequency"] / beo["absolute_frequency"].sum()) * 100
lotr["rel_freq"] = (lotr["absolute_frequency"] / lotr["absolute_frequency"].sum()) * 100

# === Category order (top to bottom) ===
ordered_categories = ["Heroes", "Rulers", "Commoners", "G. supernat.", "E. supernat." ]
df_order = pd.DataFrame({"recipient_category": ordered_categories})

# === Merge data ===
merged = df_order.merge(
    beo[["recipient_category", "absolute_frequency", "rel_freq"]],
    on="recipient_category", how="left"
).merge(
    lotr[["recipient_category", "absolute_frequency", "rel_freq"]],
    on="recipient_category", how="left",
    suffixes=("_beowulf", "_lotr")
).fillna(0)

# === Save Excel table ===
final = merged.copy()
final.columns = ["Recipient category", "Beowulf (abs.)", "Beowulf (%)", "LOTR (abs.)", "LOTR (%)"]
final.to_excel(output_table, index=False)
print(f"✅ Table saved to: {output_table}")

# === Prepare for plotting ===
bar_width = 0.4
y = np.arange(len(ordered_categories))

# Reverse only labels (top to bottom visual order)
merged_plot = merged.iloc[::-1]
labels = merged_plot["recipient_category"]
beo_vals = merged_plot["rel_freq_beowulf"]
lotr_vals = merged_plot["rel_freq_lotr"]

# === Plot ===
plt.figure(figsize=(10, 6))
plt.barh(y + bar_width/2, beo_vals, height=bar_width, color="darkorange", edgecolor="black", label="Beowulf")
plt.barh(y - bar_width/2, lotr_vals, height=bar_width, color="steelblue", edgecolor="black", label="LOTR")

# Dynamic x-axis
max_val = max(beo_vals.max(), lotr_vals.max())
x_max = min(100, (int(max_val // 5) + 2) * 5)
plt.xticks(np.arange(0, x_max + 1, 5), fontsize=12)
plt.xlim(0, x_max)

plt.yticks(y, labels, fontsize=12)
plt.xlabel("Relative Frequency (%)", fontsize=14)
plt.ylabel("Recipient Category", fontsize=14)
plt.title("Relative Frequency of Recipient Categories in Gift-Giving Events", fontsize=16,)

for x in np.arange(5, x_max, 5):
    plt.axvline(x=x, color="grey", linestyle="dashed", linewidth=0.6)

plt.axvline(x=0, color="black", linewidth=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(output_graph, dpi=300)
plt.close()
print(f"✅ Chart saved to: {output_graph}")
