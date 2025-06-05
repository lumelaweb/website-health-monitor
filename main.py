import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

# ---- PAGE SETUP ----
st.set_page_config(page_title="Website Health Monitor", layout="centered")
st.title("📊 Website Health Monitor")
st.markdown("""
Upload your monthly website data from **Google Analytics, Search Console, ConvertKit**, or **Clarity**  
to receive a summarized AI-powered insight report + growth tip for your business.
""")

# ---- BUSINESS SELECTION ----
business_name = st.selectbox(
    "Select your business/client:",
    ["-- Select --", "LumelaWeb", "Client A", "Client B", "Other"]
)

# ---- CSV PARSER FUNCTION ----
def try_parse_csv(file):
    try:
        file.seek(0)
        return pd.read_csv(file)
    except:
        pass
    t
