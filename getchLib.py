'''
From here:
https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
which is from here:
http://code.activestate.com/recipes/134892/

Sampe usage:
from getchLib import _Getch
import sys
getch = _Getch()
print("Will echo what you type. Ctrl-c to exit.")
while True:
  inChar = getch()
  print(inChar, end='', flush=True)
  if inChar in  [chr(3),chr(4),chr(7)]:
    print("Recieved ctrl-c, ctrl-d, or ctrl-g. Exiting...")
    sys.exit(0)
'''

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
