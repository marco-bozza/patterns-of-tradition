import xml.etree.ElementTree as ET
import pandas as pd
import os

data_path = "D:/Archivio/Documenti/Tesi/Data/singing_analysis/data"
output_path = "D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/extractions"
os.makedirs(output_path, exist_ok=True)

xml_file = os.path.join(data_path, "beowulf.xml")
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
tree = ET.parse(xml_file)
root = tree.getroot()

def get_token_id(token):
    return token.attrib.get('{http://www.w3.org/XML/1998/namespace}id', None)

all_tokens = root.findall('.//tei:w', ns)
token_id_to_position = {get_token_id(token): idx + 1 for idx, token in enumerate(all_tokens) if get_token_id(token)}

chapters = []

for div in root.findall('.//tei:div[@n]', ns):
    chapter_number = div.attrib['n']
    first_token = div.find('.//tei:w', ns)
    if first_token is not None:
        token_id = get_token_id(first_token)
        token_number = token_id_to_position.get(token_id, None)
        chapters.append({
            'chapter_number': chapter_number,
            'token_id': token_id,
            'token_number': token_number
        })
    else:
        print(f"⚠️ Warning: No token found in chapter {chapter_number}")

df_chapters = pd.DataFrame(chapters)
output_file = os.path.join(output_path, "beowulf_chapters.xlsx")
df_chapters.to_excel(output_file, index=False)

print(f"✅ Extracted {len(df_chapters)} chapters from Beowulf and saved to {output_file}")
