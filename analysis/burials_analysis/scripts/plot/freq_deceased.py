import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Config paths ===
input_path = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/extractions"
output_graph_path = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/graphs/freq_deceased.png"
output_table_path = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/tables/freq_deceased.xlsx"

# === Load data ===
beowulf = pd.read_excel(f"{input_path}/beowulf_freq_deceased.xlsx")
lotr = pd.read_excel(f"{input_path}/lotr_freq_deceased.xlsx")

# === Normalize category names ===
rename_map = {
    "Evil supernaturals": "E. supernat."
}
beowulf["deceased_category"] = beowulf["deceased_category"].replace(rename_map)
lotr["deceased_category"] = lotr["deceased_category"].replace(rename_map)

# === Calculate relative frequencies ===
beowulf_total = beowulf["absolute_frequency"].sum()
lotr_total = lotr["absolute_frequency"].sum()
beowulf["relative_frequency"] = (beowulf["absolute_frequency"] / beowulf_total) * 100
lotr["relative_frequency"] = (lotr["absolute_frequency"] / lotr_total) * 100

# === Create merged comparison table ===
categories_order = ["Rulers", "Heroes", "E. supernat.", "Animals"]
all_categories = pd.DataFrame({"deceased_category": categories_order})

merged = all_categories.merge(
    beowulf[["deceased_category", "absolute_frequency", "relative_frequency"]],
    on="deceased_category", how="left"
).merge(
    lotr[["deceased_category", "absolute_frequency", "relative_frequency"]],
    on="deceased_category", how="left",
    suffixes=("_beowulf", "_lotr")
)

# === Save Excel table ===
merged.columns = ["Category", "Beowulf Abs.", "Beowulf Rel.", "LOTR Abs.", "LOTR Rel."]
merged.to_excel(output_table_path, index=False)

# === Plot grouped horizontal bar chart ===
bar_width = 0.4
y = np.arange(len(categories_order))[::-1]  # Reverse y-axis to get top-to-bottom order

plt.figure(figsize=(10, 6))
plt.barh(y + bar_width/2, merged["Beowulf Rel."], height=bar_width, label="Beowulf", color="darkorange", edgecolor="black")
plt.barh(y - bar_width/2, merged["LOTR Rel."], height=bar_width, label="LOTR", color="steelblue", edgecolor="black")

# Axis and labels
# Invert category labels to match bar position (top to bottom)
plt.yticks(np.arange(len(categories_order)), categories_order[::-1], fontsize=12)

# Dynamically set x-axis limit based on max value
max_val = max(merged["Beowulf Rel."].max(), merged["LOTR Rel."].max())
x_max = min(100, (int(max_val // 5) + 2) * 5)
plt.xticks(np.arange(0, x_max + 1, 5), fontsize=12)
plt.xlim(0, x_max)
plt.xlabel("Relative Frequency (%)", fontsize=14)
plt.ylabel("Deceased Category", fontsize=14)
plt.title("Relative Frequency of Deceased Categories in Burial Events", fontsize=16)

# Vertical reference lines every 5 units
for line in np.arange(5, 100, 5):
    plt.axvline(x=line, color="grey", linestyle="dashed", linewidth=0.5)

plt.axvline(x=0, color="black", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(output_graph_path, dpi=300)
plt.close()

print("✅ Chart and table successfully saved.")
