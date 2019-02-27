"""
Web Server Clients
Author: Ameya Daigavane
Uses cURL to make HTTP requests to our server.
"""

import subprocess
import os

# We remove our command-line proxy settings.
env = dict(os.environ)
env['HTTP_PROXY'] = ''

# Subprocess to use curl and see the output.
output = subprocess.check_output(['curl', '-s', 'localhost:7000/files/file1.txt'], env=env)
print(output.decode())
