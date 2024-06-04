import json
import traceback
from collections import defaultdict
from inspect import signature, Signature
from pathlib import Path
from typing import Callable, DefaultDict, Set, Union, Any, List, Dict

from .handlers.folder_handler import folder_handler_wrapper
from .http import HTTPHeader, HTTPStatusCodes, ContentTypes, HTTPHeaders
from .request import Request
from .response import Response


class TurboAPI:
    def __init__(self) -> None:
        self._mounted_folders: Set[str] = set()
        self._mapping: DefaultDict[str, Dict[str, Callable]] = defaultdict(dict)

    def post(self, route: str) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self._mapping["POST"][route] = func
            return func

        return wrapper

    def get(self, route: str) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self._mapping["GET"][route] = func
            return func

        return wrapper

    def mount_folder(self, base_route: str) -> None:
        self._mounted_folders.add(base_route if base_route.startswith("/") else f"/{base_route}")

    def _get_handler(self, method: str, uri: str) -> Union[Callable, None]:
        handler: Callable = self._mapping.get(method.upper(), {}).get(uri, None)

        if not handler:
            for mounted_folder in self._mounted_folders:
                if uri.startswith(mounted_folder):
                    handler = folder_handler_wrapper(Path(mounted_folder.removeprefix("/")).resolve().absolute())
                    break

        return handler

    @staticmethod
    def _assemble_handler_arguments(handler: Callable, request: Request, response: Response) -> List[Any]:
        pre_initialized = {Request: request, Response: response, Signature.empty: None}
        args = []
        handler_signature = signature(handler).parameters

        for parameter, param_type in list(handler_signature.items()):
            if type(param_type.annotation) is not str:
                requested_type = param_type.annotation
            else:
                requested_type = eval(param_type.annotation)

            param = pre_initialized.get(param_type.annotation, handler_signature)
            args.append(requested_type() if param is handler_signature else param)

        return args

    def handle_request(self, request: Request) -> bytes:
        try:
            method, uri = request.method, request.uri
            if not uri:
                uri = "/"

            handler = self._get_handler(method, uri)

            if not handler:
                return (
                        HTTPHeader.HTTP_1_1.value +
                        HTTPStatusCodes.NOT_FOUND_404.value +
                        HTTPHeader.RN.value
                ).encode()

            response = Response(
                ContentTypes.PLAIN.value,
                HTTPStatusCodes.OK_200.value
            )

            args = self._assemble_handler_arguments(handler, request, response)
            response_data = handler(*args)

            res = (
                    HTTPHeader.HTTP_1_1.value + response.STATUS_CODE + HTTPHeader.RN.value +
                    HTTPHeaders.CONTENT_TYPE.value + response.CONTENT_TYPE + HTTPHeader.RN.value +
                    HTTPHeaders.CONTENT_LENGTH.value + str(len(response_data)) + HTTPHeader.RNRN.value
            ).encode()

            if type(response_data) is str:
                res += response_data.encode()
            elif type(response_data) is bytes:
                res += response_data
            else:
                res += json.dumps(response_data).encode()

            return res
        except Exception as e:
            traceback.print_exception(e)
            return (
                    HTTPHeader.HTTP_1_1.value + HTTPStatusCodes.INTERNAL_SERVER_ERROR_500.value + HTTPHeader.RNRN.value
            ).encode()
