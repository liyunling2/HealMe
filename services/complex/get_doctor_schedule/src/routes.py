from flask import Blueprint, request
from typing import List
import httpx
import asyncio
import os

routes = Blueprint("get_doctor_schedule", __name__)

@routes.route("/", methods=["GET"])
async def get_doctor_schedule():
    # At any point 404 error
    clinic_id = request.args.get("clinicID")

    if not clinic_id:
        return { "message": "no clinicID sent" }, 400

    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(
            get_doctor_profiles(client, clinic_id),
            get_clinic_blocked_slots(client, clinic_id),
            get_clinic_doctor_ratings(client, clinic_id),
            get_bookings(client, clinic_id)
        )
        
        try:
            # get response data for each or raise error
            response_data = [response.raise_for_status().json() for response in responses]

            return format_response(response_data), 200

        except httpx.HTTPStatusError as err:
            print(err.request.url)
            return { "message": "dumbass" }, 400

        except:
            return { "message": "Something went wrong." }, 500

# def get_data(client, base_url, url_path_fn, **kwargs):
#     clinic_id = kwargs.get("clinic_id")
#     url_path = url_path_fn(base_url, clinic_id)
#     return client.get(url_path)

def get_doctor_profiles(client, clinic_id):
    url = os.environ.get("PROFILE_URL")
    return client.get(f"{url}/doctors?clinicID={clinic_id}")

def get_clinic_blocked_slots(client, clinic_id):
    url = os.environ.get("BLOCKED_SLOTS_URL")
    return client.get(f"{url}?clinicID={clinic_id}")

def get_clinic_doctor_ratings(client, clinic_id):
    url = os.environ.get("RATING_URL")
    return client.get(f"{url}?clinicID={clinic_id}")

def get_bookings(client, clinic_id):
    url = os.environ.get("BOOKING_URL")
    return client.get(f"{url}?clinicID={clinic_id}")

def format_response(response_data: List[dict]):
    doctors, blocked_slots, ratings, bookings = response_data

    