import pandas as pd
from src.config import (
    HIGH_VALUE_MULTIPLIER,
    ODD_HOURS_START,
    ODD_HOURS_END,
    VELOCITY_THRESHOLD_COUNT,
    VELOCITY_WINDOW_MINUTES,
    DOMESTIC_LOCATIONS
)

class AnomalyDetector:
    """
    Detects anomalies in transaction data based on a set of predefined rules.
    """

    def __init__(self, transactions_df: pd.DataFrame):
        """
        Initializes the detector with transaction data.
        
        Args:
            transactions_df (pd.DataFrame): DataFrame containing transaction records.
        """
        self.df = transactions_df.copy()

    def _detect_high_value(self) -> pd.Series:
        """Rule 1: Detects transactions with an unusually high amount."""
        return self.df['Amount'] > (self.df['AvgDailySpend'] * HIGH_VALUE_MULTIPLIER)

    def _detect_odd_hours(self) -> pd.Series:
        """Rule 2: Detects transactions occurring at unusual times."""
        return self.df['Timestamp'].dt.hour.between(ODD_HOURS_START, ODD_HOURS_END, inclusive='left')

    def _detect_location_mismatch(self) -> pd.Series:
        """Rule 3: Detects transactions from foreign locations."""
        return ~self.df['Location'].isin(DOMESTIC_LOCATIONS)

    def _detect_high_velocity(self) -> pd.Series:
        """Rule 4: Detects a high frequency of transactions in a short time."""
        # Sort by account and time to ensure correct windowing
        self.df = self.df.sort_values(by=['AccountID', 'Timestamp'])

        # CORRECTED LINE: Added on='Timestamp' to specify the time column for the window
        velocity_check = self.df.groupby('AccountID').rolling(
            f'{VELOCITY_WINDOW_MINUTES}min', on='Timestamp'
        ).count()['TransactionID'] # Counting on a non-time column is more robust

        # The result is a MultiIndex Series, we need to align it back to the original df index
        return velocity_check.reset_index(level=0, drop=True) > VELOCITY_THRESHOLD_COUNT

    def run_detection(self) -> pd.DataFrame:
        """
        Applies all anomaly detection rules and flags anomalous transactions.
        
        Returns:
            pd.DataFrame: A DataFrame containing only the anomalous transactions,
                          with a new 'AnomalyType' column.
        """
        print("🔍 Running anomaly detection rules...")
        
        # Apply each detection rule
        high_value_flags = self._detect_high_value()
        odd_hours_flags = self._detect_odd_hours()
        location_flags = self._detect_location_mismatch()
        velocity_flags = self._detect_high_velocity()

        # Combine flags into a dictionary
        anomaly_flags = {
            "High Value": high_value_flags,
            "Odd Hour": odd_hours_flags,
            "Foreign Location": location_flags,
            "High Velocity": velocity_flags,
        }

        # Create the 'AnomalyType' column by joining reasons for flagged transactions
        self.df['AnomalyType'] = 'None'
        for reason, flags in anomaly_flags.items():
            self.df.loc[flags, 'AnomalyType'] = self.df.loc[flags, 'AnomalyType'].apply(
                lambda x: f"{reason}" if x == 'None' else f"{x}, {reason}"
            )

        # Filter for rows that are flagged as anomalous
        anomalies_df = self.df[self.df['AnomalyType'] != 'None'].copy()
        
        print(f"✅ Detection complete. Found {len(anomalies_df)} anomalous transactions.")
        return anomalies_df