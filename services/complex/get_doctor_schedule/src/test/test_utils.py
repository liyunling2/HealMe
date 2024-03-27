import os
import unittest
from unittest import mock
from src.utils import create_schedule, deep_mask
import httpx
import pytest
from src.routes import (get_bookings, get_blocked_slots,
                    get_clinic_doctor_ratings, get_doctor_profile_with_rating)

test_client = httpx.AsyncClient(
    transport=httpx.MockTransport(
        lambda request: httpx.Response(200, json={"message": "ok"}),
    )
)

@mock.patch.dict(os.environ, {"PROFILE_URL": "http://profile_url", "BLOCKED_SLOTS_URL": "http://blocked_slots_url", "RATING_URL": "http://rating_url", "BOOKING_URL": "http://booking_url"})
@pytest.mark.asyncio
async def test_get_doctor_profiles():
    response = await get_doctor_profile_with_rating(test_client, "clinic_id")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_create_schedule():
    blocked_slots = [
        {
            'id': "wow",
            'doctorID': "fake_doctor_id",
            'clinicID': "fake_clinic_id",
            'date': "2022-01-01",
            'slotNo': 1,
            'reason': "fake_reason"
        },
        {
            'id': "wow",
            'doctorID': "fake_doctor_id",
            'clinicID': "fake_clinic_id",
            'date': "2022-01-01",
            'slotNo': 5,
            'reason': "fake_reason"
        },
        {
            'id': "wow",
            'doctorID': "fake_doctor_id",
            'clinicID': "fake_clinic_id",
            'date': "2022-01-01",
            'slotNo': 2,
            'reason': "fake_reason"
        }
    ]

    bookings = [
        {
            "bookingID": "fake_booking_id",
            "patientID": "fake_patient_id",
            "doctorID": "fake_doctor_id",
            "clinicID": "fake_clinic_id",
            "date": "2022-01-01",
            "slotNo": 3,
            "bookingStatus": "fake_booking_status",
        },
        {
            "bookingID": "fake_booking_id",
            "patientID": "fake_patient_id",
            "doctorID": "fake_doctor_id",
            "clinicID": "fake_clinic_id",
            "date": "2022-01-01",
            "slotNo": 4,
            "bookingStatus": "fake_booking_status",
        }
    ]

    res = create_schedule(blocked_slots, bookings)
    
    assert res == [{
        "slotNo": 1,
        "type": "blocked_slot"
    }, {
        "slotNo": 2,
        "type": "blocked_slot"
    }, {
        "slotNo": 3,
        "type": "booking"
    }, {
        "slotNo": 4,
        "type": "booking"
    },
    {
        "slotNo": 5,
        "type": "blocked_slot"
    }]
    
def test_deep_mask():
    mask_dic = {
        "a": None,
        "c": {
            "d": None
        }
    }

    dic = {
        "a": 4,
        "b": 3,
        "c": {
            "d": 5,
            "e": 6
        }
    }

    res = deep_mask(dic, mask_dic)
    print(res)

    assert res == {
        "a": 4,
        "c": {
            "d": 5,
        }
    }
