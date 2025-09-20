import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

# --- Configuration ---
NUM_RECORDS = 1050
ACCOUNTS_TO_CREATE = 200
START_DATE = datetime(2025, 8, 20)
END_DATE = datetime(2025, 9, 20)

# --- Initialize Faker for realistic data ---
fake = Faker()

# --- Lists for generating varied data ---
MERCHANTS = [
    'Amazon', 'Walmart', 'Starbucks', 'Apple Store', 'ExxonMobil', 'Costco', 'Netflix',
    'Delta Airlines', 'Uber', 'Lyft', 'Whole Foods', 'Target', 'Best Buy', 'Home Depot'
]
TRANSACTION_TYPES = ['Card', 'Online', 'ATM', 'Transfer']
DOMESTIC_LOCATIONS = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
FOREIGN_LOCATIONS = ['London', 'Tokyo', 'Paris', 'Sydney', 'Hong Kong', 'Singapore', 'Dubai', 'Moscow', 'Mexico City', 'Toronto']

# --- Generate a base set of accounts for consistency ---
accounts = []
for i in range(ACCOUNTS_TO_CREATE):
    accounts.append({
        'AccountID': f'ACC{1000 + i}',
        'AccountHistoryDays': random.randint(30, 1500),
        'AvgDailySpend': round(random.uniform(50, 800), 2)
    })

print(f"Generating {NUM_RECORDS} transactions for {ACCOUNTS_TO_CREATE} accounts...")

# --- Main loop to generate transaction records ---
transactions = []
for i in range(NUM_RECORDS):
    account = random.choice(accounts)
    
    # Generate a normal-looking amount
    amount = round(account['AvgDailySpend'] * random.uniform(0.1, 2.5), 2)
    if amount < 5.0: amount = round(random.uniform(5, 50), 2)

    # Generate a random timestamp
    random_seconds = random.randint(0, int((END_DATE - START_DATE).total_seconds()))
    timestamp = START_DATE + timedelta(seconds=random_seconds)
    
    transactions.append({
        'TransactionID': f'TXN{10000 + i}',
        'AccountID': account['AccountID'],
        'Timestamp': timestamp,
        'Amount': amount,
        'Merchant': random.choice(MERCHANTS),
        'TransactionType': random.choice(TRANSACTION_TYPES),
        'Location': random.choice(DOMESTIC_LOCATIONS),
        'AccountHistoryDays': account['AccountHistoryDays'],
        'AvgDailySpend': account['AvgDailySpend']
    })

df = pd.DataFrame(transactions)

print("Injecting anomalies into the dataset...")

# --- Inject Anomalies ---

# 1. High Value Anomalies (15 records)
high_value_indices = df.sample(n=15).index
for idx in high_value_indices:
    avg_spend = df.loc[idx, 'AvgDailySpend']
    df.loc[idx, 'Amount'] = round(avg_spend * random.uniform(15, 40), 2)
    df.loc[idx, 'Merchant'] = fake.company() + " Inc." # Make merchant look more unique

# 2. Odd Hour Anomalies (15 records, avoiding overlap)
remaining_indices = df.index.difference(high_value_indices)
odd_hour_indices = pd.Series(remaining_indices).sample(n=15)
for idx in odd_hour_indices:
    current_ts = df.loc[idx, 'Timestamp']
    # Set hour to be between 1 AM and 4 AM
    odd_hour_ts = current_ts.replace(hour=random.randint(1, 4))
    df.loc[idx, 'Timestamp'] = odd_hour_ts

# 3. Foreign Location Anomalies (15 records)
remaining_indices = df.index.difference(high_value_indices).difference(odd_hour_indices)
foreign_loc_indices = pd.Series(remaining_indices).sample(n=15)
for idx in foreign_loc_indices:
    df.loc[idx, 'Location'] = random.choice(FOREIGN_LOCATIONS)

# 4. High Velocity Anomalies (4 clusters of 5 transactions each = 20 records)
remaining_indices = df.index.difference(high_value_indices).difference(odd_hour_indices).difference(foreign_loc_indices)
for i in range(4): # Create 4 clusters
    account = random.choice(accounts)
    start_time = START_DATE + timedelta(seconds=random.randint(0, int((END_DATE - START_DATE).total_seconds()) - 600))
    
    velocity_indices = pd.Series(remaining_indices).sample(n=5)
    remaining_indices = remaining_indices.difference(velocity_indices)
    
    for j, idx in enumerate(velocity_indices):
        df.loc[idx, 'AccountID'] = account['AccountID']
        df.loc[idx, 'Timestamp'] = start_time + timedelta(minutes=j*2) # Transactions 2 mins apart
        df.loc[idx, 'Location'] = fake.city() # Vary the city slightly

# 5. Combined Anomaly (High Value + Odd Hour + Foreign, 3 records)
remaining_indices = df.index.difference(high_value_indices).difference(odd_hour_indices).difference(foreign_loc_indices)
combo_indices = pd.Series(remaining_indices).sample(n=3)
for idx in combo_indices:
    avg_spend = df.loc[idx, 'AvgDailySpend']
    df.loc[idx, 'Amount'] = round(avg_spend * random.uniform(20, 50), 2)
    current_ts = df.loc[idx, 'Timestamp']
    df.loc[idx, 'Timestamp'] = current_ts.replace(hour=random.randint(1, 4))
    df.loc[idx, 'Location'] = random.choice(FOREIGN_LOCATIONS)

# --- Finalize and Save ---
# Shuffle the dataframe so anomalies are not clustered
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
output_filename = 'presentation_transactions.csv'
df.to_csv(output_filename, index=False)

print(f"\n✅ Success! {len(df)} records saved to '{output_filename}'.")
print("The file contains a mix of normal transactions and injected anomalies.")