import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# === Paths ===
beo_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions/beowulf_freq_pairs.xlsx"
lotr_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions/lotr_freq_pairs.xlsx"
output_excel = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/tables/gift_freq_pairs.xlsx"
output_graph = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/graphs/gift_freq_pairs.png"

# === Load data ===
beo = pd.read_excel(beo_path)
lotr = pd.read_excel(lotr_path)

# === Normalize pair labels ===
replace_map = {
    "Good supernaturals": "G. supernat.",
    "Evil supernaturals": "E. supernat."
}
beo["pair"] = beo["pair"].replace(replace_map, regex=True)
lotr["pair"] = lotr["pair"].replace(replace_map, regex=True)

# === Calculate relative frequencies (%)
beo["rel_freq"] = (beo["absolute_frequency"] / beo["absolute_frequency"].sum()) * 100
lotr["rel_freq"] = (lotr["absolute_frequency"] / lotr["absolute_frequency"].sum()) * 100

# === Merge data ===
merged = pd.merge(
    beo[["pair", "absolute_frequency", "rel_freq"]],
    lotr[["pair", "absolute_frequency", "rel_freq"]],
    on="pair", how="outer", suffixes=("_beowulf", "_lotr")
).fillna(0)

# === Custom order (reversed)
custom_order = [
    "Rulers → Heroes",
    "Rulers → Rulers",
    "Heroes → Rulers",
    "Heroes → Heroes",
    "Rulers → Commoners",
    "Commoners → Rulers",
    "G. supernat. → Heroes",
    "Heroes → Commoners",
    "Commoners → Heroes",
    "G. supernat. → Commoners",
    "Rulers → G. supernat.",
    "E. supernat. → Rulers",
    "Heroes → G. supernat.",
    "Heroes → E. supernat.",
    "G. supernat. → G. supernat.",
    "E. supernat. → E. supernat."
][::-1]  # reversed

merged["pair"] = pd.Categorical(merged["pair"], categories=custom_order, ordered=True)
merged = merged.sort_values("pair")

# === Save table ===
export_df = merged.copy()
export_df.columns = ["Pair", "Beowulf (abs.)", "Beowulf (%)", "LOTR (abs.)", "LOTR (%)"]
export_df.to_excel(output_excel, index=False)
print(f"✅ Table saved to: {output_excel}")

# === Plot: side-by-side horizontal bar chart ===
bar_height = 0.4
y = np.arange(len(merged))

plt.figure(figsize=(10, max(6, 0.3 * len(merged))))

plt.barh(y - bar_height / 2, merged["rel_freq_lotr"], height=bar_height,
         color="steelblue", label="LOTR", edgecolor="black")
plt.barh(y + bar_height / 2, merged["rel_freq_beowulf"], height=bar_height,
         color="darkorange", label="Beowulf", edgecolor="black")

# Axes formatting
plt.yticks(y, merged["pair"], fontsize=11)
plt.ylabel("Pair (Giver Category → Recipient Category)", fontsize=14)

max_val = max(merged["rel_freq_beowulf"].max(), merged["rel_freq_lotr"].max())
x_max = min(100, (int(max_val // 5) + 2) * 5)
plt.xticks(range(0, x_max + 1, 5), fontsize=12)
plt.xlim(0, x_max)
plt.xlabel("Relative Frequency (%)", fontsize=14)
plt.title("Relative Frequency of Giver → Recipient Category Pairs", fontsize=16)

# Grid and lines
for x in range(5, x_max, 5):
    plt.axvline(x=x, linestyle="--", color="gray", linewidth=0.5)
plt.axvline(x=0, color="black", linewidth=0.6)

plt.legend()
plt.tight_layout()
plt.savefig(output_graph, dpi=300)
plt.close()
print(f"✅ Chart saved to: {output_graph}")
