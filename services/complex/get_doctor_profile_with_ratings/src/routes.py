from flask import Blueprint, jsonify
from models import Doctor, DoctorRating
from db import db

routes = Blueprint("routes", __name__)

@routes.route("/doctors/<string:doctorID>/profile_with_rating", methods=["GET"])
def get_doctor_profile_with_rating(doctorID):
    try:
        doctor = Doctor.query.get(doctorID)
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

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

        return jsonify(doctor_profile), 200
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
