from datetime import datetime

def get_log_message_dict(response_with_code_tup):
    response, code = response_with_code_tup

    message = response.get("message", "")
    details = response.get("data", {})
    level = get_log_level(code)

    return {
        "message": message,
        "source": "manageBooking complex service",
        "timestamp": datetime.now().isoformat(),
        "details": details,
        "level": level
    }

def get_log_level(code):
    if (code >= 200 and code < 300):
        return "INFO"
    elif (code >= 300 and code < 400):
        return "WARNING"
    else:
        return "ERROR"