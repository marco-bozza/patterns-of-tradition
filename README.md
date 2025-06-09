# Patterns of Tradition
**A Digital Philological Analysis of *Beowulf* and *The Lord of the Rings***

This repository contains the data and code developed for the thesis Patterns of Tradition: A Digital Philological Analysis of Beowulf and The Lord of the Rings. It includes the XML-encoded texts, annotated datasets, Python scripts for data analysis, and the source code for the Streamlit-based corpus viewer.
⚠️ Please note: Due to copyright restrictions, the XML file of The Lord of the Rings is not included. However, the annotated datasets and all related scripts are fully provided to ensure transparency and reproducibility.

## 📁 Repository Structure

```
patterns-of-tradition/
│
├── data/                  # XML corpora and annotated Excel datasets
│   ├── beowulf.xml
│   ├── beowulf_gifts.xlsx
│   └── ...
│
├── analysis/              # Python scripts for data extraction and visualization
│   ├── burial_analysis
│   ├── gift_giving_analysis
│   └── singing_analysis
│
├── viewer/                # Streamlit app for exploring annotated data
│   ├── app.py
│   ├── utils
│   └── ...
│
└── README.md              # This file
```

## 🛠️ Requirements

- Python 3.9 or higher
- Packages:
  - `pandas`
  - `matplotlib`
  - `openpyxl`
  - `streamlit`

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## ▶️ How to Use

### 1. **Explore the XML and annotation data**
You can find all source files under the `data/` directory:
- XML-encoded texts for *Beowulf*
- Excel files with manually annotated events on gift-giving, singing, and burials

### 2. **Run data analysis scripts**
Use the Python scripts in the `analysis/` folder to:
- Extract event frequencies and categories
- Generate comparative graphs
- Perform both quantitative and qualitative inspections

Example:

```bash
python analysis/calculate_frequencies.py
```

The outputs (tables and plots) will be saved in an `output/` folder.

### 3. **Launch the corpus viewer**
To interactively explore the annotated data with filters and full-text quotations:

```bash
cd viewer
streamlit run app.py
```

This will open the viewer in your browser, allowing you to:
- Browse events by text and motif
- Filter by category or keyword
- View contextual quotations and structured metadata

---

## 📖 License
This project is released under the MIT License.

## 👤 Author
Marco Bozza — 2025 Master's Thesis in Scienze del Linguaggio  
Università Ca' Foscari Venezia
