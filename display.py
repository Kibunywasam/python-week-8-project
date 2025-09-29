
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from collections import Counter

# Set wide layout for better visualization
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# TITLE AND DESCRIPTION
st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Load cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\Users\\Wintham\\Desktop\\PLP\\python\\cord-19-sample.csv")
    return df

df = load_data()

# Ensure 'year' is integer 
df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
df = df.dropna(subset=['year'])  # Safety drop
df['year'] = df['year'].astype(int)

# Get actual min/max years from data
min_year_actual = int(df['year'].min())
max_year_actual = int(df['year'].max())

# Use slider, but adapt to real data range
# Default: (2020, 2021) 
year_range = st.slider(
    "Select year range",
    min_value=min_year_actual,
    max_value=max_year_actual,
    value=(max(2020, min_year_actual), min(2021, max_year_actual))
)

# Filter data based on selection
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Display context
st.write(f"Showing **{len(filtered_df):,} papers** published between {year_range[0]} and {year_range[1]}.")

# 1. PUBLICATIONS OVER TIME 
st.subheader("Publications Over Time")
year_counts = df['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots(figsize=(9, 4.5))
ax1.bar(year_counts.index, year_counts.values, color='lightgray', label='All years')
selected_years = [y for y in year_counts.index if year_range[0] <= y <= year_range[1]]
ax1.bar(selected_years, [year_counts[y] for y in selected_years], color='steelblue', label='Selected range')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# 2. TOP JOURNALS 
st.subheader("Top Publishing Journals")
journals_filtered = filtered_df[filtered_df['journal'] != 'Unknown']['journal']
top_journals = journals_filtered.value_counts().head(10)

if not top_journals.empty:
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax2, palette='viridis')
    ax2.set_xlabel("Number of Papers")
    ax2.set_ylabel("Journal")
    # Add value labels
    for i, v in enumerate(top_journals.values):
        ax2.text(v + 10, i, str(v), color='black', va='center')
    st.pyplot(fig2)
else:
    st.write("No journal data available for the selected year range.")



#  3. PAPER COUNTS BY SOURCE 
st.subheader("Distribution of Papers by Source")
source_counts = filtered_df['source_x'].value_counts()

if not source_counts.empty:
    fig4, ax4 = plt.subplots(figsize=(9, 5))
    bars = ax4.bar(source_counts.index, source_counts.values, color='teal')
    ax4.set_xlabel("Source")
    ax4.set_ylabel("Number of Papers")
    ax4.set_xticklabels(source_counts.index, rotation=45, ha='right')
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    # Add value labels on bars
    for bar in bars:
        ax4.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + max(source_counts.values)*0.01,
            f'{int(bar.get_height())}',
            ha='center', va='bottom', fontsize=9
        )
    st.pyplot(fig4)
    
    # Show top sources in text
    st.write("**Top sources:**")
    st.write(source_counts.head().to_dict())
else:
    st.write("No source data available.")

# 4. SAMPLE DATA TABLE 
st.subheader("Sample Papers")
sample_cols = ['title', 'journal', 'year', 'source_x', 'abstract_word_count']
st.dataframe(
    filtered_df[sample_cols].head(10),
    use_container_width=True,
    hide_index=True
)

# 5. WORD CLOUD OF TITLES 
st.subheader("Word Cloud of Paper Titles")
all_titles = ' '.join(filtered_df['title'].astype(str).str.lower())
all_titles_clean = re.sub(r'[^a-z\s]', ' ', all_titles)
words = all_titles_clean.split()

stop_words = {
    'the', 'and', 'of', 'a', 'in', 'to', 'for', 'on', 'with', 'by', 'an', 'as', 'is', 'are',
    'was', 'were', 'be', 'or', 'that', 'this', 'at', 'from', 'it', 'which', 'but', 'not',
    'have', 'has', 'had', 'been', 'will', 'would', 'could', 'should', 'may', 'might', 'can',
    'co', 'http', 'doi', 'org', 'preprint', 'review', 'article', 'paper', 'study', 'research',
    'covid', 'covid19', 'sars', 'cov', 'coronavirus', 'virus', 'viral', 'patients', 'cases'
}
filtered_words = [w for w in words if len(w) > 2 and w not in stop_words]

if filtered_words:
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        colormap='plasma',
        collocations=False
    ).generate(' '.join(filtered_words))
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.imshow(wordcloud, interpolation='bilinear')
    ax3.axis('off')
    st.pyplot(fig3)
else:
    st.write("Not enough title text to generate a word cloud.")

#  FOOTER 
st.markdown("---")
st.caption("Data: CORD-19 Research Dataset | App built with Streamlit")