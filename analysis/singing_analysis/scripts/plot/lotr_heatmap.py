import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === Load data ===
file_path = "D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/extractions/lotr_freq_pairs.xlsx"
df = pd.read_excel(file_path)

# Replace names
replace_map = {
    "Good supernaturals": "G. supernat.",
    "Evil supernaturals": "E. supernat.",
    "Myth": "Myth-Religion"
}

# Split pairs into giver and recipient
df[["singer", "song"]] = df["pair"].str.split(" → ", expand=True)
df["singer"] = df["singer"].replace(replace_map)
df["song"] = df["song"].replace(replace_map)

# === Category orders ===
singer_categories = ["Poets", "Heroes", "Rulers", "Commoners", "G. supernat.", "E. supernat."]
song_categories = ["Tales", "Lament", "Feasting", "Myth-Religion", "Nature", "War", "Travel", "Enchantment"]

# === Fill empty matrix ===
heatmap_data = pd.DataFrame(index=singer_categories, columns=song_categories, dtype=float).fillna(0)

# === Populate matrix with relative frequencies (x100 to convert to %)
for _, row in df.iterrows():
    singer = row["singer"]
    content = row["song"]
    freq = row["relative_frequency"] * 100
    if singer in singer_categories and content in song_categories:
        heatmap_data.loc[singer, content] = freq

# === Plot ===
plt.figure(figsize=(12, 8))
ax = sns.heatmap(
    heatmap_data,
    annot=heatmap_data.applymap(lambda x: f"{x:.1f}%" if x > 0 else ""),
    fmt="",
    cmap="Blues",
    linewidths=0.5,
    linecolor="lightgrey",
    square=True,
    cbar_kws={'label': 'Relative Frequency (%)'}
)

# === Labels ===
plt.xlabel("Content of the Song", fontsize=14)
plt.ylabel("Singer Category", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=12)
plt.yticks(rotation=0, fontsize=12)

# === Title and Colorbar ===
plt.title("Heatmap of Singing in The Lord of the Rings", fontsize=16, pad=20)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)
cbar.set_label("Relative Frequency (%)", fontsize=14)

# === Save ===
plt.tight_layout()
plt.savefig("D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/graphs/singing_lotr_heatmap.png", dpi=300)
plt.close()
