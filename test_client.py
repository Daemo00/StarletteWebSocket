from starlette.testclient import TestClient

from main import instance


def main():
    client = TestClient(instance)

    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello!")

        data = websocket.receive_text()

        print(data)


if __name__ == "__main__":
    main()
