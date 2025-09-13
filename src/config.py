import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- LLM Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Anomaly Detection Thresholds ---

# High Value Anomaly: Flag transactions where the amount is > X times the account's average daily spend.
HIGH_VALUE_MULTIPLIER = 10.0

# Odd Hours Anomaly: Define the window for "odd hours" (e.g., 1 AM to 5 AM)
ODD_HOURS_START = 1
ODD_HOURS_END = 5

# Velocity Anomaly: Flag if an account has more than X transactions in a Y-minute window.
VELOCITY_THRESHOLD_COUNT = 4
VELOCITY_WINDOW_MINUTES = 10

# Location Anomaly: For this POC, we'll assume the account's home country is the US.
# Any transaction outside this list is considered a foreign mismatch.
DOMESTIC_LOCATIONS = ["New York", "Chicago", "Miami", "Internet"]

# --- Reporting Configuration ---
REPORTS_DIR = "data/reports"
CSV_REPORT_FILENAME = "anomaly_report.csv"