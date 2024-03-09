from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
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

    slots = get_filtered_query_from_args(args, BlockedSlot)

    return {
        "data": [slot.json() for slot in slots]
    }