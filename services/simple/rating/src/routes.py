from flask import Blueprint, request
from models import DoctorRating, ClinicRating
from db import db


routes = Blueprint("rating", __name__)


