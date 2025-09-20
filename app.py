import time
import streamlit as st
import pandas as pd
from src.data_loader import load_transactions
from src.anomaly_detector import AnomalyDetector
from src.narrative_generator import NarrativeGenerator

st.set_page_config(page_title="Transaction Anomaly Narrator (TAN)", layout="wide")

st.title("🤖 Transaction Anomaly Narrator (TAN)")
st.caption("An AI-powered tool to detect and explain anomalies in financial transactions.")

# --- Session State Initialization ---
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None

# --- Main App Logic ---
uploaded_file = st.file_uploader("Upload your transactions CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Use a temporary file path for loading
        with open("temp_uploaded.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        transactions_df = load_transactions("temp_uploaded.csv")

        if transactions_df is not None:
            st.success(f"Successfully loaded {len(transactions_df)} transactions.")
            
            if st.button("🔍 Run Anomaly Detection", type="primary"):
                with st.spinner("Detecting anomalies and generating narratives... This may take a moment."):
                    # Detect anomalies
                    detector = AnomalyDetector(transactions_df)
                    anomalies_df = detector.run_detection()
                    
                    if not anomalies_df.empty:
                        # Generate narratives
                        narrator = NarrativeGenerator()
                        narratives = []
                        progress_bar = st.progress(0, text="Generating narratives...")
                        for i, row in enumerate(anomalies_df.to_dict('records')):
                            narratives.append(narrator.generate_narrative(row))
                            time.sleep(1) # Wait for 1 second between each API call
                            progress_bar.progress((i + 1) / len(anomalies_df), text=f"Generating narrative {i+1}/{len(anomalies_df)}")
                        anomalies_df['Narrative'] = narratives
                        progress_bar.empty() # Remove the progress bar when done
    
                        st.session_state.processed_data = anomalies_df
                    else:
                        st.session_state.processed_data = pd.DataFrame() # Empty df if no anomalies
                
                if st.session_state.processed_data.empty:
                    st.info("No anomalies were detected in the provided data.")
                else:
                    st.success(f"Processing complete! Found {len(st.session_state.processed_data)} anomalies.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- Display Results ---
if st.session_state.processed_data is not None:
    st.divider()
    st.subheader("Anomaly Detection Results")

    if not st.session_state.processed_data.empty:
        # Displayable columns
        display_cols = ['TransactionID', 'AccountID', 'Timestamp', 'Amount', 'Location', 'AnomalyType', 'Narrative']
        st.dataframe(st.session_state.processed_data[display_cols], width='stretch')
    else:
        # This message shows after a run that finds no anomalies
        st.write("No anomalies to display.")