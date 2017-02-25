#!/usr/bin/env python3

import argparse

import sys
import socket
from socket import socket as Socket


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('my_address', type=str)
    parser.add_argument('mail_server', type=str)
    parser.add_argument('their_address', type=str)
    parser.add_argument('message', type=str)
    args = parser.parse_args()


    send_mail(args.my_address, args.mail_server, args.their_address, args.message)


    # success
    return 0


def send_mail(my_address, mail_server, their_address, message):

    client_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((mail_server, 25))

    sentences = ["helo localhost",
                 "mail from: <" + my_address + ">",
                 "rcpt to: <" + their_address + ">",
                 "data",
                 message + "\n.",
                 "quit", ]
    for s in sentences:
        reply = client_socket.recv(2048)
        print("reply: ", reply)

        s += "\n"
        print(s.encode("utf-8"))
        client_socket.send(s.encode("utf-8"))

    client_socket.close()

    return



if __name__ == "__main__":
    sys.exit(main())
