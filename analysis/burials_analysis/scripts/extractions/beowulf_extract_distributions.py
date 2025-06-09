import pandas as pd
import xml.etree.ElementTree as ET
import os
import re

# Paths for Beowulf
data_dir = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/data"
xml_path = os.path.join(data_dir, "beowulf.xml")
events_path = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/extractions/beowulf_complete_events.xlsx"
output_dir = "D:/Archivio/Documenti/Tesi/Data/burials_analysis/output/extractions"
os.makedirs(output_dir, exist_ok=True)

# Parse XML and get token positions
print("🔎 Parsing XML...")
tree = ET.parse(xml_path)
root = tree.getroot()
all_tokens = root.findall(".//{http://www.tei-c.org/ns/1.0}w")

token_id_to_position = {}
for idx, token in enumerate(all_tokens, start=1):
    token_id = token.attrib.get('{http://www.w3.org/XML/1998/namespace}id')
    if token_id:
        token_id_to_position[token_id] = idx

print(f"✅ Found {len(token_id_to_position)} token IDs in XML.")

# Load events
df_events = pd.read_excel(events_path)

# Keep only the first occurrence of each unique event ID
df_events = df_events.drop_duplicates(subset="id", keep="first")

def get_linear_position(quotation):
    if isinstance(quotation, str):
        match = re.search(r'(w\d+\.\d+)', quotation)
        if match:
            token_id = match.group(1)
            return token_id_to_position.get(token_id, None)
    return None

df_events["linear_position"] = df_events["quotation"].apply(get_linear_position)
missing_positions = df_events["linear_position"].isna().sum()
print(f"⚠️ Events without position: {missing_positions}")

total_tokens = len(all_tokens)
df_events["block"] = (df_events["linear_position"] / total_tokens * 100).fillna(0).astype(int)

distribution = df_events.groupby("block").size().reset_index(name="number_of_events")
output_path = os.path.join(output_dir, "beowulf_distribution_events.xlsx")
distribution.to_excel(output_path, index=False)
print(f"✅ Distribution calculated and saved to {output_path}")
