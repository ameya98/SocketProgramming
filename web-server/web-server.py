"""
Asynchronous IO Based Web Server
Author: Ameya Daigavane
Serves files stored server-side using non-blocking sockets and system calls.
"""

import socket
import sys
import asyncio
import aiofiles

# Get directory as command-line argument, default to current directory.
try:
    rootdir = sys.argv[1]
except IndexError:
    rootdir = '.'


# Starts the server to listen over the given port.
def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        print('Server listening on port', port, flush=True)

        # Make socket non-blocking
        listening_socket.setblocking(0)

        # Bind socket to port and start listening.
        listening_socket.bind((host, port))
        listening_socket.listen(2)

        # Keep listening and accepting connections.
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(accept_connections(listening_socket))


# Accept connections. Non-blocking due to asyncio.
async def accept_connections(listening_socket):
    loop = asyncio.get_event_loop()

    while True:
        connection_socket, address = await loop.sock_accept(listening_socket)
        print('Connection from', address[0], 'on port', address[1], flush=True)

        await listen(connection_socket)
        print('Connection with', address[0], 'on port', address[1], 'closed', flush=True)


# Listens and transmits over the socket identified with this socket object.
async def listen(data_socket):
    loop = asyncio.get_event_loop()

    with data_socket:
        try:
            # Wait for bytes to be sent, and decode as ASCII when they do arrive.
            num_bytes = 10000
            http_request = (await loop.sock_recv(data_socket, num_bytes)).decode('ascii')
        except ConnectionAbortedError:
            return

        try:
            # Parse the HTTP request to get the file name.
            file_name = get_file_name(http_request)

            # Open file and read contents.
            # If the file doesn't exist, we catch the FileNotFound exception.
            async with aiofiles.open(rootdir + file_name, 'r') as f:
                file_text = await f.read()

            # Create the HTTP response with file_text in the body.
            response = http_okay(file_text)

        except (FileNotFoundError, IndexError, UnicodeDecodeError, OSError):
            error_text = 'Error: File not found.'

            # Create the HTTP response with the error message in the body.
            response = http_error(error_text)

        # Send the byte-encoded response over the socket.
        await loop.sock_sendall(data_socket, response.encode())


# Hacky parsing to extract the file name from the HTTP request.
def get_file_name(request):
    try:
        filename = request.split()[1]
        return filename
    except IndexError:
        print('Invalid request', request, 'of length', len(request), flush=True)
        raise


# Returns a string with a HTTP status code of 404, with the response body as the error message.
def http_error(error_message):
    return http_response(error_message, status=404, status_text='NOT FOUND')


# Returns a string with a HTTP status code of 200, with the response body as passed.
def http_okay(response_body):
    return http_response(response_body, status=200, status_text='OK')


# Returns a string containing HTTP headers with the text message in the body.
def http_response(text, status=200, status_text='OK'):

    # Indicates the HTTP protocol being used, and the status.
    response_proto = 'HTTP/1.1'
    response_status = str(status)
    response_status_text = status_text

    # HTTP headers.
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(text),
        'Connection': 'close',
    }

    # Combining all of these as one string.
    response_headers_raw = ''.join(str(key) + ': ' + str(val) + '\n' for key, val in response_headers.items())

    # HTTP body.
    response_body_raw = text

    # Concatenate everything with the right spacing.
    response = response_proto + ' ' + response_status + ' ' + response_status_text + '\n'
    response += response_headers_raw + '\n'
    response += response_body_raw + '\n'

    return response


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 7000

    start_server(host, port)



