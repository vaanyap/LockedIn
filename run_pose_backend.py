import os
import socket

from poseDetection import app


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0


def choose_port():
    configured_port = os.environ.get("LOCKEDIN_BACKEND_PORT")
    if configured_port:
        return int(configured_port)

    if not is_port_in_use(5000):
        return 5000

    return 5001


if __name__ == "__main__":
    port = choose_port()
    print(f"Starting LockedIn backend on http://127.0.0.1:{port}")
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=port)