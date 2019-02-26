# Socket Programming
Exercises taken from the 6th edition of *Computer Networks: A Top-Down Approach* by Kurose and Ross.

## Web Server
Retrieves contents of files stored server-side. Currently, only one request served at a time.  
Run with:
```python
python web-server.py dirpath
```

*dirpath* is an optional argument indicating the path to the directory containing files to be read. Both absolute and relative paths work. If not passed, the current directory is used.
