from utils.database_manager import mark_attendance

success, message = mark_attendance(1)

print(success)
print(message)