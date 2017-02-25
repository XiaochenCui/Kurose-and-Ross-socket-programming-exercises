#!/usr/bin/env python3

import argparse
import re
import math
import threading

import sys
import socket
import itertools
from socket import socket as Socket


CHUNK_SIZE = 2048


def main():

    # Command line arguments. Use port 8080 by default: widely used for proxys
    # and >1024 so we don't need sudo to run.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=8080, type=int,
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
        # no multithreaded yet, would need to set up atomic updates to dict.
        # Might be automatic in python?

        # Create empty dict for cached pages
        cache_dict = {}

        print("Proxy server ready")

        while True:
            # Accept TCP connection from client
            with server_socket.accept()[0] as connection_socket:


                # Fill in the code to recive the request, check if the url is
                # in cache_dict and either serve the cached version or request
                # the page from the real server and cache it.

                # You may want to use code from the web server to extract
                # information from the request.

                # If you want to do more after that you could try to handle
                # updating cached pages, and then try to convert the server to
                # a multithreaded version.


                t = threading.Thread(target=handle_request, args=(cache_dict,
                                                                  connection_socket))
                t.start()

                return 0


# TODO: implement a multithreaded version
def handle_request(cache_dict, server_socket):
    # request head and host
    request = server_socket.recv(CHUNK_SIZE).decode("utf-8")
    match = re.search(r".*Host: (.+?)\nUser-Agent", request)
    request_host = match.group(1).strip()
    print("host:", request_host)

    # create a new server_socket and get response from host
    proxy_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((request_host, 80))
    proxy_socket.send(request.encode("utf-8"))
    response = b""
    chunk = proxy_socket.recv(CHUNK_SIZE)
    while chunk:
        response += chunk
        chunk = proxy_socket.recv(CHUNK_SIZE)
    print("Response: ", response)
    proxy_socket.close()

    # send back the response
    count_chunk = math.ceil(len(response)/CHUNK_SIZE)
    for i in range(count_chunk):
        server_socket.send(response[i*CHUNK_SIZE: i*CHUNK_SIZE+CHUNK_SIZE])
    server_socket.close()


if __name__ == "__main__":
    sys.exit(main())
