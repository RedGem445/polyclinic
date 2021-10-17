import constrains
import data

import psycopg2
import random


conn = psycopg2.connect(
    dbname="polyclinic", user="polyclinic_admin", password="qwerty", host="127.0.0.1")
cur = conn.cursor()

# CREATE PERSONS tuples
for _ in range(constrains.PersonGenerator.NUM):
    sex = random.choice(data.SEXES)
    last_name = random.choice(data.LAST_NAMES[sex])
    first_name = random.choice(data.FIRST_NAMES[sex])
    patronymic = random.choice(data.PATRONYMICS[sex])
    cur.execute(
        "INSERT INTO person (sex, last_name, first_name, patronymic) VALUES (%s, %s, %s, %s)",
        (sex, last_name, first_name, patronymic)
    )

conn.commit()
cur.execute("SELECT MIN(id), MAX(id) from person;")
min_person_id, max_person_id = cur.fetchone()

# CREATE doctors tuples
persons_ids = set(range(min_person_id, max_person_id + 1))

doctors_ids = set(random.sample(persons_ids, constrains.DoctorGenerator.NUM))

for id in doctors_ids:
    cur.execute(
        "INSERT INTO doctor (person_id) VALUES (%s)",
        (id,)
    )

# CREATE patient tuples
patients_ids = random.sample(
    persons_ids - doctors_ids, constrains.PatientGenerator.NUM)

for id in patients_ids:
    cur.execute(
        "INSERT INTO patient (person_id) VALUES (%s)",
        (id,)
    )

conn.commit()

# CREATE patient_symptoms tuples
patients_with_symptoms = set(random.sample(
    patients_ids, constrains.PatientSymptopmsGenerator.NUM_DISTINCT_PATIENT))


for id in patients_with_symptoms:
    for _ in range(
        random.randint(
            constrains.PatientSymptopmsGenerator.MIN_NUM_PATIENT,
            constrains.PatientSymptopmsGenerator.MAX_NUM_PATIENT)
    ):
        symptom = random.choice(data.SYMPTOMS)
        cur.execute(
            "INSERT INTO patient_symptom (patient_id, symptom) VALUES (%s, %s)",
            (id, symptom,)
        )

conn.commit()

# CREATE diagnosis_name tuples
for name in data.DIAGNOSIS:
    cur.execute(
        "INSERT INTO diagnosis_name (name) VALUES (%s)",
        (name,)
    )

conn.commit()

# CREATE diagnosis tuples
patients_with_diagnosis = random.sample(
    patients_ids, constrains.DiagnosisGenerator.NUM_DISTINCT_PATIENT)

cur.execute("SELECT MIN(id), MAX(id) from diagnosis_name;")
min_diagnosis_name_id, max_diagnosis_name_id = cur.fetchone()
diagnosis_names = range(min_diagnosis_name_id, max_diagnosis_name_id + 1)

for patient_id in patients_with_diagnosis:

    k = random.randint(
        constrains.DiagnosisGenerator.MIN_NUM_PATIENT,
        constrains.DiagnosisGenerator.MAX_NUM_PATIENT)

    doctors = random.sample(doctors_ids, k)

    for i in range(k):
        name = random.choice(diagnosis_names)

        cur.execute(
            "INSERT INTO diagnosis (name_id, doctor_id, patient_id) VALUES (%s, %s, %s)",
            (name, doctors[i], patient_id,)
        )

conn.commit()
