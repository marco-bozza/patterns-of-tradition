import pandas as pd
import os

# Paths
data_dir = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/extractions"
output_freq = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/extractions"

os.makedirs(output_freq, exist_ok=True)

# Load event data
file_path = os.path.join(data_dir, "beowulf_complete_events.xlsx")
df = pd.read_excel(file_path)

# Normalize categories by removing (M) and (F)
df["deceased_category"] = df["deceased_category"].str.replace(r" \((M|F)\)", "", regex=True)

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

# Frequency of deceased categories (based on unique events)
freq_deceased = df_unique.groupby("deceased_category").size().reset_index(name="absolute_frequency")
freq_deceased["relative_frequency"] = freq_deceased["absolute_frequency"] / len(df_unique)
save_excel(freq_deceased, "beowulf_freq_deceased")

# Frequency of burialtypes (based on unique events)
freq_burialtype = df_unique.groupby("burialtype_category").size().reset_index(name="absolute_frequency")
freq_burialtype["relative_frequency"] = freq_burialtype["absolute_frequency"] / len(df_unique)
save_excel(freq_burialtype, "beowulf_freq_burialtypes")

# Frequency of objects (based on all events)
freq_objects = df.groupby("object_category").size().reset_index(name="absolute_frequency")
freq_objects["relative_frequency"] = freq_objects["absolute_frequency"] / len(df)
save_excel(freq_objects, "beowulf_freq_objects")

print("✅ Burials frequencies calculated and saved (per 10k tokens only for unique events)!")
