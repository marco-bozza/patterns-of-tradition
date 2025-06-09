from collections import defaultdict
from typing import Dict
import xml.etree.ElementTree as ET

def build_token_index(xml_root: ET.Element) -> Dict[str, Dict[str, str]]:
    """
    Builds a dictionary of tokens from the XML root.
    Each token ID maps to its text and its XML element.
    """
    token_dict = {}
    for elem in xml_root.iter():
        if elem.tag.endswith("w"):
            token_id = elem.attrib.get("xml:id") or elem.attrib.get("{http://www.w3.org/XML/1998/namespace}id")
            if token_id:
                token_dict[token_id] = {
                    "text": elem.text.strip() if elem.text else "",
                    "element": elem
                }
    return token_dict

def extract_quotation(start_id: str, end_id: str, token_dict: Dict[str, Dict[str, str]], work: str, preview=False) -> str:
    """
    Extracts a quotation from token_dict using start and end token IDs.
    Respects line breaks and formats the quotation with line numbers.
    """

    def token_sort_key(token_id: str):
        parts = token_id.lstrip("w").split(".")
        return tuple(int(p) for p in parts)

    try:
        lines = defaultdict(list)
        current_page = None

        # Get page of start_id for LOTR
        start_parts = start_id.lstrip("w").split(".")
        start_page = int(start_parts[0]) if work == "lotr" else None

        for token_id, data in token_dict.items():
            parts = token_id.lstrip("w").split(".")
            
            # Skip invalid token IDs
            if (work == "lotr" and len(parts) != 3) or (work == "beowulf" and len(parts) != 2):
                continue

            # Check range inclusion
            if not (token_sort_key(start_id) <= token_sort_key(token_id) <= token_sort_key(end_id)):
                continue

            # Group tokens by line
            if work == "lotr":
                page = int(parts[0])
                line = int(parts[1])
                if page != start_page:
                    continue  # Skip tokens from other pages
                key = (page, line)
                current_page = page
            else:  # beowulf
                line = int(parts[0])
                key = (line,)

            lines[key].append(data["text"])

        # Format output
        output = []
        for key in sorted(lines.keys()):
            if work == "lotr":
                _, line = key
                line_str = f"{line} | {' '.join(lines[key])}"
            else:
                (line,) = key
                line_str = f"{line} | {' '.join(lines[key])}"
            output.append(line_str)

        if preview:
            # Mostra solo la prima riga del risultato
            return ' '.join(lines[sorted(lines.keys())[0]]) + "..."

        if work == "lotr":
            return f"Page {current_page}\n\n" + "\n".join(output)
        else:
            return "\n".join(output)

    except Exception as e:
        return f"[Error building quotation: {str(e)}]"
