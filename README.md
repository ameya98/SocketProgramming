# Socket Programming
Exercises taken from the 6th edition of *Computer Networks: A Top-Down Approach* by Kurose and Ross.

## Web Server
Retrieves contents of files stored serverside. Currently, only one request served at a time.
'''python
python web-server.py dirpath
'''

*dirname* is an optional argument indicating the path to the directory containing files to be read. Both absolute and relative paths work. If not passed, the current directory is used.