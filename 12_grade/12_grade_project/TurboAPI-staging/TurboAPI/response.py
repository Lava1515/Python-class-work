from dataclasses import dataclass


@dataclass
class Response:
    CONTENT_TYPE: str
    STATUS_CODE: str
