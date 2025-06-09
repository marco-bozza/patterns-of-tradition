import pandas as pd
import os

# Paths
data_dir = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions"
output_freq = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions"

os.makedirs(output_freq, exist_ok=True)

# Load event data
file_path = os.path.join(data_dir, "lotr_complete_events.xlsx")
df = pd.read_excel(file_path)

# Normalize categories by removing (M) and (F)
df["giver_category"] = df["giver_category"].str.replace(r" \((M|F)\)", "", regex=True)
df["recipient_category"] = df["recipient_category"].str.replace(r" \((M|F)\)", "", regex=True)

# Known text length for LOTR
text_length = 467167

def save_excel(df, filename):
    path = os.path.join(output_freq, filename + ".xlsx")
    df.to_excel(path, index=False)
    print(f"✅ Saved: {path}")

# Filter unique events by ID
df_unique = df.drop_duplicates(subset="id", keep="first")

# Absolute frequency and relative frequency (per 10,000 tokens) of complete events
freq_events = pd.DataFrame({
    "absolute_frequency": [len(df_unique)],
    "relative_frequency_per_10k_tokens": [len(df_unique) / text_length * 10000]
})
save_excel(freq_events, "lotr_freq_events")

# Frequency of giver categories (based on unique events)
freq_giver = df_unique.groupby("giver_category").size().reset_index(name="absolute_frequency")
freq_giver["relative_frequency"] = freq_giver["absolute_frequency"] / len(df_unique)
save_excel(freq_giver, "lotr_freq_giver")

# Frequency of gift categories (based on all rows)
freq_gift = df.groupby("gift_category").size().reset_index(name="absolute_frequency")
freq_gift["relative_frequency"] = freq_gift["absolute_frequency"] / len(df)
save_excel(freq_gift, "lotr_freq_gift")

# Frequency of recipient categories (based on unique events)
freq_recipient = df_unique.groupby("recipient_category").size().reset_index(name="absolute_frequency")
freq_recipient["relative_frequency"] = freq_recipient["absolute_frequency"] / len(df_unique)
save_excel(freq_recipient, "lotr_freq_recipient")

# Frequency of hierarchical pairs (based on unique events)
df_unique["pair"] = df_unique["giver_category"] + " → " + df_unique["recipient_category"]
freq_pairs = df_unique.groupby("pair").size().reset_index(name="absolute_frequency")
freq_pairs["relative_frequency"] = freq_pairs["absolute_frequency"] / len(df_unique)
save_excel(freq_pairs, "lotr_freq_pairs")

print("✅ Frequencies calculated and saved (per 10k tokens only for events)!")
