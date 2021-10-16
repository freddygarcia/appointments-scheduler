from flask import request as flask_request
from datetime import date, time, datetime
from collections import defaultdict

from app.error_handler import AppointmentBadTimeError, AppointmentExistsError, InvalidUserIdError

class Appointment:

    class Format:
        TIMESTAMP = 'timestamp'
        ISOFORMAT = 'isoformat'
        COMMON = 'common'
        JSON = 'json'

        @staticmethod
        def from_string(value: str) -> str:
            return {
                'iso' : Appointment.Format.ISOFORMAT,
                'cmn' : Appointment.Format.COMMON,
                'json' : Appointment.Format.JSON,
                'ts' : Appointment.Format.TIMESTAMP
            }.get(value.lower(), Appointment.Format.ISOFORMAT)

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
        return datetime.strptime(str_time, '%H:%M').time()
    
    def get_datetime(self):
        return datetime.combine(self.date, self.time)
    
    def format(self, format: Format):
        dt = self.get_datetime()

        if format == Appointment.Format.TIMESTAMP:
            return dt.timestamp()
        elif format == Appointment.Format.ISOFORMAT:
            return dt.isoformat()
        elif format == Appointment.Format.COMMON:
            return dt.strftime("%Y-%m-%d %H:%M")
        elif format == Appointment.Format.JSON:
            return {
                'date' : self.date.isoformat(),
                'time' : self.time.isoformat()
            }
        else:
            raise ValueError(f'Invalid format: {format}')
    
    def __str__(self) -> str:
        return f'{self.user_id} {self.date} {self.time}'

class Appointments:

    def __init__(self):
        self.appointments = defaultdict(list)
    
    def check_user_already_has_appointment(self, user_id: int, date: date):
        return date in [item.date for item in self.appointments[user_id]]
    
    def check_time_is_valid(self, time: time):
        return time.minute % 30 != 0
    
    def add(self, appointment: Appointment):

        if self.check_user_already_has_appointment(appointment.user_id, appointment.date):
            raise AppointmentExistsError(f'User {appointment.user_id} has alredy  an appointment on {appointment.date}')
        
        if self.check_time_is_valid(appointment.time):
            _time = appointment.time.strftime('%H:%M')
            raise AppointmentBadTimeError(f'Invalid time: {_time}, please use the format HH:MM in 30 minutes range. e.x. 1:30')

        self.appointments[appointment.user_id].append(appointment)
    
    def get(self, user_id: str, format=Appointment.Format.JSON):

        if user_id.isdigit():
            user_id = int(user_id)
        else:
            raise InvalidUserIdError
        
        return [ item.format(format) for item in self.appointments[user_id] ]

    def __repr__(self):
        return f"<Appointments {self.appointments}>"

    def __str__(self):
        return len(self.appointments).__str__()

    def to_dict(self):
        return {
            "appointments": dict(self.appointments)
        }
