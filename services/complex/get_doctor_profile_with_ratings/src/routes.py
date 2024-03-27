from flask import Blueprint, jsonify
from invokes import get_doctor_profile, get_doctor_ratings
import traceback

routes = Blueprint("doctor_profile_with_ratings", __name__)

@routes.route("/<string:doctorID>", methods=["GET"])
def get_doctor_profile_with_rating(doctorID):
    try:
        doctor_profile = get_doctor_profile(doctorID)
        if doctor_profile is None:
            return jsonify({"data": None, "message": "Doctor not found"}), 404
        
        ratings = get_doctor_ratings(doctorID)

        if ratings:
            average_rating = sum(rating['ratingGiven'] for rating in ratings) / len(ratings)
        else:
            average_rating = "No ratings yet"

        doctor_profile['averageRating'] = average_rating
        doctor_profile['ratings'] = ratings

        return jsonify({"data": doctor_profile, "message": "Doctor profile with ratings retrieved successfully."}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"data": None, "message": "An error occurred retrieving the doctor profile with ratings."}), 500