import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from src.config import REPORTS_DIR

def create_csv_report(anomalies_df: pd.DataFrame, filename: str):
    """Saves the final DataFrame of anomalies to a CSV file."""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        
    file_path = os.path.join(REPORTS_DIR, filename)
    anomalies_df.to_csv(file_path, index=False)
    print(f"📄 CSV report saved to: {file_path}")

class PDFReportGenerator:
    """Generates a detailed PDF report for a single anomaly."""
    
    def generate_report(self, anomaly_data: dict):
        """Creates and saves a PDF report for one transaction."""
        
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)

        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Transaction Anomaly Incident Report", 0, 1, 'C')
        pdf.ln(10)
        
        # --- Metadata ---
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 8, "Report Generated:", 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 1)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 8, "Transaction ID:", 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, str(anomaly_data['TransactionID']), 0, 1)

        pdf.set_font("Arial", 'B', 10)
        pdf.cell(50, 8, "Account ID:", 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, str(anomaly_data['AccountID']), 0, 1)
        pdf.ln(5)

        # --- Details Table ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Transaction Details", 0, 1)
        
        details = {
            "Timestamp": anomaly_data['Timestamp'].strftime('%Y-%m-%d %H:%M:%S Z'),
            "Amount": f"${anomaly_data['Amount']:,.2f}",
            "Merchant": str(anomaly_data['Merchant']),
            "Location": str(anomaly_data['Location']),
            "Account Avg. Daily Spend": f"${anomaly_data['AvgDailySpend']:,.2f}",
        }
        
        for key, value in details.items():
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(60, 8, f"{key}:", 0, 0)
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 8, value, 0, 1)
        pdf.ln(5)

        # --- Anomaly Analysis ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Anomaly Analysis", 0, 1)
        
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(60, 8, "Detected Anomaly Types:", 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(220, 50, 50) # Red color for emphasis
        pdf.cell(0, 8, str(anomaly_data['AnomalyType']), 0, 1)
        pdf.set_text_color(0, 0, 0) # Reset color
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, "Generated Narrative:", 0, 1)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 6, anomaly_data['Narrative'])
        pdf.ln(10)

        # --- Footer ---
        pdf.set_y(-25)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "This is an auto-generated report by the Transaction Anomaly Narrator (TAN).", 0, 0, 'C')

        # --- Save File ---
        file_path = os.path.join(REPORTS_DIR, f"INCIDENT_{anomaly_data['TransactionID']}.pdf")
        pdf.output(file_path)
        print(f"📝 PDF report generated for {anomaly_data['TransactionID']}")