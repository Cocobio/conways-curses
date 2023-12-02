import curses

options = ['Rows',
           'Columns',
           # 'Start/Stop',
           ]

selected = 0

options_width = max(len(opt) for opt in options)
for i in range(len(options)):
    options[i] = options[i].rjust(options_width, " ")

options_max = []

rows = 0
columns = 0


def init():
    global rows, columns
    options_max.append(curses.LINES-3)
    options_max.append(curses.COLS-2)

    rows = options_max[0]//2
    columns = options_max[1]//2


def get_rows():
    return rows


def get_columns():
    return columns


def sub_sel():
    global selected
    if selected != 0:
        selected -= 1


def add_sel():
    global selected
    if selected != len(options)-1:
        selected += 1


def add_sel_opt():
    global selected, rows, columns

    if selected == 0:
        rows += 1 if rows < options_max[0] else 0
    else:
        columns += 1 if columns < options_max[1] else 0


def sub_sel_opt():
    global selected, rows, columns

    if selected == 0:
        rows -= 1 if rows > 0 else 0
    else:
        columns -= 1 if columns > 0 else 0


def print_gui(stdscr):
    height, width = stdscr.getmaxyx()

    h_offset = (height-len(options)*2)//2
    x_offset = (width-(8+options_width+2*len(str(max(options_max)))))//2

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    if selected == 0:
        stdscr.addstr(h_offset, x_offset, options[0]+" :  "
                      + str(rows).rjust(len(str(options_max[0])), " ")
                      + f"/{options_max[0]} ", curses.color_pair(2))
        stdscr.addstr(h_offset+2, x_offset, options[1]+" :  "
                      + str(columns).rjust(len(str(options_max[1])), " ")
                      + f"/{options_max[1]} ")
    else:
        stdscr.addstr(h_offset, x_offset, options[0]+" :  "
                      + str(rows).rjust(len(str(options_max[0])), " ")
                      + f"/{options_max[0]} ")
        stdscr.addstr(h_offset+2, x_offset, options[1]+" :  "
                      + str(columns).rjust(len(str(options_max[1])), " ")
                      + f"/{options_max[1]} ", curses.color_pair(2))
