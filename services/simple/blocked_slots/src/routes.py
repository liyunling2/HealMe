from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import BlockedSlot
from db import db
from utils import get_filtered_query_from_args

routes = Blueprint("blocked-slots", __name__)

@routes.route("/", methods=["POST"])
def add_blocked_slot():
    data = request.get_json()
    slot = BlockedSlot(**data)
    
    try:
        db.session.add(slot)
        db.session.commit()

    except IntegrityError:
        return {
            "message": "Slot already blocked"
        }, 400
    
    return {
        "message": "Slot created",
        "data": slot.json()
    }, 201

@routes.route("/", methods=["GET"])
def get_blocked_slots():
    args = request.args

    try:
        slots = get_filtered_query_from_args(args, BlockedSlot)
    except InvalidRequestError as e:
        return {
            "message": "Bad request: " + str(e)
        }, 400

    return {
        "data": [slot.json() for slot in slots]
    }