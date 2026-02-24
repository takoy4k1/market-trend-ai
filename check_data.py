import pandas as pd

df = pd.read_csv("data/clean/AAPL_clean.csv")

print("=== SHAPE ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== FIRST 3 ROWS ===")
print(df.head(3))

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== PRICE STATS ===")
print(df["close_price"].describe())

print("\n=== DATE RANGE ===")
print(f"From: {df['date'].min()}")
print(f"To:   {df['date'].max()}")