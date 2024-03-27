import requests

def get_doctor_profile(doctorID):
    # URL of the doctor profile microservice
    url = f"http://profile-service/doctors/{doctorID}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return None
    except requests.RequestException as e:
        print(f"Error calling profile service: {e}")
        return None

def get_doctor_ratings(doctorID):
    # URL of the rating microservice
    url = f"http://rating-service/doctors/{doctorID}/ratings"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return []
    except requests.RequestException as e:
        print(f"Error calling rating service: {e}")
        return []
