import socket, sys

# Get directory as command-line argument, default to current directory.
try:
    rootdir = sys.argv[1]
except IndexError:
    rootdir = '.'


# Starts the server to listen over the give port.
def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        # Bind socket to port and start listening.
        listening_socket.bind((host, port))
        listening_socket.listen()
        print('Server listening on port', port)

        # Keep listening and accepting connections. Currently blocking.
        while True:
            connection_socket, address = listening_socket.accept()

            print('Connection from', address[0], 'on port', address[1])
            listen(connection_socket)
            print('Connection with', address[0], 'on port', address[1], 'closed')


# Listens and transmits over the socket identified with this socket object.
def listen(data_socket):
    num_bytes = 10000

    with data_socket:
        try:
            # Wait for bytes to be sent, and decode as ASCII when they do arrive.
            http_request = data_socket.recv(num_bytes).decode('ascii')
        except ConnectionAbortedError:
            return

        try:
            # Parse the HTTP request to get the file name.
            file_name = get_file_name(http_request)

            # Open file and read contents.
            # If the file doesn't exist, we catch the FileNotFound exception.
            with open(file_name, 'r') as f:
                file_text = f.read()

            # Create the HTTP response with file_text in the body.
            response = http_response(file_text)

        except (FileNotFoundError, IndexError):
            error_text = 'Error: File not found.'

            # Create the HTTP response with the error message in the body.
            response = http_error(error_text)

        # Send the byte-encoded response over the socket.
        data_socket.sendall(response.encode())


# Hacky parsing to extract the file name from the HTTP request.
def get_file_name(request):
    try:
        filename = request.split()[1]
        return rootdir + filename
    except IndexError:
        print('Invalid request', request, 'of length', len(request))
        raise

def http_error(error_message):
    return http_response(error_message, status=404, status_text='NOT FOUND')


def http_response(text, status=200, status_text='OK'):
    # Indicates the HTTP protocol being used, and the status.
    response_proto = 'HTTP/1.1'
    response_status = str(status)
    response_status_text = status_text

    # HTTP headers.
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(text),
        'Connection': 'keep-alive',
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
    host = "127.0.0.1"
    port = 7000

    start_server(host, port)



