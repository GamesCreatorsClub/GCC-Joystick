import curses, curses.textpad, time
from functools import reduce
from struct import pack

# TODO
# - handle window resizes
# - also allow single axes (not just 2 axes grouped into a "stick")
# - handle "known" buttons? (start, select, etc.)

def draw_stick(window, key, xvalue, yvalue, xname, yname, selected):
    window.erase()
    # Title and border
    window.addstr(0, 0, 'Stick [ ]')
    window.addstr(0, 7, key, curses.color_pair(1) + (curses.A_REVERSE if selected else 0))
    curses.textpad.rectangle(window, 1, 0, 9, 8)

    # Axis values
    window.addstr(10, 0, '{:4} {:>4}'.format(xname, xvalue))
    window.addstr(11, 0, '{:4} {:>4}'.format(yname, yvalue))

    # Current position
    vx = round((xvalue)/50) + 4
    vy = round((yvalue)/50) + 5
    window.addch(vy, vx, curses.ACS_DIAMOND, curses.color_pair(2))

    # Arrow keys
    if selected:
        window.addch(vy-1, vx, curses.ACS_UARROW, curses.color_pair(1))
        window.addch(vy+1, vx, curses.ACS_DARROW, curses.color_pair(1))
        window.addch(vy, vx-1, curses.ACS_LARROW, curses.color_pair(1))
        window.addch(vy, vx+1, curses.ACS_RARROW, curses.color_pair(1))
    window.refresh()

def draw_dpad(window, key, xvalue, yvalue, selected):
    window.erase()
    # Title
    window.addstr(0, 0, 'D-pad [ ]')
    window.addstr(0, 7, key, curses.color_pair(1) + (curses.A_REVERSE if selected else 0))

    # D-pad shape
    vy = 4
    vx = 4
    curses.textpad.rectangle(window, vy-3, vx-1, vy+3, vx+1)
    curses.textpad.rectangle(window, vy-1, vx-4, vy+1, vx+4)
    window.addch(vy-1, vx-1, curses.ACS_LRCORNER)
    window.addch(vy-1, vx+1, curses.ACS_LLCORNER)
    window.addch(vy+1, vx-1, curses.ACS_URCORNER)
    window.addch(vy+1, vx+1, curses.ACS_ULCORNER)

    # "Pressed" positions
    if yvalue != 0:
        window.addch(vy + yvalue*2, vx, curses.ACS_DIAMOND, curses.color_pair(2))
    if xvalue != 0:
        window.addch(vy, vx + xvalue*3, curses.ACS_DIAMOND, curses.color_pair(2))

    # Arrow keys - or clear the middle
    if selected:
        window.addch(vy-1, vx, curses.ACS_UARROW, curses.color_pair(1))
        window.addch(vy+1, vx, curses.ACS_DARROW, curses.color_pair(1))
        window.addch(vy, vx-1, curses.ACS_LARROW, curses.color_pair(1))
        window.addch(vy, vx+1, curses.ACS_RARROW, curses.color_pair(1))
    else:
        window.addch(vy-1, vx, ' ')
        window.addstr(vy, vx-1, '   ')
        window.addch(vy+1, vx, ' ')

    window.refresh()
    
def draw_buttons(window, buttons, pressed):
    window.addstr(0, 0, 'Buttons')
    for i, b in enumerate(buttons):
        window.addstr(i + 2, 0, '{:6.6} ( ) [ ]'.format(buttons[i]))
        window.addstr(i + 2, 12, chr(ord('A') + i), curses.color_pair(1))
        window.addch(i + 2, 8, curses.ACS_DIAMOND if pressed[i] else ' ', curses.color_pair(2))
    window.refresh()

def control_dpad(x, y, c):
    if c == curses.KEY_UP:
        y = max(-1, y - 1)
    elif c == curses.KEY_DOWN:
        y = min(1, y + 1)
    elif c == curses.KEY_RIGHT:
        x = min(1, x + 1)
    elif c == curses.KEY_LEFT:
        x = max(-1, x - 1)

    return (x, y)

def control_stick(x, y, t0, c):
    t = time.monotonic()
    dt = t - t0
    if dt > 0.2:
        if x > 0:
            x = max(0, x - 10)
        elif x < 0:
            x = min(0, x + 10)
        if y > 0:
            y = max(0, y - 10)
        elif y < 0:
            y = min(0, y + 10)
        t0 = t
    if c == curses.KEY_UP:
        y = max(-127, y - 10)
        t0 = t
    elif c == curses.KEY_DOWN:
        y = min(127, y + 10)
        t0 = t
    elif c == curses.KEY_RIGHT:
        x = min(127, x + 10)
        t0 = t
    elif c == curses.KEY_LEFT:
        x = max(-127, x - 10)
        t0 = t

    return (x, y, t0)

def curses_main(screen, device, has_dpad, axes, sticks, buttons):
    DPAD_WIN_HEIGHT = 8
    DPAD_WIN_WIDTH = 9
    STICK_WIN_HEIGHT = 12
    STICK_WIN_WIDTH = 10
    BUTTON_WIN_WIDTH = 14

    dpad_x = 0
    dpad_y = 0
    
    screen.nodelay(1)
    try:
        curses.curs_set(0)
    except:
        pass
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    pressed = [False] * len(buttons)
    axis_values = dict([(a, 0) for a in axes])
    selected_stick = 0
    t0 = time.monotonic()

    # Create windows for buttons and for each stick

    xpos = 2
    if has_dpad:
        dpad_win = screen.subwin(DPAD_WIN_HEIGHT, DPAD_WIN_WIDTH, 2, xpos)
        xpos = xpos + DPAD_WIN_WIDTH + 2
    stick_wins = [ screen.subwin(STICK_WIN_HEIGHT, STICK_WIN_WIDTH, 2, xpos + (STICK_WIN_WIDTH + 4) * i + 2) for i in range(len(sticks)) ]
    xpos = xpos + (STICK_WIN_WIDTH + 4) * len(sticks) + 2
    buttons_win = screen.subwin(len(buttons) + 3, BUTTON_WIN_WIDTH, 2, xpos)
    
    def update_stick(i):
        if has_dpad:
            if i == 0:
                draw_dpad(dpad_win, '1', dpad_x, dpad_y, selected_stick == 0)
            else:
                stick = sticks[i-1]
                draw_stick(stick_wins[i-1], str(i+1), axis_values[stick[0]], axis_values[stick[1]], stick[0], stick[1], selected_stick == i)
        else:
            stick = sticks[i]
            draw_stick(stick_wins[i], str(i+1), axis_values[stick[0]], axis_values[stick[1]], stick[0], stick[1], selected_stick == i)

    # Draw screen border etc.
    
    screen.box()
    screen.addstr(0, 2, ' Virtual Gamepad ', curses.A_REVERSE)

    footer = max(STICK_WIN_HEIGHT, len(buttons) + 2) + 3
    screen.addstr(footer, 2, '[ ] Quit')
    screen.addstr(footer, 3, 'Q', curses.color_pair(1))

    # Draw buttons and sticks

    draw_buttons(buttons_win, buttons, pressed)
    for i in range(len(sticks) + (1 if has_dpad else 0)):
        update_stick(i)
        
    stop = False
    while not stop:
        has_changes = False
        c = screen.getch()
        if c == ord('q'):
            stop = True
        elif ord('a') <= c < ord('a') + len(buttons):
            pressed[c - ord('a')] = not pressed[c - ord('a')]
            draw_buttons(buttons_win, buttons, pressed)
            has_changes = True
        elif ord('1') <= c < ord('1') + len(sticks) + (1 if has_dpad else 0):
            old = selected_stick
            selected_stick = c - ord('1')
            update_stick(old)
            update_stick(selected_stick)
            
        if has_dpad and selected_stick == 0:
            (new_x, new_y) = control_dpad(dpad_x, dpad_y, c)
            if new_x != dpad_x or new_y != dpad_y:
                dpad_x, dpad_y = new_x, new_y
                update_stick(0)
                has_changes = True
        else:
            stick = sticks[selected_stick - (1 if has_dpad else 0)]
            (new_x, new_y, t0) = control_stick(axis_values[stick[0]], axis_values[stick[1]], t0, c)
            if axis_values[stick[0]] != new_x or axis_values[stick[1]] != new_y:
                axis_values[stick[0]], axis_values[stick[1]] = new_x, new_y
                update_stick(selected_stick)
                has_changes = True
            
        sh, sw = screen.getmaxyx()
        screen.move(sh-1, sw-1)
        if has_changes:
            button_bits = reduce((lambda bits, v: (bits | 1<<v[0] if v[1] else bits)), [(i,v) for i, v in enumerate(pressed)], 0)
            # TODO handle any number of buttons/axes
            # TODO also handle dpad
            device.send_values(button_bits, [axis_values[a] for a in axes])
        curses.napms(10)

def run(device, has_dpad, axes, sticks, buttons):
    stop = False
    while not stop:
        print("Waiting for connections")
        device.listen()
        try:
            curses.wrapper(curses_main, device, has_dpad, axes, sticks, buttons)
            stop = True
        except Exception as e:
            print("Failed to send data - disconnected " + str(e))
