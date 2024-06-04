import socket
import threading
from typing import Tuple, List, Dict

from .http import HTTPHeaders, HTTPHeader
from .request import Request
from .turbo_api import TurboAPI


class SimpleServer:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server_socket: socket.socket | None = None

    def _initiate_server(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        print(f"Server Started, Listening on port {self._host}:{self._port}")

    def _accept_connection(self) -> Tuple[socket.socket, Tuple[str, int]]:
        client_socket, client_address = self._server_socket.accept()
        return client_socket, client_address

    @staticmethod
    def _extract_content_length(http_header: str) -> int:
        if HTTPHeaders.CONTENT_TYPE.value in http_header:
            return int(http_header.split(HTTPHeaders.CONTENT_TYPE.value + " ")[0].split(HTTPHeader.RN.value)[0])
        return 0

    @staticmethod
    def _parse_headers(headers: List[str]) -> Dict[str, str]:
        headers_dict = {}
        for header in headers:
            header_name, header_value = header.split(":", 1)
            headers_dict[header_name.strip()] = header_value.strip()
        return headers_dict

    def _recv_http_request(self, client_socket: socket.socket) -> Tuple[str, str, Dict[str, str], bytes]:
        header = b""
        while b"\r\n\r\n" not in header:
            res = client_socket.recv(1)
            if res == b"":
                raise ConnectionError("Connection closed")
            header += res

        header = header.decode()

        body = b""
        content_length = self._extract_content_length(header)
        while len(body) < content_length:
            res = client_socket.recv(content_length - len(body))
            if res == b"":
                raise ConnectionError("Connection closed")
            body += res

        headers_split = header[:-len(HTTPHeader.RNRN.value)].split(HTTPHeader.RN.value)
        method, uri = headers_split[0].split()[:2]

        return method.upper(), uri, self._parse_headers(headers_split[1:]), body

    def _handle_client(self, app: TurboAPI, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        try:
            method, uri, headers, body = self._recv_http_request(client_socket)
            print(f"{client_address[0]}:{client_address[1]} - {method} - {uri}")
            request = Request(uri, method, body, headers)
            res = app.handle_request(request)
            client_socket.sendall(res)
        finally:
            client_socket.close()

    def run(self, app: TurboAPI) -> None:
        self._initiate_server()
        while Tuple:
            client_socket, client_address = self._accept_connection()
            threading.Thread(target=self._handle_client, args=(app, client_socket, client_address,)).start()
