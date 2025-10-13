# debug_yoyo.py
import pandas as pd

F = "users.csv"
target = "yoyo"

print("=== RAW FILE LINES CONTAINING username ===")
with open(F, "rb") as f:
    for i, raw in enumerate(f):
        if target.encode("utf-8") in raw:
            print("line", i, raw.rstrip())
print()

print("=== csv.reader view of matching line(s) ===")
import csv
with open(F, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if any(target == c or target == c.strip() for c in row):
            print("csv row", i, row)
print()

print("=== pandas read (raw strings) ===")
df = pd.read_csv(F, dtype=str, keep_default_na=False, encoding="utf-8")
print("dtypes:", df.dtypes.to_dict())
rows = df.loc[df['username'].astype(str).str.strip() == target]
print("rows (as dict):", rows.to_dict(orient='records'))

if not rows.empty:
    s = rows.iloc[0].get("score", "")
    print("repr(score):", repr(s))
    print("bytes:", s.encode('utf-8'))
