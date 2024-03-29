from flask import Blueprint, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from templates import create_html_email
load_dotenv()
routes = Blueprint("notification", __name__)

@routes.route("/")
def index():
    return "Notification service is running"

#POST A NOTIFICATION
@routes.route("/notification", methods=["POST"])
def send_email():
    data = request.json
    try:
        message = Mail(
            from_email=data['from'],
            to_emails=data['to'],
            subject=data['subject'],
            html_content=create_html_email(**data['content'])
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        
        return jsonify({'message': 'Email sent successfully', 'status_code': response.status_code}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

