import psycopg2
import csv

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="ayush_icd_bridge",
    user="postgres",
    password="5227",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Load NAMASTE codes from CSV
with open('namaste_codes.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO namaste_codes (code, name, description, category)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code) DO NOTHING;
        """, (row['code'], row['name'], row['description'], row['category']))

conn.commit()
cur.close()
conn.close()
print("NAMASTE codes loaded successfully.")
