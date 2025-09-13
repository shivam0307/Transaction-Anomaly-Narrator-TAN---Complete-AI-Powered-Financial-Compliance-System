from src.data_loader import load_transactions
from src.anomaly_detector import AnomalyDetector
from src.narrative_generator import NarrativeGenerator
from src.report_generator import create_csv_report, PDFReportGenerator
from src.config import CSV_REPORT_FILENAME

def main():
    """
    Main pipeline to run the Transaction Anomaly Narrator.
    """
    print("🚀 Starting Transaction Anomaly Narrator (TAN) Pipeline...")
    
    # 1. Load Data
    transactions_df = load_transactions("data/input/synthetic_transactions.csv")
    if transactions_df is None:
        return

    # 2. Detect Anomalies
    detector = AnomalyDetector(transactions_df)
    anomalies_df = detector.run_detection()

    if anomalies_df.empty:
        print("✅ No anomalies found. Pipeline finished.")
        return

    # 3. Generate Narratives
    print("✍️ Generating narratives for detected anomalies...")
    narrator = NarrativeGenerator()
    anomalies_df['Narrative'] = anomalies_df.apply(
        lambda row: narrator.generate_narrative(row.to_dict()),
        axis=1
    )

    # 4. Generate Reports
    print("📊 Generating final reports...")
    
    # Generate summary CSV report
    final_report_df = anomalies_df[['TransactionID', 'AccountID', 'Timestamp', 'Amount', 'Location', 'AnomalyType', 'Narrative']]
    create_csv_report(final_report_df, CSV_REPORT_FILENAME)
    
    # Generate individual PDF reports
    pdf_reporter = PDFReportGenerator()
    for _, row in anomalies_df.iterrows():
        pdf_reporter.generate_report(row.to_dict())

    print("\n🎉 TAN Pipeline finished successfully!")
    print(f"➡️ Check the '{CSV_REPORT_FILENAME}' and PDF files in the 'data/reports/' directory.")

if __name__ == "__main__":
    main()