#!/usr/bin/env python3

import argparse
import os

import sys
import itertools
import socket
from socket import socket as Socket

# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', args.port))
        server_socket.listen(1)

        print("server ready")

        while True:

            with server_socket.accept()[0] as connection_socket:
                request = connection_socket.recv(1024).decode('ascii')
                reply = http_handle(request)
                connection_socket.send(reply.encode('utf-8'))


            print("\n\nReceived request")
            print("======================")
            print(request.rstrip())
            print("======================")


            print("\n\nReplied with")
            print("======================")
            print(reply.rstrip())
            print("======================")


    return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    assert not isinstance(request_string, bytes)

    location = request_string.split(" ")[1]
    reply = location

    if os.path.isfile(location):
        with open(location, "rt") as f:
            reply = f.read()
    else:
        reply = "HTTP/1.0 404 Not Found\r\n"

    return reply


if __name__ == "__main__":
    sys.exit(main())
