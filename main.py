from fastapi import FastAPI
import psycopg2
import json

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        dbname="ayush_icd_bridge",
        user="postgres",
        password="5227",
        host="localhost",
        port="5432"
    )

@app.get("/map/{namaste_code}")
def get_mapping(namaste_code: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT icd11_code, confidence_score, notes
        FROM code_mappings
        WHERE namaste_code = %s
    """, (namaste_code,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {
            "icd11_code": result[0],
            "confidence_score": result[1],
            "notes": result[2]
        }
    return {"error": "Mapping not found"}
