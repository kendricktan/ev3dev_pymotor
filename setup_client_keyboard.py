from ev3dev_pymotor.ev3dev_pymotor import *
from tcp.client import *
import curses
import time
import thread

# Initalizes client
# Checks for usage help
if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'Usage: python setup_client.py [server ip]'
        sys.exit()

TCP_IP = str(sys.argv[1]) if len(sys.argv) > 1 else ''

client = client_tcp(TCP_IP)

# Need to multi-thread
thread.start_new_thread(client.client_loop_set, ())

# Initializes curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 10, 'Hit "q" to quit')
stdscr.refresh()

key = ''

while key != ord('q'):
    key = stdscr.getch()
    stdscr.addch(20,25,key)
    stdscr.refresh()

    if key == curses.KEY_UP:
        stdscr.addstr(2, 20, 'Up')
        client.set_msg('run_forever')

    elif key == curses.KEY_DOWN:
        stdscr.addstr(3, 20, 'Down')
        client.set_msg('change_rps(-0.75)')

    elif key == curses.KEY_LEFT:
        stdscr.addstr(4, 20, 'Left')
        client.set_msg('left change_rps(0.75)')
        time.sleep(0.03)
        client.set_msg('right change_rps(-0.75)')

    elif key == curses.KEY_RIGHT:
        stdscr.addstr(5, 20, 'Right')
        client.set_msg('left change_rps(-0.75)')
        time.sleep(0.03)
        client.set_msg('right change_rps(0.75)')

    elif key == ord('t'):
        stdscr.addstr(6, 20, 'Toggle')
        client.set_msg('toggle')

    elif key == ord('s'):
        stdscr.addstr(7, 20, 'Stop')
        client.set_msg('stop')

curses.endwin()
