from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import BlockedSlot
from db import db
import traceback

routes = Blueprint("blocked-slots", __name__)

@routes.route("/", methods=["POST"])
def add_blocked_slot():
    try:
        data = request.get_json()
        slot = BlockedSlot(**data)

        if slot.slotNo < 1 or slot.slotNo > 24:
            return {
                "message": "Invalid slot no. Only slot nos betweeen 1 and 24 are allowed."
            }, 400
    
        db.session.add(slot)
        db.session.commit()

    except IntegrityError:
        return {
            "message": "Slot already blocked"
        }, 400

    except TypeError as e:
        return {
            "message": str(e)
        }, 400

    except Exception as e:
        traceback.print_exception(e)
        return {
            "message": str(e)
        }, 500
    
    return {
        "message": "Slot created",
        "data": slot.json()
    }, 201

@routes.route("/", methods=["GET"])
def get_blocked_slots():
    args = request.args
    try:
        slots = BlockedSlot.query.filter_by(**args).all()

    except InvalidRequestError as e:
        return {
            "message": "Bad request: " + str(e)
        }, 400

    return {
        "data": [slot.json() for slot in slots]
    }