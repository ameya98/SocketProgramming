"""
Web Server Clients
Author: Ameya Daigavane
Spawns multiple clients that make HTTP requests to our server.
"""

import multiprocessing
import os
import requests

# Remove command-line proxy settings.
os.environ['HTTP_PROXY'] = ''


def start_client(client_num):
    # Using the requests library to make HTTP requests.
    response = requests.get('http://localhost:7000/files/file1.txt')

    print(client_num, response.text)


if __name__ == '__main__':
    clients = []
    num_clients = 100

    for client_num in range(num_clients):
        client_process = multiprocessing.Process(target=start_client, args=(client_num,))
        client_process.start()
        clients.append(client_process)

    for client_process in clients:
        client_process.join()


