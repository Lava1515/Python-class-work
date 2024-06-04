from pathlib import Path
from typing import Callable

from ..http import ContentTypes, HTTPStatusCodes
from ..request import Request
from ..response import Response


def folder_handler_wrapper(base_folder: Path) -> Callable:
    def folder_handler(request: Request, response: Response) -> bytes:
        uri = request.uri.removeprefix("/")
        path = Path(uri).absolute().resolve()
        if not path.exists() and base_folder not in list(path.parents):
            response.STATUS_CODE = HTTPStatusCodes.NOT_FOUND_404.value
            return b""
        response.CONTENT_TYPE = ContentTypes.from_file_extension(path.suffix[:].removeprefix(".")).value
        return path.read_bytes()

    return folder_handler
