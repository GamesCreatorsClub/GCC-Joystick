import curses, curses.textpad, time
from functools import reduce
from struct import pack

# TODO
# - handle window resizes
# - also allow single axes (not just 2 axes grouped into a "stick")
# - handle "known" buttons? (start, select, etc.)

def draw_arrows(window, y, x):
    window.addch(y-1, x, curses.ACS_UARROW, curses.color_pair(1))
    window.addch(y+1, x, curses.ACS_DARROW, curses.color_pair(1))
    window.addch(y, x-1, curses.ACS_LARROW, curses.color_pair(1))
    window.addch(y, x+1, curses.ACS_RARROW, curses.color_pair(1))

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
        draw_arrows(window, vy, vx)
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
        draw_arrows(window, vy, vx)
    else:
        window.addch(vy-1, vx, ' ')
        window.addstr(vy, vx-1, '   ')
        window.addch(vy+1, vx, ' ')
    window.refresh()

def draw_hat_switch(window, key, xvalue, yvalue, selected):
    window.erase()
    # Title and border
    window.addstr(0, 0, 'Hat [ ]')
    window.addstr(0, 5, key, curses.color_pair(1) + (curses.A_REVERSE if selected else 0))
    curses.textpad.rectangle(window, 1, 0, 5, 6)
    # Current position
    window.addch(yvalue*2 + 3, xvalue*3 + 3, curses.ACS_DIAMOND, curses.color_pair(2))
    window.addstr(6, 1, 'X  {:>2}'.format(xvalue))
    window.addstr(7, 1, 'Y  {:>2}'.format(yvalue))
    # Arrow keys
    if selected:
        draw_arrows(window, 3, 3)
    window.refresh()
    
def draw_buttons(window, buttons, pressed):
    window.addstr(0, 0, 'Buttons')
    for i, b in enumerate(buttons):
        window.addstr(i + 2, 0, '{:6.6} ( ) [ ]'.format(buttons[i]))
        window.addstr(i + 2, 12, chr(ord('A') + i), curses.color_pair(1))
        window.addch(i + 2, 8, curses.ACS_DIAMOND if pressed[i] else ' ', curses.color_pair(2))
    window.refresh()

def control_hat_switch(x, y, c):
    if c == curses.KEY_UP:
        y = max(-1, y - 1)
    elif c == curses.KEY_DOWN:
        y = min(1, y + 1)
    elif c == curses.KEY_RIGHT:
        x = min(1, x + 1)
    elif c == curses.KEY_LEFT:
        x = max(-1, x - 1)

    return (x, y)

def control_dpad(x, y, c):
    #TODO same as control_hat_switch for now - maybe only allow only one direction at a time instead of both x and y?
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

def hat_value(x, y):
    if x == 0 and y == -1:
        # top
        return 1
    elif x == 1 and y == -1:
        # top right
        return 2
    elif x == 1 and y == 0:
        # right
        return 3
    elif x == 1 and y == 1:
        # bottom right
        return 4
    elif x == 0 and y == 1:
        # bottom
        return 5
    elif x == -1 and y == 1:
        # bottom left
        return 6
    elif x == -1 and y == 0:
        # left
        return 7
    elif x == -1 and y == -1:
        # top left
        return 8
    else:
        return 9

def curses_main(screen, title, device, has_hat_switch, has_dpad, axes, sticks, buttons):
    HAT_SWITCH_WIN_HEIGHT = 8
    HAT_SWITCH_WIN_WIDTH = 7
    DPAD_WIN_HEIGHT = 8
    DPAD_WIN_WIDTH = 9
    STICK_WIN_HEIGHT = 12
    STICK_WIN_WIDTH = 10
    BUTTON_WIN_WIDTH = 14

    dpad_x = 0
    dpad_y = 0
    hat_switch_x = 0
    hat_switch_y = 0
    
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
    if has_hat_switch:
        hat_switch_win = screen.subwin(HAT_SWITCH_WIN_HEIGHT, HAT_SWITCH_WIN_WIDTH, 2, xpos)
        xpos = xpos + HAT_SWITCH_WIN_WIDTH + 4
    buttons_win = screen.subwin(len(buttons) + 3, BUTTON_WIN_WIDTH, 2, xpos)

    hat_switch_idx = len(sticks) + (1 if has_dpad else 0)
    
    def update_stick(i):
        if i == hat_switch_idx:
            draw_hat_switch(hat_switch_win, str(hat_switch_idx+1), hat_switch_x, hat_switch_y, selected_stick == hat_switch_idx)
        elif has_dpad:
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
    screen.addstr(0, 2, ' {} '.format(title), curses.A_REVERSE)

    footer = max(STICK_WIN_HEIGHT, len(buttons) + 2) + 3
    screen.addstr(footer, 2, '[ ] Quit')
    screen.addstr(footer, 3, 'Q', curses.color_pair(1))

    # Draw buttons and sticks

    draw_buttons(buttons_win, buttons, pressed)
    for i in range(len(sticks) + (1 if has_dpad else 0) + (1 if has_hat_switch else 0)):
        update_stick(i)

    stop = False
    while not stop:
        has_changes = False
        c = screen.getch()
        if c == ord('q'):
            stop = True
        elif ord('a') <= c < ord('a') + len(buttons):
            # a, b, c... keys: buttons on/off
            pressed[c - ord('a')] = not pressed[c - ord('a')]
            draw_buttons(buttons_win, buttons, pressed)
            has_changes = True
        elif ord('1') <= c < ord('1') + len(sticks) + (1 if has_hat_switch else 0) + (1 if has_dpad else 0):
            # 1, 2... keys: select d-pad, sticks or hat switch
            old = selected_stick
            selected_stick = c - ord('1')
            update_stick(old)
            update_stick(selected_stick)

        # Check arrow keys for selected control and update it if changed
        if has_dpad and selected_stick == 0:
            (new_x, new_y) = control_dpad(dpad_x, dpad_y, c)
            if new_x != dpad_x or new_y != dpad_y:
                dpad_x, dpad_y = new_x, new_y
                update_stick(0)
                has_changes = True
        elif has_hat_switch and selected_stick == hat_switch_idx:
            (new_x, new_y) = control_hat_switch(hat_switch_x, hat_switch_y, c)
            if new_x != hat_switch_x or new_y != hat_switch_y:
                hat_switch_x, hat_switch_y = new_x, new_y
                update_stick(hat_switch_idx)
                has_changes = True
        else:
            stick = sticks[selected_stick - (1 if has_dpad else 0)]
            (new_x, new_y, t0) = control_stick(axis_values[stick[0]], axis_values[stick[1]], t0, c)
            if axis_values[stick[0]] != new_x or axis_values[stick[1]] != new_y:
                axis_values[stick[0]], axis_values[stick[1]] = new_x, new_y
                update_stick(selected_stick)
                has_changes = True

        # Move cursor to the lower right corner
        sh, sw = screen.getmaxyx()
        screen.move(sh-1, sw-1)

        # If anything changed, send new values to the BT device
        if has_changes:
            button_bits = reduce((lambda bits, v: (bits | 1<<v[0] if v[1] else bits)), [(i,v) for i, v in enumerate(pressed)], 0)
            # TODO handle any number of buttons/axes
            device.send_values(button_bits, [axis_values[a] for a in axes], hat_value(hat_switch_x, hat_switch_y))
        curses.napms(10)

def run(title, device, has_hat_switch, has_dpad, axes, sticks, buttons):
    stop = False
    while not stop:
        print("Waiting for connections")
        device.listen()
        try:
            curses.wrapper(curses_main, title, device, has_hat_switch, has_dpad, axes, sticks, buttons)
            stop = True
        except Exception as e:
            print("Failed to send data - disconnected " + str(e))
