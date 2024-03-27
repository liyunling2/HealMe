from flask import Blueprint, jsonify
from models import Doctor, DoctorRating
from db import db
import traceback

routes = Blueprint("doctor_profile_with_ratings", __name__)

@routes.route("/<string:doctorID>", methods=["GET"])
def get_doctor_profile_with_rating(doctorID):
    try:
        doctor = Doctor.query.get(doctorID)
        
        if not doctor:
            return jsonify({"data": None, "message": "Doctor not found"}), 404

        ratings = DoctorRating.query.filter_by(doctorID=doctorID).all()

        if ratings:
            average_rating = sum(rating.ratingGiven for rating in ratings) / len(ratings)
            ratings_list = [rating.json() for rating in ratings]
        else:
            average_rating = None
            ratings_list = []

        doctor_profile = doctor.json()
        doctor_profile['averageRating'] = average_rating
        doctor_profile['ratings'] = ratings_list

        return jsonify({"data": doctor_profile, "message": "Doctor profile with ratings retrieved successfully."}), 200
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return jsonify({"data": None, "message": "An error occurred retrieving the doctor profile with ratings."}), 500
