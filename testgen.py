import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- UI SETUP ---
st.set_page_config(page_title="EE Smart Grid Analyzer", layout="wide")
st.title("⚡ GridSense AI")
st.subheader("Automated Anomaly Detection for Electrical Engineers")

# --- INITIALIZATION ---
# Using Streamlit Secrets for security (No hardcoded keys!)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Key not found. Please set GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# --- MAIN LOGIC ---
st.write("### 1. Upload or Load Data")
uploaded_file = st.file_uploader("Upload your sensor/grid CSV data", type=["csv"])

# Sample Data Feature
if st.button("Load Sample Data for Testing"):
    # Create a dummy CSV file in memory for the demo
    data = {
        "Timestamp": ["08:00", "09:00", "10:00", "11:00"],
        "Power_KW": [45.2, 48.5, 120.5, 47.1],
        "Voltage_V": [230, 229, 245, 231]
    }
    df = pd.DataFrame(data)
    st.session_state['df'] = df
    st.success("Sample data loaded!")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state['df'] = df

if 'df' in st.session_state:
    df = st.session_state['df']
    st.write("### Data Preview")
    st.dataframe(df.head())

    if st.button("Analyze Data with AI"):
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            data_summary = df.head(10).to_string()
            prompt = f"You are a Senior EE. Analyze this data snapshot: {data_summary}. Identify grid inefficiencies and anomalies."
            
            with st.spinner("Analyzing..."):
                response = model.generate_content(prompt)
                st.write("### AI Analysis Results")
                st.info(response.text)
                st.download_button("Download Report", response.text, file_name="analysis.txt")
        except Exception as e:
            st.error(f"Error: {e}")

