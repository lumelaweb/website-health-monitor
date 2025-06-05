import streamlit as st
import pandas as pd
import openai
import datetime

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

# ---- DATA UPLOAD ----
st.subheader("📁 Upload Monthly CSV Data")
uploaded_file = st.file_uploader("Upload your combined CSV file", type="csv")

data = None
if uploaded_file:
    # Preview raw contents for debugging
    uploaded_file.seek(0)
    st.text(uploaded_file.read(500).decode('utf-8', errors='replace'))
    uploaded_file.seek(0)  # Reset pointer

    try:
        data = pd.read_csv(uploaded_file)
    except Exception:
        try:
            uploaded_file.seek(0)
            data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        except Exception:
            try:
                uploaded_file.seek(0)
                data = pd.read_csv(uploaded_file, sep=';', engine='python')
            except Exception as e:
                st.error(f"❌ Could not parse CSV file: {e}")

    if data is not None:
        st.success("✅ Data uploaded successfully!")
        st.dataframe(data.head())

        if st.button("🧠 Generate GPT Summary"):
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                sample_data = data.head().to_string(index=False)

                prompt = f"""
You are a web analytics expert. This is a monthly performance report for a business named {business_name}.

Based on the following data:

{sample_data}

Please provide:
- 3 traffic or performance insights
- 1 issue or red flag
- 1 growth tip for next month

Use a warm, consultative tone that is easy to understand.
"""

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )

                summary = response.choices[0].message.content

                st.subheader("💡 AI-Generated Insights")
                st.markdown(summary)

                st.download_button(
                    label="📄 Download Summary",
                    data=summary,
                    file_name=f"{business_name}_Health_Report_{datetime.date.today()}.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ GPT-4 failed to generate summary: {e}")
    else:
        st.warning("Please upload a valid CSV file to continue.")

# ---- OPTIONAL NOT
