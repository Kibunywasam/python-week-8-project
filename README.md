#  CORD-19 Research Explorer

A data science project exploring the CORD-19 (COVID-19 Open Research Dataset) to uncover trends in scientific publishing during the pandemic. This project includes data cleaning, exploratory analysis, visualizations, and an interactive Streamlit dashboard.

---

##  Overview

The CORD-19 dataset, released by the Allen Institute for AI and partners, contains over 200,000 scholarly articles related to coronaviruses. This project focuses on the metadata (titles, abstracts, publication dates, journals, etc.) to answer key questions such as:

- How did research output evolve over time?
- Which journals published the most COVID-19 research?
- What topics dominated paper titles?
- Where did the data originate (sources)?

The final deliverable is an interactive Streamlit web app that allows users to explore the data dynamically.

---

##  Project Structure

cord19-explorer/
├── README.md
├── cord-19-sample.csv       # Cleaned sample dataset (output from Colab) from metadata.csv
├── display.py                                                  # Streamlit application
└── colab notebook python-week-8-project.ipynb            # Colab analysis script


---

##  Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone or download this repository.
2. Install required packages:

```bash
pip install streamlit pandas matplotlib seaborn wordcloud


