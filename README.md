# Socket Programming
Exercises taken from the 6th edition of *Computer Networks: A Top-Down Approach* by Kurose and Ross.   
The textbook materials and code snippets are locked behind a paywall, so these are my own implementations of the exercises. Please raise an issue if you find any bugs.

## Web Server
Serves files stored server-side. Run with:
```python
python web-server.py dirpath
```
*dirpath* is an optional argument indicating the path to the directory containing files to be read. Both absolute and relative paths work. If not passed, the current directory is used.
Currently, only one request served at a time. 
