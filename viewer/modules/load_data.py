import os
import pandas as pd
import xml.etree.ElementTree as ET

# Define the base directory of the project (one level above this module)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_annotations(theme: str, work: str) -> pd.DataFrame:
    """
    Load the Excel file containing annotations for the given theme and work.
    """

    # Map the internal theme name to the actual file suffixes
    theme_file_map = {
        "gift_giving": "gifts",
        "singing": "songs",
        "burials": "burials"
    }

    filename = f"{work.lower()}_{theme_file_map[theme]}.xlsx"
    filepath = os.path.join(BASE_DIR, "data", "annotations", filename)
    print(f"Loading annotations from: {filepath}")  # optional debug message
    return pd.read_excel(filepath)

def load_xml(work: str) -> ET.Element:
    """
    Load and return the root element of the XML tree for the given work.
    """
    filename = f"{work.lower()}.xml"
    filepath = os.path.join(BASE_DIR, "data", "texts", filename)
    print(f"Loading XML from: {filepath}")  # optional debug message
    tree = ET.parse(filepath)
    return tree.getroot()
