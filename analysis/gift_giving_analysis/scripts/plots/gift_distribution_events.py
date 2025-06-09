import pandas as pd
import matplotlib.pyplot as plt
import os

# === Paths ===
base_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis"
input_path = os.path.join(base_path, "output", "extractions")
output_table_path = os.path.join(base_path, "output", "tables", "gift_distribution_events.xlsx")
output_graph_path = os.path.join(base_path, "output", "graphs", "gift_distribution_events.png")

# Ensure output directories exist
os.makedirs(os.path.dirname(output_table_path), exist_ok=True)
os.makedirs(os.path.dirname(output_graph_path), exist_ok=True)

# === Load data ===
beowulf_df = pd.read_excel(os.path.join(input_path, "beowulf_distribution_events.xlsx"))
lotr_df = pd.read_excel(os.path.join(input_path, "lotr_distribution_events.xlsx"))

# === Create 10% bins ===
beowulf_df["larger_block"] = (beowulf_df["block"] / 10).astype(int) * 10
lotr_df["larger_block"] = (lotr_df["block"] / 10).astype(int) * 10

# === Aggregate number of events per bin ===
beowulf_grouped = beowulf_df.groupby("larger_block")["number_of_events"].sum().reset_index()
lotr_grouped = lotr_df.groupby("larger_block")["number_of_events"].sum().reset_index()

# === Calculate relative frequencies (%) ===
beowulf_grouped["rel_freq"] = (beowulf_grouped["number_of_events"] / beowulf_grouped["number_of_events"].sum()) * 100
lotr_grouped["rel_freq"] = (lotr_grouped["number_of_events"] / lotr_grouped["number_of_events"].sum()) * 100

# === Merge all values together ===
merged = pd.merge(beowulf_grouped, lotr_grouped, on="larger_block", how="outer", suffixes=("_beowulf", "_lotr")).fillna(0)
merged = merged.sort_values("larger_block")

# === Create human-readable block labels ===
merged["block"] = merged["larger_block"].astype(int).astype(str) + "-" + (merged["larger_block"] + 10).astype(int).astype(str) + "%"

# === Create and save table ===
final_df = merged[[
    "block",
    "number_of_events_beowulf", "rel_freq_beowulf",
    "number_of_events_lotr", "rel_freq_lotr"
]]
final_df.columns = ["Block", "Beowulf (abs.)", "Beowulf (%)", "LOTR (abs.)", "LOTR (%)"]
final_df.to_excel(output_table_path, index=False)
print(f"✅ Table saved to: {output_table_path}")

# === Plot relative frequency bar chart ===
x_labels = [str(i+1) for i in range(len(final_df))]  # da "1" a "10"
x = range(len(final_df))
bar_width = 0.4

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar([i - bar_width/2 for i in x], final_df["Beowulf (%)"], width=bar_width,
       label="Beowulf", color="darkorange", edgecolor="black")
ax.bar([i + bar_width/2 for i in x], final_df["LOTR (%)"], width=bar_width,
       label="LOTR", color="steelblue", edgecolor="black")

ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.set_xlabel("Textual Block Number (Each Representing 10% of the Total Tokens)", fontsize=14)
ax.set_ylabel("Relative Frequency (% of Total Gift-Giving Events)", fontsize=14)
ax.set_ylim(bottom=0)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.6)
ax.set_title("Distribution of Gift-Giving Events across Equal Sized Textual Blocks", fontsize=16)

# === Save chart ===
plt.tight_layout()
plt.savefig(output_graph_path, dpi=300)
plt.close()
print(f"✅ Chart saved to: {output_graph_path}")
