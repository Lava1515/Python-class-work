from enum import Enum
from types import DynamicClassAttribute
from typing import Dict


class HTTPHeader(Enum):
    HTTP_1_0 = "HTTP/1.0 "
    HTTP_1_1 = "HTTP/1.1 "
    RN = "\r\n"
    RNRN = "\r\n\r\n"

    @property
    def value(self) -> str:
        return super().value


class HTTPRequestType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    CONNECT = "CONNECT"

    @property
    def value(self) -> str:
        return super().value


class HTTPStatusCodes(Enum):
    OK_200 = "200 OK"
    CREATED_201 = "201 Created"
    ACCEPTED_202 = "202 Accepted"
    REDIRECT_203 = "203 Redirect"
    NO_CONTENT_204 = "204 No Content"
    REDIRECT_205 = "205 Redirect"
    MOVED_301 = "301 Moved"
    FOUND_302 = "302 Found"
    SEE_OTHER_303 = "303 See Other"
    NOT_MODIFIED_304 = "304 Not Modified"
    BAD_REQUEST_400 = "400 Bad Request"
    UNAUTHORIZED_401 = "401 Unauthorized"
    FORBIDDEN_403 = "403 Forbidden"
    NOT_FOUND_404 = "404 Not Found"
    METHOD_NOT_ALLOWED_405 = "405 Method Not Allowed"
    NOT_ACCEPTABLE_406 = "406 Not Acceptable"
    PARAMETER_ERROR_422 = "422 Unprocessable Entity"
    INTERNAL_SERVER_ERROR_500 = "500 Internal Server Error"
    NOT_IMPLEMENTED_501 = "501 Not Implemented"
    BAD_GATEWAY_502 = "502 Bad Gateway"
    SERVICE_UNAVAILABLE_503 = "503 Service Unavailable"
    GATEWAY_TIMEOUT_504 = "504 Gateway Timeout"

    @property
    def value(self) -> str:
        return super().value


class HTTPHeaders(Enum):
    AUTHORIZATION = "Authorization:"
    CONTENT_TYPE = "Content-Type:"
    CONTENT_LENGTH = "Content-Length:"
    ACCEPT = "Accept:"
    ENCODING = "Content-Encoding:"
    HOST = "Host:"
    NAME = "Name:"
    QUERY_STRING = "Query-String:"
    TRANSFER_ENCODING = "Transfer-Encoding:"
    WWW_AUTHENTICATE = "WWW-Authenticate:"

    @property
    def value(self) -> str:
        return super().value


class ContentTypes(Enum):
    PLAIN = "text/plain"
    HTML = "text/html"
    JSON = "application/json"
    CSS = "text/css"
    YAML = "application/yaml"
    XML = "application/xml"
    ZIP = "application/zip"
    PNG = "image/png"
    JPEG = "image/jpeg"
    BMP = "image/bmp"
    TIFF = "image/tiff"
    JPG = "image/jpg"

    @property
    def value(self) -> str:
        return super().value

    @staticmethod
    def from_file_extension(extension: str) -> "ContentTypes":
        file_extensions_to_content_type: Dict[str, ContentTypes] = {
            "txt": ContentTypes.PLAIN,
            "html": ContentTypes.HTML,
            "json": ContentTypes.JSON,
            "css": ContentTypes.CSS,
            "yaml": ContentTypes.YAML,
            "xml": ContentTypes.XML,
            "zip": ContentTypes.ZIP,
            "png": ContentTypes.PNG,
            "jpeg": ContentTypes.JPEG,
            "bmp": ContentTypes.BMP,
            "tiff": ContentTypes.TIFF,
            "jpg": ContentTypes.JPG
        }
        file_extension = extension.lower().removeprefix(".")
        return file_extensions_to_content_type.get(file_extension, ContentTypes.PLAIN)
