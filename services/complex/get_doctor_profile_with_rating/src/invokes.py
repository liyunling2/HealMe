import os
import requests

PROFILE_URL = os.getenv('PROFILE_URL')
RATING_URL = os.getenv('RATING_URL')

def get_doctor_profile(doctor_id):
    response = requests.get(f"{PROFILE_URL}/doctors/{doctor_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_doctor_ratings(doctor_id):
    response = requests.get(f"{RATING_URL}/?doctorID={doctor_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
