from datetime import datetime

class Patient:
    def __init__(self, name, age, complaint):
        self.name = name
        self.age = age
        self.complaint = complaint
        self.registration_time = datetime.now()
        self.seen_time = None

    def get_info(self):
        time_str = self.registration_time.strftime("%H:%M")
        return f"{self.name} ({self.age} years) - {self.complaint} | Arrived: {time_str}"