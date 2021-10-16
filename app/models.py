from flask import request as flask_request
from datetime import date, time, datetime
from collections import defaultdict

from app.error_handler import AppointmentBadTimeError, AppointmentExistsError, InvalidUserIdError

class Appointment:

    def __init__(self):
        self.user_id = None
        self.date = None
        self.time = None

    @staticmethod
    def from_request(request: flask_request):
        appointment = Appointment()

        try:
            appointment.user_id = request.json['user_id']
            appointment.date = request.json['date']
            appointment.time = request.json['time']
        except KeyError as e:
            raise ValueError(f'Missing key: {e}')
        
        try:
            appointment.date = Appointment.parse_date(appointment.date)
        except ValueError as e:
            raise ValueError(f'Invalid date: {appointment.date}, please use the format YYYY-MM-DD')
        
        try:
            appointment.time = Appointment.parse_time(appointment.time)
        except (ValueError, TypeError) as e:
            raise ValueError(f'Invalid time: {appointment.time}, please use the format HH:MM')
        
        return appointment

    @staticmethod
    def parse_date(str_date: str):
        return date.fromisoformat(str_date)
    
    @staticmethod
    def parse_time(str_time: str):
        return datetime.strptime(str_time, '%H:%M')
    
    def __str__(self) -> str:
        return f'{self.user_id} {self.date} {self.time}'

class Appointments:

    def __init__(self):
        self.appointments = defaultdict(dict)
    
    def check_user_already_has_appointment(self, user_id: int, date: date):
        return date in self.appointments[user_id]
    
    def check_time_is_valid(self, time: time):
        return time.minute % 30 != 0
    
    def add(self, appointment: Appointment):

        if self.check_user_already_has_appointment(appointment.user_id, appointment.date):
            raise AppointmentExistsError(f'User {appointment.user_id} has alredy  an appointment on {appointment.date}')
        
        if self.check_time_is_valid(appointment.time):
            _time = appointment.time.strftime('%H:%M')
            raise AppointmentBadTimeError(f'Invalid time: {_time}, please use the format HH:MM in 30 minutes range. e.x. 1:30')

        self.appointments[appointment.user_id][appointment.date] = appointment.time
    
    def get(self, user_id: str):

        if user_id.isdigit():
            user_id = int(user_id)
        else:
            raise InvalidUserIdError
        
        return [ { 'date' : k, 'time' : v } for k, v in self.appointments[user_id].items() ]

    def __repr__(self):
        return f"<Appointments {self.appointments}>"

    def __str__(self):
        return len(self.appointments).__str__()

    def to_dict(self):
        return {
            "appointments": dict(self.appointments)
        }
