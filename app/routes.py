from flask import Blueprint

appointment = Blueprint('simple_page', __name__)

@appointment.route("/appointments", methods=['GET'])
def get_appointments():
    return "<p>Hello, World!</p>"

@appointment.route("/appointments", methods=['POST'])
def post_appointments():
    return "<p>Hello, World!</p>"
