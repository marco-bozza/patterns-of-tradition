import xml.etree.ElementTree as ET
import pandas as pd
import os

data_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/data"
output_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions"
os.makedirs(output_path, exist_ok=True)

xml_file = os.path.join(data_path, "lotr.xml")
tree = ET.parse(xml_file)
root = tree.getroot()

def get_token_id(token):
    return token.attrib.get('{http://www.w3.org/XML/1998/namespace}id', None)

# Map all tokens to their linear positions
all_tokens = root.findall('.//w')
token_id_to_position = {get_token_id(token): idx + 1 for idx, token in enumerate(all_tokens) if get_token_id(token)}

chapters = []
book_counter = 0

# Search for div elements with type="book" and within them find the chapters
for book_div in root.findall('.//div[@type="book"]'):
    book_counter += 1
    chapter_counter = 0
    for chapter_div in book_div.findall('.//div[@type="chapter"]'):
        chapter_counter += 1
        head = chapter_div.find('./head')
        chapter_name = head.text.strip() if head is not None else "Unnamed Chapter"
        first_token = chapter_div.find('.//w')
        if first_token is not None:
            token_id = get_token_id(first_token)
            token_number = token_id_to_position.get(token_id, None)
            if token_number:
                chapter_code = f"{book_counter}.{chapter_counter}"
                chapters.append({
                    'book_number': book_counter,
                    'chapter_number': chapter_counter,
                    'chapter_code': chapter_code,
                    'chapter_name': chapter_name,
                    'token_id': token_id,
                    'token_number': token_number
                })

df_chapters = pd.DataFrame(chapters)
output_file = os.path.join(output_path, "lotr_chapters.xlsx")
df_chapters.to_excel(output_file, index=False)

print(f"✅ Extracted {len(df_chapters)} chapters with numeric codes and saved to {output_file}")
