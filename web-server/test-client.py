"""
Web Server Clients
Author: Ameya Daigavane
Spawns multiple clients that make HTTP requests to our server.
"""

import multiprocessing
import os
import requests
import sys

# Remove command-line proxy settings.
os.environ['HTTP_PROXY'] = ''


def start_client(client_num, file_path):
    # Using the requests library to make HTTP requests.
    response = requests.get('http://localhost:7000' + file_path)

    print(client_num, response.text)


if __name__ == '__main__':
    # Command-line arguments with defaults.
    try:
        num_clients = int(sys.argv[1])
    except (IndexError, TypeError):
        num_clients = 10

    try:
        file_path = sys.argv[2]
    except (IndexError, TypeError):
        file_path = '/files/bigfile1.txt'

    # Create client subprocesses.
    clients = []
    for client_num in range(num_clients):
        client_process = multiprocessing.Process(target=start_client, args=(client_num, file_path))
        client_process.start()
        clients.append(client_process)

    for client_process in clients:
        client_process.join()


