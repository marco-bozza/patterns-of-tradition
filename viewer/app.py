import streamlit as st
import pandas as pd
import os
import xml.etree.ElementTree as ET

from modules.parse_text import build_token_index
from modules.view_builder import display_gift_result, display_singing_result, display_burial_result

# Impostazioni iniziali
st.set_page_config(page_title="Annotation Viewer", layout="wide")

# Selezione testo e tema
st.sidebar.title("Settings")
text_labels = {"lotr": "The Lord of the Rings", "beowulf": "Beowulf"}
theme_labels = {"gift_giving": "Gift Giving", "singing": "Singing", "burials": "Burials"}

# Invertiamo i dizionari per usarli nel selectbox
text_options = {"The Lord of the Rings": "lotr", "Beowulf": "beowulf"}
theme_options = {"Gift Giving": "gift_giving", "Singing": "singing", "Burials": "burials"}

selected_text_label = st.sidebar.selectbox("Select text", list(text_options.keys()))
work = text_options[selected_text_label]

selected_theme_label = st.sidebar.selectbox("Select theme", list(theme_options.keys()))
theme = theme_options[selected_theme_label]

# Percorsi file
DATA_DIR = "data"
ANNOTATION_PATH = os.path.join(DATA_DIR, "annotations", f"{work}_{theme}.xlsx")
TEXT_PATH = os.path.join(DATA_DIR, "texts", f"{work}.xml")

# Caricamento file
df = pd.read_excel(ANNOTATION_PATH)
xml_tree = ET.parse(TEXT_PATH)
xml_root = xml_tree.getroot()
token_dict = build_token_index(xml_root)

# Filtri comuni
st.sidebar.title("Filters")
search_keyword = st.sidebar.text_input("Search keyword")
show_categories = st.sidebar.checkbox("Show categories", value=True)

# Filtro e visualizzazione per gift_giving
if theme == "gift_giving":
    def remove_gender(cat):
        if pd.isna(cat):
            return cat
        return cat.split(" (")[0]

    df["giver_category_clean"] = df["giver_category"].apply(remove_gender)
    df["recipient_category_clean"] = df["recipient_category"].apply(remove_gender)
    df["gift_category_clean"] = df["gift_category"].apply(remove_gender)

    if work == "lotr":
        giver_order = ["Rulers", "Heroes", "Good Supernaturals", "Evil Supernaturals", "Commoners"]
        recipient_order = ["Rulers", "Heroes", "Good Supernaturals", "Evil Supernaturals", "Commoners"]
        gift_order = ["Treasures", "Arms", "Hospitality", "Provisions", "Objects", "Transports", "Consorts"]
    else:
        giver_order = recipient_order = ["Rulers", "Heroes", "Commoners"]
        gift_order = ["Treasures", "Arms", "Hospitality", "Transports", "Consorts"]

    selected_giver_categories = st.sidebar.multiselect("Giver Categories", giver_order)
    selected_gift_categories = st.sidebar.multiselect("Gift Categories", gift_order)
    selected_recipient_categories = st.sidebar.multiselect("Recipient Categories", recipient_order)

    filtered_df = df.copy()
    if search_keyword:
        keyword = search_keyword.lower()
        mask = (
            df["giver_NE"].fillna("").str.lower().str.contains(keyword) |
            df["giver_NN"].fillna("").str.lower().str.contains(keyword) |
            df["gift_NN"].fillna("").str.lower().str.contains(keyword) |
            df["recipient_NE"].fillna("").str.lower().str.contains(keyword) |
            df["recipient_NN"].fillna("").str.lower().str.contains(keyword)
        )
        filtered_df = filtered_df[mask]

    if selected_giver_categories:
        filtered_df = filtered_df[filtered_df["giver_category_clean"].isin(selected_giver_categories)]
    if selected_recipient_categories:
        filtered_df = filtered_df[filtered_df["recipient_category_clean"].isin(selected_recipient_categories)]
    if selected_gift_categories:
        filtered_df = filtered_df[filtered_df["gift_category_clean"].isin(selected_gift_categories)]

elif theme == "singing":
    def remove_gender(cat):
        if pd.isna(cat):
            return cat
        return cat.split(" (")[0]

    df["singer_category_clean"] = df["singer_category"].apply(remove_gender)

    if work == "lotr":
        singer_order = ["Rulers", "Heroes", "Good Supernaturals", "Evil Supernaturals", "Commoners", "Poets"]
    else:
        singer_order = ["Rulers", "Heroes", "Commoners", "Poets"]

    content_order = ["Travel", "Feasting", "Nature", "Tales", "Lament", "War", "Myth", "Enchantment"]

    selected_singer_categories = st.sidebar.multiselect("Singer Categories", singer_order)
    selected_contents = st.sidebar.multiselect("Content Categories", content_order)

    filtered_df = df.copy()
    if search_keyword:
        keyword = search_keyword.lower()
        mask = (
            df["singer_NE"].fillna("").str.lower().str.contains(keyword) |
            df["singer_NN"].fillna("").str.lower().str.contains(keyword) |
            df["singer_quoted"].fillna("").str.lower().str.contains(keyword)
        )
        filtered_df = filtered_df[mask]

    if selected_singer_categories:
        filtered_df = filtered_df[filtered_df["singer_category_clean"].isin(selected_singer_categories)]
    if selected_contents:
        filtered_df = filtered_df[filtered_df["content"].isin(selected_contents)]

elif theme == "burials":
    def remove_gender(cat):
        if pd.isna(cat):
            return cat
        return cat.split(" (")[0]

    df["deceased_category_clean"] = df["deceased_category"].apply(remove_gender)
    df["burialtype_category_clean"] = df["burialtype_category"].apply(remove_gender)
    df["object_category_clean"] = df["object_category"].apply(remove_gender)

    df["deceased_clean"] = df["deceased_NE"].combine_first(df["deceased_NN"]).fillna("")
    df["burialtype_clean"] = df["burialtype_NN"].fillna("")
    df["object_clean"] = df["object_NN"].fillna("")

    if work == "lotr":
        deceased_order = ["Rulers", "Heroes", "Evil Supernaturals", "Animals"]
        burialtype_order = ["Mounds", "Graves", "Pyres", "Boats", "Heaps"]
        object_order = ["Treasures", "Arms"]
    else:
        deceased_order = ["Rulers", "Heroes"]
        burialtype_order = ["Mounds", "Graves", "Pyres", "Boats"]
        object_order = ["Treasures", "Arms"]

    selected_deceased_categories = st.sidebar.multiselect("Deceased Categories", deceased_order)
    selected_burialtype_categories = st.sidebar.multiselect("Burial Categories", burialtype_order)
    selected_object_categories = st.sidebar.multiselect("Object Categories", object_order)

    filtered_df = df.copy()

    if search_keyword:
        keyword = search_keyword.lower()
        mask = (
            df["deceased_NE"].fillna("").str.lower().str.contains(keyword) |
            df["deceased_NN"].fillna("").str.lower().str.contains(keyword) |
            df["burialtype_NN"].fillna("").str.lower().str.contains(keyword) |
            df["object_NN"].fillna("").str.lower().str.contains(keyword)
        )
        filtered_df = filtered_df[mask]

    if selected_deceased_categories:
        filtered_df = filtered_df[filtered_df["deceased_category_clean"].isin(selected_deceased_categories)]
    if selected_burialtype_categories:
        filtered_df = filtered_df[filtered_df["burialtype_category_clean"].isin(selected_burialtype_categories)]
    if selected_object_categories:
        filtered_df = filtered_df[filtered_df["object_category_clean"].isin(selected_object_categories)]

# Ordinamento e conteggio
filtered_df = filtered_df.sort_values(by=["id", "n"])
total_results = len(filtered_df)

# Titolo risultati
text_title = text_labels[work]
theme_title = theme_labels[theme]
st.markdown(f"## {text_title} – {theme_title}")
st.markdown(f"**Results found: {total_results}**")

# Sidebar: paginazione
results_per_page = st.sidebar.selectbox("Results per page", [10, 25, 50], index=0)
total_pages = (total_results - 1) // results_per_page + 1
page_number = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1)

start_idx = (page_number - 1) * results_per_page
end_idx = start_idx + results_per_page
page_df = filtered_df.iloc[start_idx:end_idx]

# Visualizzazione
for _, row in page_df.iterrows():
    if theme == "gift_giving":
        display_gift_result(row, token_dict, show_categories, work)
    elif theme == "singing":
        display_singing_result(row, token_dict, show_categories, work)
    elif theme == "burials":
        display_burial_result(row, token_dict, show_categories, work)
