import psycopg2
import csv

conn = psycopg2.connect(
    dbname="ayush_icd_bridge",
    user="postgres",
    password="5227",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

with open('icd11_codes.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO icd11_codes (code, title, definition, chapter)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code) DO NOTHING;
        """, (row['code'], row['title'], row['definition'], row['chapter']))

conn.commit()
cur.close()
conn.close()
print("✅ ICD-11 codes loaded successfully.")
