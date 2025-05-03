from enum import Enum

class LogInfoType(Enum):
    Correct = "[CORRECT]"
    Status = "[STATUS]"
    Error = "[ERROR]"
    ResponseStatus = "[RESPONSE STATUS]"

def log_info(text : str, log_info_type : LogInfoType = LogInfoType.Status):
    print(log_info_type.value + " " + text)
