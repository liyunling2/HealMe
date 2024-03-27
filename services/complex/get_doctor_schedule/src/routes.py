from flask import Blueprint, request
from typing import List
import httpx
import os
import asyncio
from utils import create_schedule

routes = Blueprint("get_doctor_schedule", __name__)

@routes.route("/hello", methods=["GET"])
async def hello():
    return { "message": "Hello, World!", "env_vars": dict(os.environ) }, 200

@routes.route("/", methods=["GET"])
async def get_doctor_schedule():
    # At any point 404 error
    args = request.args
    clinic_id = args.get("clinicID")

    if not clinic_id:
        return { "message": "no clinicID sent" }, 400

    client = httpx.AsyncClient()
    try:
        # get response data for each or raise error
        responses = await asyncio.gather(
            asyncio.create_task(get_doctor_profile_with_rating(client, args)),
            asyncio.create_task(get_blocked_slots(client, args)),
            asyncio.create_task(get_bookings(client, args))
        )
        response_data = [response.raise_for_status().json() for response in responses]

        return response_data
        return format_response(request.args, response_data), 200

    except httpx.HTTPStatusError as err:
        print("HTTP STATUS ERROR: ", err)
        print("Response data: ", err.response.json())
        print("Request url: ", err.request.url)
        return { "message": f"Request to {err.request.url} failed" }, 500
    
    except httpx.HTTPError as err:
        # print error
        print("ERROR: ", err)
        print("Request url: ", err.request.url)
        return { "message": f"Request to {err.request.url} failed" }, 500

    except Exception as err:
        print(err)
        return { "message": "Something went wrong." }, 500

    finally:
        await client.aclose()

def get_data_from_url(client, url, args):
    print("fetching from", url)
    clinic_id = args.get("clinicID")
    return client.get(f"{url}?clinicID={clinic_id}")

def get_doctor_profile_with_rating(client, args):
    url = os.environ.get("PROFILE_URL")
    return get_data_from_url(client, url + "/doctors", args)

def get_blocked_slots(client, args):
    url = os.environ.get("BLOCKED_SLOTS_URL")
    return get_data_from_url(client, url, args)

def get_bookings(client, args):
    url = os.environ.get("BOOKING_URL")
    return get_data_from_url(client, url, args)

def format_response(args, response_data: List[dict]):
    print("Response data: ", response_data)
    doctor_profile, blocked_slots, bookings = (res["data"] for res in response_data)
    
    response_data = {
        "date": args.get("date"),
        "doctorID": args.get("doctorID"),
        "clinicID": args.get("clinicID")
    } \
    | doctor_profile \
    | {"schedule": create_schedule(blocked_slots, bookings)}
    
    return response_data

    

    