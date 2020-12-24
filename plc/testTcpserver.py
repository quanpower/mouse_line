# coding: utf-8
from __future__ import absolute_import

import sys


if sys.version_info[0] == 2:
    import SocketServer as socketserver
else:
    import socketserver


class CustomRequestHandler(socketserver.StreamRequestHandler):
    def __init__(self, socket, host_port, server):
        # print(socket)
        print(host_port)
        # print(server)

    def handle(self):
        request_data = self.request.recv(65535)

        self.wfile.write(request_data)


def main():
    try:
        server = socketserver.TCPServer(
            ('0.0.0.0', 8000), CustomRequestHandler
        )

        server.serve_forever()
    except KeyboardInterrupt:
        return



if __name__ == '__main__':
    exit(main())
