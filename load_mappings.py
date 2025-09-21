import psycopg2

conn = psycopg2.connect(
    dbname="ayush_icd_bridge",
    user="postgres",
    password="5227",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Sample mappings between NAMASTE and ICD-11 codes
mappings = [
    ('AYU001', 'ICD001', 0.95, 'Strong clinical overlap'),
    ('AYU002', 'ICD002', 0.90, 'Metabolic similarity'),
    ('AYU003', 'ICD003', 0.85, 'Respiratory symptoms match'),
    ('AYU004', 'ICD004', 0.80, 'Digestive system correlation'),
    ('AYU005', 'ICD005', 0.88, 'Skin condition parallels')
]

for namaste_code, icd11_code, score, notes in mappings:
    cur.execute("""
        INSERT INTO code_mappings (namaste_code, icd11_code, confidence_score, notes)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (namaste_code, icd11_code, score, notes))

conn.commit()
cur.close()
conn.close()
print("✅ Code mappings inserted successfully.")
