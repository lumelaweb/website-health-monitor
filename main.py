import streamlit as st
import openai
import pandas as pd

st.title("📊 Website Health Report Generator")

# Upload or simulate data
uploaded_file = st.file_uploader("Upload your GA4 data CSV")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data.head())

    if st.button("Generate GPT Summary"):
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        # Example: summarize the uploaded CSV
        prompt = f"Summarize key insights from this website data:\n{data.head().to_string()}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        st.subheader("💡 Insights")
        st.write(summary)
