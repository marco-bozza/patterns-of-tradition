import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# Define paths
base_path = "D:/Archivio/Documenti/Tesi/Data/singing_analysis"
data_path = os.path.join(base_path, "output", "extractions", "lotr_distribution_events.xlsx")
chapters_path = os.path.join(base_path, "output", "extractions", "lotr_chapters.xlsx")
output_folder = os.path.join(base_path, "output", "graphs")
output_path = os.path.join(output_folder, "songs_lotr_distribution_events.png")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load data
df = pd.read_excel(data_path)
chapters_df = pd.read_excel(chapters_path)

# Chapter positions
total_tokens = 467167  
chapter_positions = chapters_df["token_number"].dropna().astype(int) / total_tokens * 100
chapter_labels = chapters_df["chapter_code"]

# Create plot
fig, ax = plt.subplots(figsize=(20, 6))

# Plot bars aligned to the left
ax.bar(df["block"], df["number_of_events"], width=1.0, color="steelblue", edgecolor="black", alpha=0.8, align='edge')

# Axis settings
ax.set_xlabel("Textual Block Number (Each Representing 1% of the Total Tokens)", fontsize=14)
ax.set_ylabel("Total Number of Singing Events", fontsize=14)
num_blocks = df["block"].max()
# Tick principali ogni 5
ax.set_xticks(range(0, 101, 5))
ax.set_xticklabels([str(i) for i in range(0, 101, 5)])

# Tick secondari ogni 1 (senza etichette)
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.tick_params(axis='x', which='minor', length=3, color='gray')  # puoi personalizzare lunghezza e colore

ax.set_yticks(range(0, df["number_of_events"].max() + 2, 1))
ax.set_xlim(0, 100)
ax.set_ylim(0, df["number_of_events"].max() + 2)
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
ax.set_title("Distribution of The Lord of the Rings Singing Events across Equal Sized Textual Blocks", fontsize=16)

# Chapter lines and smaller labels
for pos, label in zip(chapter_positions, chapter_labels):
    ax.axvline(x=pos, color="red", linestyle="dotted", linewidth=1.2, alpha=0.7)
    ax.text(pos, df["number_of_events"].max() + 0.5, label, rotation=90, verticalalignment="top", fontsize=8, color="darkred")

plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.close()

print(f"✅ Saved updated plot: {output_path}")
