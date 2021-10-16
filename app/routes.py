from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound

from app.models import Appointment, Appointments
from http import HTTPStatus as http_codes


appointment = Blueprint('simple_page', __name__)
appointments = Appointments()


@appointment.errorhandler(Exception)
def exception_handler(e):
    return jsonify({"error": str(e)}), http_codes.INTERNAL_SERVER_ERROR


@appointment.errorhandler(ValueError)
def exception_handler(e):
    return jsonify({"error": str(e)}), http_codes.BAD_REQUEST


@appointment.errorhandler(NotFound)
def exception_handler(e):
    return jsonify({"error": e.description}), http_codes.NOT_FOUND


@appointment.route("/appointments/<user_id>/<format>", methods=['GET'])
@appointment.route("/appointments/<user_id>", methods=['GET'])
def get_appointments(user_id, format=Appointment.Format.JSON):

    appointment_format = Appointment.Format.from_string(format)
    appointments_list = appointments.get(user_id, appointment_format)

    if not appointments_list:
        raise NotFound("Appointments not found")

    return jsonify(appointments_list)


@appointment.route("/appointments", methods=['POST'])
def post_appointments():

    appointment = Appointment.from_request(request)
    appointments.add(appointment)
    return '', http_codes.CREATED
