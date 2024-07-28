from datetime import datetime


def log(log_type: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] - [{log_type.upper()}]: {message}"
    print(msg)