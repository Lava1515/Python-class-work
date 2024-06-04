from dataclasses import dataclass


@dataclass
class Request:
    uri: str
    method: str
    data: bytes
    headers: dict
