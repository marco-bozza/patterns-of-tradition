import pandas as pd
import os

# Paths
data_dir = "D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/extractions"
output_freq = "D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/extractions"

os.makedirs(output_freq, exist_ok=True)

# Load event data
file_path = os.path.join(data_dir, "beowulf_complete_events.xlsx")
df = pd.read_excel(file_path)

# Normalize categories by removing (M) and (F)
df["singer_category"] = df["singer_category"].str.replace(r" \((M|F)\)", "", regex=True)

# Known text length for Beowulf
text_length = 17372

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
save_excel(freq_events, "beowulf_freq_events")

# Frequency of song content (based on unique events)
freq_song_content = df_unique.groupby("content").size().reset_index(name="absolute_frequency")
freq_song_content["relative_frequency"] = freq_song_content["absolute_frequency"] / len(df_unique)
save_excel(freq_song_content, "beowulf_freq_songs")

# Frequency of singer category (based on all events)
freq_singer = df.groupby("singer_category").size().reset_index(name="absolute_frequency")
freq_singer["relative_frequency"] = freq_singer["absolute_frequency"] / len(df)
save_excel(freq_singer, "beowulf_freq_singers")

# Frequency of hierarchical pairs (giver → recipient) (based on unique events)
df_unique["pair"] = df_unique["singer_category"] + " → " + df_unique["content"]
freq_pairs = df_unique.groupby("pair").size().reset_index(name="absolute_frequency")
freq_pairs["relative_frequency"] = freq_pairs["absolute_frequency"] / len(df_unique)
save_excel(freq_pairs, "beowulf_freq_pairs")

print("✅ Singing frequencies calculated and saved (10k tokens only for unique events)!")
