import pandas as pd
import xml.etree.ElementTree as ET

def get_token_positions(filepath_xml):
    print("🔎 Parsing XML...")
    tree = ET.parse(filepath_xml)
    root = tree.getroot()
    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}
    tokens = root.findall('.//tei:w', namespace)
    token_map = {token.attrib['{http://www.w3.org/XML/1998/namespace}id']: idx + 1 for idx, token in enumerate(tokens)}
    total_tokens = len(tokens)
    print(f"✅ Found {total_tokens} tokens in XML.")
    return token_map, total_tokens

def prepare_dataframe(filepath_excel, filepath_xml):
    df = pd.read_excel(filepath_excel)
    token_positions, total_tokens = get_token_positions(filepath_xml)

    def extract_first_token(quotation):
        return quotation.split()[0] if isinstance(quotation, str) else None

    df['first_token'] = df['quotation'].apply(extract_first_token)

    def token_to_position(token_id):
        return token_positions.get(token_id, None)

    df['token_position'] = df['first_token'].apply(token_to_position)
    df['token_position'] = df['token_position'].fillna(0).astype(int)
    return df, total_tokens

# === CONFIGURATION ===
text_name = "beowulf"
excel_path = f"D:/Archivio/Documenti/Tesi/Data/singing_analysis/data/{text_name}_songs.xlsx"
xml_path = f"D:/Archivio/Documenti/Tesi/Data/singing_analysis/data/{text_name}.xml"
output_path = f"D:/Archivio/Documenti/Tesi/Data/singing_analysis/output/extractions/{text_name}_complete_events.xlsx"

# === EXECUTION ===
df, total_tokens = prepare_dataframe(excel_path, xml_path)
df.to_excel(output_path, index=False)
print(f"✅ {text_name.upper()} events extracted and saved to {output_path}")
print(f"✅ Total tokens in {text_name.upper()}: {total_tokens}")
