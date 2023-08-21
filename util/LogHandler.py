from enum import Enum

class LogType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class LogHandler():
    def __init__(self):
        self.info_path = ".secrets/info_log.txt"
        self.warning_path = ".secrets/warning_log.txt"
        self.error_path = ".secrets/error_log.txt"

    def write(self, path: str, msg: str):
        with open(path, 'a') as file:
            file.write(msg + "\n")

    def write_to_log(self, logtype: LogType, msg: str):
        match (logtype):
            case LogType.INFO:
                path = self.info_path
            case LogType.WARNING:
                path = self.warning_path
            case LogType.ERROR:
                path = self.error_path
            case _ :
                raise Exception

        self.write(path, msg)

