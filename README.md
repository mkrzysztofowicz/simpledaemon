# SimpleDaemon

This project implements a simple UNIX Daemon using the [pydaemon](https://github.com/mkrzysztofowicz/pydaemon) module, 
to demonstrate how to use the module. 

The daemon itself does very little:
* detaches from the console
* closes all file descriptors
* redirects `stdin`, `stdout` and `stderr` to `/dev/null` to ensure it's not trying to output anything to the console
* creates the PID file `/tmp/unixdaemon.pid`
* enters the main run-loop, counts the run-loop cycles, and writes the count to the output file `/tmp/unixdaemon.txt`

This project can be used as a simple example of how to implement a standard UNIX daemon in pure Python with the use of
`pydaemon` module, and can be extended to actually perform something useful. 