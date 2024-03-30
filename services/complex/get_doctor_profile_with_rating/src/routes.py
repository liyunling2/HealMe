from flask import Blueprint, jsonify
from invokes import get_doctor_profile, get_doctor_ratings

routes = Blueprint("get_doctor_profile_with_rating", __name__)

@routes.route("/<string:doctor_id>", methods=["GET"])
def get_doctor_profile_with_ratings(doctor_id):
    doctor_profile = get_doctor_profile(doctor_id)
    if doctor_profile is None:
        return jsonify({"message": "Error fetching doctor profile."}), 500
        
    doctor_ratings_response = get_doctor_ratings(doctor_id)
    if doctor_ratings_response is None or 'data' not in doctor_ratings_response:
        return jsonify({"message": "Error fetching doctor ratings."}), 500
    
    doctor_ratings = doctor_ratings_response['data']

    ratings = [float(rating["ratingGiven"]) for rating in doctor_ratings]
    average_rating = sum(ratings) / len(ratings) if ratings else 0

    doctor_profile_with_ratings = {**doctor_profile, "averageRating": average_rating, "ratingCount": len(ratings)}

    return jsonify({"data": doctor_profile_with_ratings, "message": "Doctor profile with ratings retrieved successfully."}), 200
