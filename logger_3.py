import sys
from datetime import datetime
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, message: str) -> str:
        pass


class DefaultFormatter(Formatter):
    def __init__(self, time_format="%Y-%m-%d %H:%M:%S"):
        self.time_format = time_format

    def format(self, message: str) -> str:
        timestamp = datetime.now().strftime(self.time_format)
        return f"[{timestamp}] {message}"


class Handler(ABC):
    @abstractmethod
    def emit(self, message: str):
        pass


class StderrHandler(Handler):
    def emit(self, message: str):
        sys.stderr.write(message + '\n')



class Logger:
    def __init__(self, formatter: Formatter):
        self.formatter = formatter
        self.handlers = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def log(self, message: str):
        formatted = self.formatter.format(message)
        for handler in self.handlers:
            handler.emit(formatted)
if __name__ == "__main__":
    formatter = DefaultFormatter("%H:%M:%S")
    logger = Logger(formatter)
    logger.add_handler(StderrHandler())
    logger.log("Повідомлення логгера")
