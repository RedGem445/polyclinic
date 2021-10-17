class PersonGenerator:
    NUM = 1000


class DoctorGenerator:
    NUM = 50


class PatientGenerator:
    NUM = 700


class PatientSymptopmsGenerator:
    # number of tuples with equal patients ids
    MIN_NUM_PATIENT = 1
    MAX_NUM_PATIENT = 5

    NUM_DISTINCT_PATIENT = min(
        PatientGenerator.NUM - 400, PatientGenerator.NUM)


class DiagnosisGenerator:
    # number of tuples with equal patients ids
    NUM_DISTINCT_PATIENT = min(PatientGenerator.NUM - 50, PatientGenerator.NUM)
    MIN_NUM_PATIENT = 1
    MAX_NUM_PATIENT = 2
