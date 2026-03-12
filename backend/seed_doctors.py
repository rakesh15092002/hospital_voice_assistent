# seed_doctors.py — Doctors ko JSON se DB mein load karo
# Usage: python seed_doctors.py

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, create_tables
from sqlalchemy import text

create_tables()
db = SessionLocal()

# Load doctors from JSON
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "data", "doctors.json")

with open(json_path, "r") as f:
    doctors = json.load(f)

print(f"Found {len(doctors)} doctors in doctors.json")

# Create doctors table if not exists
db.execute(text("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        department_id INTEGER,
        floor TEXT,
        fee INTEGER,
        symptoms TEXT
    )
"""))
db.commit()

# Clear existing doctors
db.execute(text("DELETE FROM doctors"))
db.commit()

# Insert doctors
for doctor in doctors:
    db.execute(text("""
        INSERT INTO doctors (id, name, specialization, department, department_id, floor, fee, symptoms)
        VALUES (:id, :name, :specialization, :department, :department_id, :floor, :fee, :symptoms)
    """), {
        "id": doctor["id"],
        "name": doctor["name"],
        "specialization": doctor["specialization"],
        "department": doctor["department"],
        "department_id": doctor["department_id"],
        "floor": doctor["floor"],
        "fee": doctor["fee"],
        "symptoms": json.dumps(doctor["symptoms"])
    })

db.commit()
db.close()

print(f"✅ {len(doctors)} doctors added to DB successfully!")
for d in doctors:
    print(f"   Dr. {d['name']} — {d['specialization']}")