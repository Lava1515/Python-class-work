import os
import random
import time
import json
import socket
import threading
import traceback

# http://127.0.0.1:8000


# Constants
WEB_ROOT = "webroot"
HTTP = "HTTP/1.1 "
STRINGS = {"up": "/uploads/", "400": "/images/400.png", "404": "/images/404.png", "403": "/images/403.png",
           "500": "/images/403.png"}
CONTENT_TYPE = "Content-Type: "
CONTENT_LENGTH = "Content-Length: "
STATUS_CODES = {"ok": "200 OK\r\n", "bad": "400 BAD REQUEST\r\n", "not found": "404 NOT FOUND\r\n",
                "forbidden": "403 FORBIDDEN\r\n", "moved": "302 FOUND\r\n",
                "server error": "500 INTERNAL SERVER ERROR\r\n"}
FILE_TYPE = {"html": "text/html;charset=utf-8\r\n", "jpg": "image/jpeg\r\n", "css": "text/css\r\n",
             "js": "text/javascript; charset=UTF-8\r\n", "txt": "text/plain\r\n", "ico": "image/x-icon\r\n",
             "gif": "image/jpeg\r\n", "png": "image/png\r\n", "svg": "image/svg+xml", "json": "application/json\r\n"}
HTTP_TYPE = ["GET", "POST"]
IP = '0.0.0.0'
PORT = 8000
SOCKET_TIMEOUT = 2

# Globals
print_ = print
printing_lock = threading.Lock()
players = {}
the_game_name = ""
PIN = 0
Running = False
Can_move = False
elapsed_time = 0
Next_questions = []


def print(*values: object, sep: str | None = " ", end: str | None = "\n", file=None, flush: bool = False) -> None:
    printing_lock.acquire()
    print_(*values, sep=sep, end=end, file=file, flush=flush)
    printing_lock.release()


def read_file(file_name):
    """ Read A File """
    with open(file_name, "rb") as f:
        data = f.read()
    return data


def bad():
    """
    assembles a http 400 bad-request response
    """
    uri = WEB_ROOT + STRINGS["400"]
    data = read_file(uri)
    content_type = CONTENT_TYPE + FILE_TYPE["png"]
    content_length = CONTENT_LENGTH + str(os.path.getsize(uri)) + "\r\n"
    http_response = (HTTP + STATUS_CODES["bad"] + content_type + content_length + "\r\n")
    http_response = http_response.encode() + data
    return http_response


def not_found():
    """
    assembles a http 404 not found response
    """
    uri = WEB_ROOT + STRINGS["404"]
    data = read_file(uri)
    content_type = CONTENT_TYPE + FILE_TYPE["png"]
    content_length = CONTENT_LENGTH + str(os.path.getsize(uri)) + "\r\n"
    http_response = (HTTP + STATUS_CODES["not found"] + content_type + content_length + "\r\n")
    http_response = http_response.encode() + data
    return http_response


def update_rank(name, timer_time):
    ranking = {0: 0, 1: 20, 2: 50, 3: 100, 4: 120, 5: 140, 6: 160, 7: 190, 8: 210,
               9: 240, 10: 270, 11: 300, 12: 320, 13: 360, 14: 390, 15: 420, 16: 450,
               17: 480, 18: 510, 19: 540, 20: 570, 21: 610, 22: 640, 23: 700, 24: 730,
               25: 750, 26: 800, 27: 850, 28: 900, 29: 980, 30: 1000}
    global players

    players[name] += ranking[int(timer_time)]
    print(players)


def Set_Next_questions(lng):
    global Next_questions
    Next_questions = []
    for i in range(lng):
        Next_questions.append("False")


def sort_fanc(place):
    return int(place.split(":")[-1])


def handle_client_request(resource, client_socket: socket.socket, data: bytes):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :param data: in case the request of the client is a POST request
    :return: None
    """
    """ """
    global players, the_game_name, PIN, Running, Can_move, elapsed_time, Next_questions
    resource = resource.split(' ')[1]
    params = ""
    if "?" in resource:
        resource, params = resource.split("?")
    status_code = ""
    if data is not None:
        if resource == "/create":
            file_name = ""
            data = data.decode()
            res_name = data
            if "Game_Name" in res_name:
                res_name = res_name.split("Game_Name")
                res_name = res_name[-1].split()
                res_name = res_name[0].split(",")
                res_name = res_name[0][3:-1]
                if res_name == "":
                    res_name = "save_file"
                file_name = "./games/" + res_name + ".json"
            with open(file_name, "w") as out_file:
                out_file.write(data)
                out_file.close()

        if resource == "/players":
            data = json.loads(data.decode())
            players[data["Client_Name"]] = 0
            json.dumps(players)

        if resource == "/set_name" and not Running:
            Running = True
            the_game_name = data.decode().split("\"")[1]
            PIN = random.randint(10000000, 99999999)
            print(PIN)

        if resource == "/move_":
            Can_move = data.decode()[1:-1]

        if "/move_Qs" in resource:
            Next_questions[int(resource[-1]) - 1] = data.decode()[1:-1]

        if resource == "/back_to_home_page":
            print("back_to_home_page")
            players = {}
            the_game_name = ""
            PIN = 0
            Running = False
            Can_move = False
            elapsed_time = 0
            Next_questions = []

        content = CONTENT_TYPE + FILE_TYPE["json"] + CONTENT_LENGTH + "2\r\n"
        http_response = (HTTP + STATUS_CODES["ok"] + content + "\r\n{}").encode()
        while len(http_response) > 0:
            sent = client_socket.send(http_response)
            http_response = http_response[sent:]
        return

    if resource == "/":
        resource = "/index.html"

    if resource == '/forbidden':
        uri = WEB_ROOT + STRINGS["403"]
        status_code = STATUS_CODES["forbidden"]
        data = read_file(uri)
        content_type = CONTENT_TYPE + FILE_TYPE["png"]
        content_length = CONTENT_LENGTH + str(os.path.getsize(uri)) + "\r\n"
        http_response = HTTP + status_code + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data

    elif resource == "/moved":
        uri = ""
        status_code = STATUS_CODES["moved"]
        http_response = HTTP + STATUS_CODES["moved"] + "location: /" + "\r\n\r\n"
        http_response = http_response.encode()

    elif resource == "/error":
        uri = WEB_ROOT + STRINGS["500"]
        status_code = STATUS_CODES["server error"]
        data = read_file(uri)
        content_type = CONTENT_TYPE + FILE_TYPE["png"]
        content_length = CONTENT_LENGTH + str(os.path.getsize(uri)) + "\r\n"
        http_response = HTTP + status_code + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data

    elif "/GETNames" in resource:
        data = json.dumps(list(players.keys()))
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data.encode())) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/GET_true_false" in resource:
        print(resource, "resource")
        answer = resource.split("%20")[1:-3]
        timer_time = resource.split("%20")[-1]
        client_name = resource.split("%20")[-2]
        number = resource.split("%20")[-3]
        print(answer, "answer")
        answer = " ".join(answer)
        with open(f'./games/{the_game_name}.json', ) as f:
            data_ = json.load(f)
        check_answer = data_["The_data"].split("question number")
        check_answer = check_answer[int(number)].split(",")
        data__ = ""
        print(answer)
        print(check_answer)
        for i in range(len(check_answer)):
            if check_answer[i] == " " + answer:
                data__ = check_answer[i + 1]
                if data__ == " true":
                    update_rank(client_name, timer_time)
                break
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data__)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data__.encode()

    elif "/GETGameInfo" in resource:
        with open(f'./games/{the_game_name}.json', ) as f:
            data = json.load(f)
        lng = data["The_data"].split(",")
        lng = (len(lng) - 3) // 8
        Set_Next_questions(lng)
        data = json.dumps(data)
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/GET_Games_Names" in resource:
        names = os.listdir("games")
        data = json.dumps(names)
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/GetIP" in resource:
        data = json.dumps(PIN)
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/Can_move" in resource:
        data = json.dumps("DO NOT Move")
        if Can_move:
            data = json.dumps("Move")
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/move_to_next" in resource:
        data = json.dumps("DO NOT Move")
        if Next_questions[int(resource[-1]) - 1] == "True":
            data = json.dumps("Move")
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data)) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    elif "/get_names_and_ranks" in resource:
        lst = []
        for key in players.keys():
            lst .append(str(key) + " : " + str(players[key]))
        lst.sort(key=sort_fanc, reverse=True)
        data = json.dumps(lst)
        content_type = CONTENT_TYPE + FILE_TYPE["json"]
        content_length = CONTENT_LENGTH + str(len(data.encode())) + "\r\n"
        http_response = HTTP + STATUS_CODES["ok"] + content_type + content_length + "\r\n"
        http_response = http_response.encode() + data.encode()

    else:
        uri = WEB_ROOT + resource

        if os.path.isfile(uri):
            file_type = uri.split('.')[-1]
            http_header = CONTENT_TYPE
            http_header += FILE_TYPE[file_type]
            status_code = STATUS_CODES["ok"]
            http_response = HTTP + status_code + http_header

        else:
            http_response = not_found()

    if status_code == STATUS_CODES["ok"]:
        data = read_file(uri)
        content_length = CONTENT_LENGTH + str(os.path.getsize(uri)) + "\r\n"
        http_response += content_length + "\r\n"
        http_response = http_response.encode() + data

    while len(http_response) > 0:
        sent = client_socket.send(http_response)
        http_response = http_response[sent:]


def validate_http_request(request: str):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and
    the requested URL
    :param request: the request which was received from the client
    :return: a tuple of (True/False - depending on if the request is valid,
    the requested resource )
    """
    get = request.split(" ")
    if get[0] in HTTP_TYPE and len(get[1]) > 0 and "HTTP/1.1\r\n" in get[2] \
            and "\r\n\r\n" in request and request.count("\r\n") >= 4:
        return True, request
    else:
        return False, request


def handle_client(client_socket: socket.socket, client_address: tuple[str, int]):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :param client_address: the address of the client
    :return: None
    """
    try:
        stop = False
        while not stop:
            client_request = ""
            client_data = None
            while True:
                try:
                    data = client_socket.recv(1).decode()
                    client_request += data
                except socket.timeout:
                    stop = True
                    break
                if data == "":
                    stop = True
                    break
                if "\r\n\r\n" in client_request:
                    break
                if client_request == "":
                    client_socket.close()
                    break
            if "POST" in client_request:
                headers = client_request.split("\r\n")
                for header in headers:
                    if "Content-Length" in header:
                        headers = header
                        break
                data_length = int(headers[16:])
                client_data = b""
                while len(client_data) < data_length:
                    client_data += client_socket.recv(data_length - len(client_data))
            if client_request != "":
                valid_http, resource = validate_http_request(client_request)
                if valid_http:
                    handle_client_request(resource, client_socket, client_data)
                else:
                    http_response = bad()
                    client_socket.send(http_response)
                    break
    except Exception as e:
        traceback.print_exception(e)
    finally:
        client_socket.close()
        print("Connection closed with '%s:%s'" % client_address)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen()
        print("Listening for connections on port %d" % PORT)
        while True:
            client_socket, client_address = server_socket.accept()
            client_socket: socket.socket
            client_address: tuple[str, int]
            print("New connection received from '%s:%s'" % client_address)
            client_socket.settimeout(SOCKET_TIMEOUT)
            t = threading.Thread(target=handle_client, args=(client_socket, client_address))
            t.start()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()
    while threading.active_count() != 1:  # wait for all clients to close open connections
        time.sleep(0.1)


if __name__ == "__main__":
    main()
