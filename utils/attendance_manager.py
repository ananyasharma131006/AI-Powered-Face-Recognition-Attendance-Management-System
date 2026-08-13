import time
from utils.database_manager import mark_attendance


class AttendanceManager:

    def __init__(self):
        self.cooldown = {}
        self.cooldown_seconds = 5

    def process(self, student_id):

        current = time.time()

        # Ignore repeated detections for 5 seconds
        if student_id in self.cooldown:
            if current - self.cooldown[student_id] < self.cooldown_seconds:
                return None, None

        success, message = mark_attendance(student_id)

        self.cooldown[student_id] = current

        return success, message

    def reset(self):
        self.cooldown.clear()