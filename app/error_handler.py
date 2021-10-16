from flask import jsonify
from http import HTTPStatus as http_codes
from werkzeug.exceptions import NotFound

class AppointmentExistsError(Exception):

    def __init__(self, message='Appointment already exists'):
        self.message = message

        super().__init__(self.message)

class AppointmentBadTimeError(Exception):

    def __init__(self, message='Appointment time is invalid'):
        self.message = message

        super().__init__(self.message)


def init_error_handlers(app):

    @app.errorhandler(Exception)
    def handle_general_error(e):
        return jsonify({"error": str(e)}), http_codes.INTERNAL_SERVER_ERROR


    @app.errorhandler(ValueError)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), http_codes.BAD_REQUEST


    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({"error": e.description}), http_codes.NOT_FOUND
