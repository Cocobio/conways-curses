import curses
from gol import GOL
from time import sleep
import gui

running = True


def draw_frame(pad, width: int, height: int,
               x_offset: int = 0, y_offset: int = 0):
    if height < 2:
        return

    pad.addstr(y_offset, x_offset, "╭"+("─"*(width-2))+"╮")
    for i in range(y_offset+1, y_offset+height-1):
        pad.addch(i, x_offset, "│")
        pad.addch(i, x_offset+width-1, "│")
    pad.addstr(y_offset + height-1, x_offset, "╰"+("─"*(width-2))+"╯")
    # pad.mvaddch(y_offset + height-1, x_offset + width-1, "╯")


def draw_boolean_matrix(pad, matrix, old_matrix, width: int, height: int,
                        x_offset: int = 0, y_offset: int = 0):
    for i, j in ((i, j) for i in range(width) for j in range(height)):
        if matrix[i][j] != old_matrix[i][j]:
            pad.addch(j + y_offset, i + x_offset,
                      "" if matrix[i][j] else " ")


def main(stdscr):
    global running
    stdscr.clear()

    # Gui
    gui.init()

    # Game of life class
    N, M = curses.COLS-2, curses.LINES-3
    gol_data = GOL((N, M))
    game_running = False
    w_offset = 0
    h_offset = 0

    curses.cbreak()
    curses.curs_set(0)

    stdscr.nodelay(True)

    # Use of colors, if not included termux glitches
    if curses.has_colors():
        curses.use_default_colors()
        curses.start_color()

    stdscr.clear()
    draw_frame(stdscr, gol_data.width+2, gol_data.height+2)
    # stdscr.border("│", "│", "─", "─", "╭", "╮", "╰", "╯")
    # stdscr.border("|", "|", "-", "-")
    while running:
        key = stdscr.getch()

        if key == ord('q'):
            running = False
        elif key == ord('s'):
            if not game_running:
                gol_data = GOL((gui.columns, gui.rows))
                w_offset = (curses.COLS-gui.columns-2)//2
                h_offset = (curses.LINES-gui.rows-3)//2
            else:
                gol_data = GOL((N, M))
                w_offset = 0
                h_offset = 0
            game_running = not game_running
            stdscr.clear()
            draw_frame(stdscr, gol_data.width+2, gol_data.height+2,
                       w_offset, h_offset)
        elif key == ord("h"):
            if not game_running:
                gui.sub_sel_opt()
        elif key == ord("j"):
            if not game_running:
                gui.add_sel()
        elif key == ord("k"):
            if not game_running:
                gui.sub_sel()
        elif key == ord("l"):
            if not game_running:
                gui.add_sel_opt()

        stdscr.refresh()

        sleep(0.2)

        if (game_running):
            draw_boolean_matrix(stdscr, gol_data.gen, gol_data.old_gen,
                                gol_data.width, gol_data.height,
                                w_offset+1, h_offset+1)
            gol_data.next_gen()
        else:
            gui.print_gui(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
