from flask import Blueprint, request,jsonify
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
                "data": None,
                "message": "Invalid slot no. Only slot nos betweeen 1 and 24 are allowed.",
            }, 400
    
        db.session.add(slot)
        db.session.commit()

    except IntegrityError:
        return {
            "data": None,
            "message": "Slot already blocked",
        }, 400

    except TypeError as e:
        return {
            "data": None,
            "message": str(e),
        }, 400

    except Exception as e:
        traceback.print_exception(e)
        return {
            "data": None,
            "message": "An unexpected error occurred.",
        }, 500
    
    return {
        "data": slot.json(),
        "message": "Slot created successfully.",
    }, 201

@routes.route("/", methods=["GET"])
def get_blocked_slots():
    args = request.args
    try:
        slots = BlockedSlot.query.filter_by(**args).all()

    except InvalidRequestError as e:
        return {
            "data": None,
            "message": "Bad request: " + str(e),
        }, 400

    if slots:
        return {
            "data": [slot.json() for slot in slots],
            "message": "Slots retrieved successfully.",
        }, 200
    
    else:
        return {
            "data": [],
            "message": "No slots found.",
        }, 200
    
@routes.route("/", methods=["DELETE"])
def delete_blocked_slot():
    slot_id = request.args.get('id')  # Get 'id' from query parameters
    if not slot_id:
        return jsonify({"message": "Slot ID is required."}), 400
    try:
        slot = BlockedSlot.query.get(slot_id)  # Retrieve the slot by id
        if slot:
            db.session.delete(slot)  # Delete the slot
            db.session.commit()  # Commit the changes
            return jsonify({"message": "Slot deleted successfully."}), 200
        else:
            return jsonify({"message": "Slot not found."}), 404
    except InvalidRequestError as e:
        db.session.rollback()  # Rollback in case of exception
        return jsonify({"message": "Bad request: " + str(e)}), 400