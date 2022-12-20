#!/usr/bin/env python3
# coding=utf-8

"""
This is a simple UNIX daemon implemented in pure python using the pydaemon module
"""

import os
import sys
import time

from pydaemon import Daemon


class UnixDaemon(Daemon):
    """
    UNIX Daemon implementation.
    This class inherits from pydaemon.Daemon.

    The UNIX Daemon implemented with this class will detach from the console,
    close all file descriptors, redirect stdin, stdout and stderr to /dev/null, etc

    Finally, it will enter the run loop and simply keep updating a text file with
    the number of run loop cycles performed so far.
    """

    def __init__(self, pidfile, outfile, daemon_name):
        """
        Override the init method.
        Sets the name of the pidfile, the name of the output file to track the number of run loop cycles and
        the name of the daemon itself.

        :param str pidfile: path to the PID file
        :param str outfile: path to the output file
        :param str daemon_name: name of the daemon
        """
        self.outfile = outfile
        self.loop_runs = 0

        super().__init__(pidfile, daemon_name=daemon_name)

    def configure(self):
        """
        configure() is a required method of the Daemon class, but we don't need it to do anything
        """
        pass

    def run(self, sleep_secs=1):
        """
        Main program run loop
        Counts the runs of the run-loop, and updates the output file with that number.

        :param int sleep_secs: number of seconds to sleep for between each run loop cycle
        """

        with open(self.outfile, 'wt') as f:
            while True:
                f.seek(0)
                self.loop_runs += 1
                f.write(f'loop runs: {self.loop_runs}\n')
                time.sleep(sleep_secs)

    def stop(self, silent=True):
        """
        Executed on daemon shutdown
        """

        os.unlink(self.pidfile)
        super().stop(silent)


def main():
    """
    Main entry point into the application
    """

    pidfile = '/tmp/unixdaemon.pid'
    output_file = '/tmp/unixdaemon.txt'
    daemon = UnixDaemon(pidfile, output_file, daemon_name='pyd')
    daemon.start()
    pid = daemon.get_pid()

    if not pid:
        print('Error starting daemon', file=sys.stderr)
        raise SystemExit(1)

    print(f'Started daemon; pid={pid}')
    raise SystemExit(0)


if __name__ == '__main__':
    main()
