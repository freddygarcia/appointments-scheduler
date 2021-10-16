class AppointmentExistsError(Exception):

    def __init__(self, message='Appointment already exists'):
        self.message = message

        super().__init__(self.message)

class AppointmentBadTimeError(Exception):

    def __init__(self, message='Appointment time is invalid'):
        self.message = message

        super().__init__(self.message)

class InvalidUserIdError(Exception):

    def __init__(self, message='Invalid user id'):
        self.message = message

        super().__init__(self.message)
