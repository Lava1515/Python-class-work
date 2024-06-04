from pathlib import Path

from TurboAPI import TurboAPI, Request, Response
from TurboAPI.http import ContentTypes
from TurboAPI.simple_server import SimpleServer

app = TurboAPI()
app.mount_folder("/webroot")


@app.get("/")
def index(response: Response) -> str:
    response.CONTENT_TYPE = ContentTypes.HTML.value
    return Path("webroot/index.html").read_text()


@app.get("/test")
def test(request: Request, response: Response) -> bytes:
    print(request)
    print(response)
    return b"hello world!"


def main() -> None:
    SimpleServer("0.0.0.0", 80).run(app)


if __name__ == '__main__':
    main()
