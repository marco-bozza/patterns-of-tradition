import pandas as pd
import xml.etree.ElementTree as ET
import re

def load_events(filepath_excel):
    """Load event annotations from the Excel file."""
    df = pd.read_excel(filepath_excel)
    return df

def count_tokens(filepath_xml):
    """Count the total number of <w> tokens in the XML file."""
    tree = ET.parse(filepath_xml)
    root = tree.getroot()
    tokens = root.findall(".//w")
    return len(tokens)

def extract_first_token(quotation_string):
    """Extract the first token identifier (e.g., 'w25.28.1') from the quotation column."""
    match = re.search(r'(w\d+\.\d+\.\d+)', quotation_string)
    if match:
        return match.group(1)
    else:
        return None

def token_to_position(token_id):
    """Convert token ID into a numeric position (e.g., w25.28.1 -> 25,28,1)."""
    parts = token_id[1:].split('.')
    return tuple(map(int, parts))

def prepare_dataframe(filepath_excel, filepath_xml):
    df = load_events(filepath_excel)
    total_tokens = count_tokens(filepath_xml)

    # Add a column with the first token and its relative position
    df['first_token'] = df['quotation'].apply(extract_first_token)

    # Sort tokens based on their position (useful for distributions)
    df['token_position'] = df['first_token'].apply(token_to_position)

    # Convert position into a linear index (approximation)
    df['token_linear'] = df['token_position'].apply(lambda x: x[0]*1_000_000 + x[1]*1_000 + x[2] if x else None)

    # Calculate relative position with respect to total tokens
    df['relative_position'] = df['token_linear'] / total_tokens

    return df, total_tokens

if __name__ == "__main__":
    excel_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/data/lotr_gifts.xlsx"
    xml_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/data/lotr.xml"

    df, total_tokens = prepare_dataframe(excel_path, xml_path)
    
    # Save output
    output_path = "D:/Archivio/Documenti/Tesi/Data/gift_giving_analysis/output/extractions/lotr_complete_events.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ Events extracted and saved! Total tokens in text: {total_tokens}")
