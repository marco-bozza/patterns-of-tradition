import streamlit as st
import pandas as pd
import re
from modules.parse_text import extract_quotation


def clean_name(value):
    if pd.isna(value) or value == "-":
        return None
    return value.strip("[]")


def clean_category(cat):
    if pd.isna(cat):
        return ""
    return "[" + cat.split(" (")[0] + "]"


def display_gift_result(row, token_dict, show_categories, work):
    row_id = str(row['id']).replace(".", "_")
    toggle_key = f"toggle_details_gift_{row_id}_{row['n']}"

    giver = clean_name(row["giver_NE"]) if pd.notna(row["giver_NE"]) and row["giver_NE"] != "-" else clean_name(row["giver_NN"])
    gift = clean_name(row["gift_NN"])
    recipient = clean_name(row["recipient_NE"]) if pd.notna(row["recipient_NE"]) and row["recipient_NE"] != "-" else clean_name(row["recipient_NN"])

    giver_cat = clean_category(row["giver_category"]) if show_categories else ""
    gift_cat = clean_category(row["gift_category"]) if show_categories else ""
    rec_cat = clean_category(row["recipient_category"]) if show_categories else ""

    st.markdown(f"**{row['id']}.{row['n']}** {giver} {giver_cat} → {gift} {gift_cat} → {recipient} {rec_cat}")

    try:
        match = re.match(r"(w[\d\.]+).*?(w[\d\.]+)", str(row.get("quotation", "")))
        if match:
            start_id, end_id = match.group(1), match.group(2)
            quote_preview = extract_quotation(start_id, end_id, token_dict, work, preview=True)
            if quote_preview:
                st.markdown(f"*{quote_preview[:200]}...*")
            else:
                st.markdown("*[Preview unavailable]*")
        else:
            st.markdown("*[Preview unavailable]*")
    except Exception as e:
        st.markdown(f"*[Preview error: {e}]*")

    if st.toggle("Show details", key=toggle_key):
        st.markdown(f"**Giver:** {giver}")
        st.markdown(f"**Gift:** {gift}")
        st.markdown(f"**Recipient:** {recipient}")
        try:
            if match:
                full_quote = extract_quotation(start_id, end_id, token_dict, work, preview=False)
                st.markdown("**Full Quotation:**")
                st.text(full_quote)
            else:
                st.markdown("*[Quotation unavailable]*")
        except Exception as e:
            st.markdown(f"*[Error building quotation: {e}]*")

    st.markdown("---")


def display_singing_result(row, token_dict, show_categories=True, work="lotr"):
    row_id = str(row['id']).replace(".", "_")
    toggle_key = f"toggle_details_singing_{row_id}_{row['n']}"

    singer = clean_name(row["singer_NE"]) if pd.notna(row["singer_NE"]) and row["singer_NE"] != "-" else clean_name(row["singer_NN"])
    singer_cat = clean_category(row.get("singer_category")) if show_categories else ""
    content = row.get("content", "")

    st.markdown(f"**{row['id']}.{row['n']}** {singer} {singer_cat} → {content}")

    try:
        match = re.match(r"(w[\d\.]+).*?(w[\d\.]+)", str(row.get("quotation", "")))
        if match:
            start_id, end_id = match.group(1), match.group(2)
            quote_preview = extract_quotation(start_id, end_id, token_dict, work, preview=True)
            if quote_preview:
                st.markdown(f"*{quote_preview[:200]}...*")
            else:
                st.markdown("*[Preview unavailable]*")
        else:
            st.markdown("*[Preview unavailable]*")
    except Exception as e:
        st.markdown(f"*[Preview error: {e}]*")

    if st.toggle("Show details", key=toggle_key):
        st.markdown(f"**Singer:** {singer}")
        st.markdown(f"**Content:** {content}")
        try:
            if match:
                full_quote = extract_quotation(start_id, end_id, token_dict, work, preview=False)
                st.markdown("**Full Quotation:**")
                st.text(full_quote)
            else:
                st.markdown("*[Quotation unavailable]*")
        except Exception as e:
            st.markdown(f"*[Error building quotation: {e}]*")

    st.markdown("---")


def display_burial_result(row, token_dict, show_categories=True, work="lotr"):
    row_id = str(row['id']).replace(".", "_")
    toggle_key = f"toggle_details_burial_{row_id}_{row['n']}"

    deceased = clean_name(row["deceased_NE"]) if pd.notna(row["deceased_NE"]) and row["deceased_NE"] != "-" else clean_name(row["deceased_NN"])
    deceased_cat = clean_category(row['deceased_category']) if show_categories and pd.notna(row.get("deceased_category")) else ""

    burial_type = row.get("burialtype_NN", "")
    if burial_type == "-":
        burial_type = ""
    burial_cat = clean_category(row['burialtype_category']) if show_categories and pd.notna(row.get("burialtype_category")) and row['burialtype_category'] != "-" else ""

    burial_object = row.get("object_NN", "")
    if burial_object == "-":
        burial_object = ""
    object_cat = clean_category(row['object_category']) if show_categories and pd.notna(row.get("object_category")) and row['object_category'] != "-" else ""

    preview_line = f"**{row['id']}.{row['n']}** {deceased}"
    if deceased_cat:
        preview_line += f" {deceased_cat}"
    if burial_type:
        preview_line += f" → {burial_type}"
        if burial_cat:
            preview_line += f" {burial_cat}"
    if burial_object:
        preview_line += f" → {burial_object}"
        if object_cat:
            preview_line += f" {object_cat}"
    st.markdown(preview_line)

    try:
        match = re.match(r"(w[\d\.]+).*?(w[\d\.]+)", str(row.get("quotation", "")))
        if match:
            start_id, end_id = match.group(1), match.group(2)
            quote_preview = extract_quotation(start_id, end_id, token_dict, work, preview=True)
            if quote_preview:
                st.markdown(f"*{quote_preview[:200]}...*")
            else:
                st.markdown("*[Preview unavailable]*")
        else:
            st.markdown("*[Preview unavailable]*")
    except Exception as e:
        st.markdown(f"*[Preview error: {e}]*")

    if st.toggle("Show details", key=toggle_key):
        st.markdown(f"**Deceased:** {deceased}")
        st.markdown(f"**Burial Type:** {row.get('burialtype_NN', '')}")
        if pd.notna(row.get("object_NN")):
            st.markdown(f"**Object:** {row.get('object_NN', '')}")
        try:
            if match:
                full_quote = extract_quotation(start_id, end_id, token_dict, work, preview=False)
                st.markdown("**Full Quotation:**")
                st.text(full_quote)
            else:
                st.markdown("*[Quotation unavailable]*")
        except Exception as e:
            st.markdown(f"*[Error building quotation: {e}]*")

    st.markdown("---")
