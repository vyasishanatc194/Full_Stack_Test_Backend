from dataclasses import dataclass


@dataclass(frozen=True)
class InvalidUserException(Exception):
    item: str
    message: str

    def __str__(self) -> str:
        return f"{self.item}:{self.message}"


@dataclass(frozen=True)
class UserException(Exception):
    item: str
    message: str

    def error_data(self) -> dict:
        return {"item": f"{self.item}", "message": f"{self.message}"}

    def __str__(self) -> str:
        return f"{self.item} {self.message}"
