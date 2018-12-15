#################################################################################
# by sDextra 
#################################################################################
# 1110011 1000100 1100101 1111000 1110100 1110010 1100001
#################################################################################

# row - field width
# column - field height
# speed - falling speed
# tops - number of top places
# level - level of difficulty
# mode - presence of a bonus
# impossible - without I tetromino
# for_level - the number of lines for level-up

# Highscore
init -100:
    if persistent.highscore is None:
        $ persistent.highscore = []

init python:
    # Tetromino Symbols
    symb_field = '·'
    symb_red = 'R'
    symb_cyan = 'C'
    symb_blue = 'B'
    symb_green = 'G'
    symb_orange = 'O'
    symb_purple = 'P'
    symb_yellow = 'Y'
    coloring = [symb_red, symb_cyan, symb_blue, symb_green, symb_orange, symb_purple, symb_yellow]

    row = 10
    column = 20

    tops = 10
    level = 1
    for_level = 20
    mode = False
    impossible = False
    speed = 0.4
    speed_limit = 0.05
    speed_acceleration = 0.03

    # Main Class
    class Tetris():
        def __init__(self, speed=.5, level=1, mode=False, bonus=0):
            self.field = ['·']*(row*column)
            self.active = 0
            self.rotate = 0
            self.tetrominos = {1:[1,1, 1,1], 2:[1,1,1,1, 0,0,0,0], 3:[1,0,0, 1,1,1], 4:[0,0,1, 1,1,1], 5:[0,1,1, 1,1,0], 6:[1,1,0, 0,1,1], 7:[0,1,0, 1,1,1] }
            self.next = self.get_tetromino()
            self.tetromino = []
            self.block = True
            self.can_rotation = True
            self.mode = mode
            self.bonus = bonus
            self.lines = 0
            self.lines_counter = 0
            self.point = 0
            self.level = level
            self.start_speed = speed
            self.speed = self.start_speed
            self.can_skip = True
            self.end = False

        def delete_I(self):
            self.tetrominos.pop(2)

        def get_tetromino(self):
            m = []
            for tetromino in self.tetrominos.values():
                m.append(tetromino)
            r = renpy.random.choice(m)
            return r

        def get_tetromino_i(self, i):
            return self.tetrominos.get(i)

        def clear(self, end=False):
            i = 0
            for cell in self.field:
                for color in coloring:
                    if cell == color:
                        self.field[i] = symb_field
                i += 1
            if end:
                self.end_turn()

        def delete(self):
            self.clear(end=True)
            self.bonus -= 1

        def draw_tetromino(self):
            self.clear()
            j = self.tetromino_index_start()
            i = 0
            for cell in self.tetromino:
                if cell:
                    # Tetromino O
                    if self.tetromino == [1,1, 1,1]:
                        self.field[self.active+j] = symb_yellow
                    # Tetromino I
                    elif self.tetromino == [1,1,1,1, 0,0,0,0] or self.tetromino == [0,0,0,0, 1,1,1,1]:
                        self.field[self.active+j] = symb_purple
                    # Tetromino J
                    elif self.tetromino == [1,0,0, 1,1,1] and not self.rotate or self.tetromino == [1,1,1, 0,0,1] and self.rotate == 180:
                        self.field[self.active+j] = symb_blue
                    elif self.tetromino == [1,1, 1,0, 1,0] and self.rotate == 90 or self.tetromino == [0,1, 0,1, 1,1] and self.rotate == 270:
                        self.field[self.active+j] = symb_blue
                    # Tetromino L
                    elif self.tetromino == [0,0,1, 1,1,1] and not self.rotate or self.tetromino == [1,1,1, 1,0,0] and self.rotate == 180:
                        self.field[self.active+j] = symb_orange
                    elif self.tetromino == [1,0, 1,0, 1,1] and self.rotate == 90 or self.tetromino == [1,1, 0,1, 0,1] and self.rotate == 270:
                        self.field[self.active+j] = symb_orange
                    # Tetromino S
                    elif self.tetromino == [0,1,1, 1,1,0] and not self.rotate or self.tetromino == [0,1,1, 1,1,0] and self.rotate == 180:
                        self.field[self.active+j] = symb_green
                    elif self.tetromino == [1,0, 1,1, 0,1] and self.rotate == 90 or self.tetromino == [1,0, 1,1, 0,1] and self.rotate == 270:
                        self.field[self.active+j] = symb_green
                    # Tetromino Z
                    elif self.tetromino == [1,1,0, 0,1,1] and not self.rotate or self.tetromino == [1,1,0, 0,1,1] and self.rotate == 180:
                        self.field[self.active+j] = symb_red
                    elif self.tetromino == [0,1, 1,1, 1,0] and self.rotate == 90 or self.tetromino == [0,1, 1,1, 1,0] and self.rotate == 270:
                        self.field[self.active+j] = symb_red
                    # Tetromino T
                    elif self.tetromino == [0,1,0, 1,1,1] and not self.rotate or self.tetromino == [1,1,1, 0,1,0] and self.rotate == 180:
                        self.field[self.active+j] = symb_cyan
                    elif self.tetromino == [1,0, 1,1, 1,0] and self.rotate == 90 or self.tetromino == [0,1, 1,1, 0,1] and self.rotate == 270:
                        self.field[self.active+j] = symb_cyan

                j = self.tetromino_index_count(j, i)
                i += 1

        def new(self):
            self.line_checker()

            self.rotate = 0
            self.active = self.center()
            self.tetromino = self.next
            self.next = self.get_tetromino()

            self.draw_tetromino()
            self.block = False
            self.can_rotation = True

        def move(self):
            if self.check_let(offset=row*2):
                self.slow()

            if self.check_let():
                self.end_turn()
                return

            self.active += row
            self.draw_tetromino()

        def shift(self, line):
            for l in reversed(range(1, line+1)):
                a = l*row
                b = a+row
                c = (l-1)*row
                d = c+row 
                self.field[a:b] = self.field[c:d]
                self.field[c:d] = [symb_field]*row

        def fast(self):
            self.speed = speed_acceleration
        def slow(self):
            self.speed_update()
        def boost(self):
            if self.speed == speed_acceleration:
                self.slow()
            else:
                self.fast()

        def left(self):
            x = self.find_x_cell(left=True)
            if x > 0:
                if not self.check_let(offset=-1-row):
                    self.active -= 1
                    self.draw_tetromino()

        def right(self):
            x = self.find_x_cell(right=True)
            if x < row-1:
                if not self.check_let(offset=1-row):
                    self.active += 1
                    self.draw_tetromino()

        def find_x_cell(self, left=False, right=False):
            m = []
            i = 0
            x = 0
            for cell in self.field:
                for color in coloring:
                    if cell == color:
                        x,y = self.coordinate_index(i)
                        m.append(x) 
                i += 1

            if m != []:
                if left:
                    x = min(m)
                elif right:
                    x = max(m)

            return x

        def outward(self):
            j = self.tetromino_index_start()
            k = 0 
            for cell in self.tetromino:
                if cell:
                    i = self.active+j
                    x,y = self.coordinate_index(i)
                    xx, yy = self.coordinate()
                    if xx >= row-3:
                        if x == 0:
                            return True
                j = self.tetromino_index_count(j, k)
                k += 1
            return False

        def check_let(self, offset=0):
            j = self.tetromino_index_start()
            k = 0 
            for cell in self.tetromino:
                if cell:
                    i = (self.active+j)+row+offset
                    x,y = self.coordinate_index(i)
                    if y <= column-1:
                        for color in coloring:
                            if self.field[i] == color.lower():
                                return True
                    else:
                        return True
                j = self.tetromino_index_count(j, k)
                k += 1
            return False

        def check_let_for_skip(self, offset=0):
            j = self.tetromino_index_start()
            k = 0
            for cell in self.tetromino:
                if cell:
                    i = (self.active+j)+row+offset
                    x,y = self.coordinate_index(i)
                    if y <= column-1:
                        for color in coloring:
                            if self.field[i] == color.lower():
                                return self.active+offset
                    else:
                        return self.active+offset
                j = self.tetromino_index_count(j, k)
                k += 1

        def skip(self):
            self.can_skip = False
            for c in range(column):
                s = self.check_let_for_skip(offset=row*c)
                if s:
                    break

            self.active = s
            self.draw_tetromino()
            self.end_turn()

        def can_skip_reload(self):
            self.can_skip = True

        def tetromino_index_start(self):
            l = len(self.tetromino)
            j = 0 if l == 8 else -1
            return j

        def tetromino_index_count(self, j, i):
            l = len(self.tetromino)

            if self.rotate == 90:
                if i == 1 or i == 3:
                    j += row-2

            elif self.rotate == 180:
                if l == 6:
                    if j == 1:
                        j += row-3
                elif l == 8:
                    j += row-1

            elif self.rotate == 270:
                if i == 1 or i == 3:
                    j += row-2

            else:
                if l == 4:
                    if j == 0:
                        j += row-2
                elif l == 8:
                    pass

                else:
                    if j == 1:
                        j += row-3
            j += 1
            return j

        def coordinate(self):
            i = self.active
            y = i // row 
            x = i - y*row
            return x,y

        def coordinate_index(self, i):
            y = i // row 
            x = i - y*row
            return x,y

        def hardening(self):
            i = 0
            for cell in self.field:
                for color in coloring:
                    if cell == color:
                        self.field[i] = color.lower()
                i+=1

        def rotation(self):
            l = len(self.tetromino)
            temp = self.tetromino[:]
            temp_rotate = self.rotate

            if l == 8:
                self.rotate = 180 if not self.rotate else False
            elif l == 6:
                if not self.rotate:
                    self.rotate = 90
                    if self.tetromino == [1,0,0, 1,1,1]:
                        self.tetromino = [1,1, 1,0, 1,0]
                    elif self.tetromino == [0,0,1, 1,1,1]:
                        self.tetromino = [1,0, 1,0, 1,1]
                    elif self.tetromino == [0,1,1, 1,1,0]:
                        self.tetromino = [1,0, 1,1, 0,1]
                    elif self.tetromino == [1,1,0, 0,1,1]:
                        self.tetromino = [0,1, 1,1, 1,0]
                    elif self.tetromino == [0,1,0, 1,1,1]:
                        self.tetromino = [1,0, 1,1, 1,0]

                elif self.rotate == 90:
                    self.rotate = 180
                    if self.tetromino == [1,1, 1,0, 1,0]:
                        self.tetromino = [1,0,0, 1,1,1]
                    elif self.tetromino == [1,0, 1,0, 1,1]:
                        self.tetromino = [0,0,1, 1,1,1]
                    elif self.tetromino == [1,0, 1,1, 0,1]:
                        self.tetromino = [0,1,1, 1,1,0] 
                    elif self.tetromino == [0,1, 1,1, 1,0]:
                        self.tetromino = [1,1,0, 0,1,1]
                    elif self.tetromino == [1,0, 1,1, 1,0]:
                        self.tetromino = [0,1,0, 1,1,1]

                    self.tetromino = self.tetromino[::-1]
                
                elif self.rotate == 180:
                    self.rotate = 270
                    if self.tetromino == [1,1,1, 0,0,1]:
                        self.tetromino = [0,1, 0,1, 1,1]
                    elif self.tetromino == [1,1,1, 1,0,0]:
                        self.tetromino = [1,1, 0,1, 0,1]
                    elif self.tetromino == [0,1,1, 1,1,0]: 
                        self.tetromino = [1,0, 1,1, 0,1]
                    elif self.tetromino == [1,1,0, 0,1,1]:
                        self.tetromino = [0,1, 1,1, 1,0]
                    elif self.tetromino == [1,1,1, 0,1,0]:
                        self.tetromino = [0,1, 1,1, 0,1]

                else:
                    self.rotate = 0
                    self.tetromino = self.tetromino[::-1]

                    if self.tetromino == [1,1, 1,0, 1,0]:
                        self.tetromino = [1,0,0, 1,1,1]
                    elif self.tetromino == [1,0, 1,0, 1,1]:
                        self.tetromino = [0,0,1, 1,1,1]
                    elif self.tetromino == [1,0, 1,1, 0,1]:
                        self.tetromino = [0,1,1, 1,1,0]
                    elif self.tetromino == [0,1,1, 1,1,0]:
                        self.tetromino = [1,1, 0,0, 1,1]
                    elif self.tetromino == [1,0, 1,1, 1,0]:
                        self.tetromino = [0,1,0, 1,1,1]

            if self.check_let(offset=-row) or self.check_let() or self.outward():
                self.rotate = temp_rotate
                self.tetromino = temp[:]

            self.draw_tetromino()

        def center(self):
            return int(row/2)

        def stats_update(self, line):
            self.lines += line
            self.lines_counter += line
            if self.lines_counter >= for_level:
                self.level += 1
                self.point += 100 * self.level
                self.lines_counter -= for_level
                self.speed_update()
            point = 100 if line == 1 else 300 if line == 2 else 700 if line == 3 else 1500
            self.point += point
            if line == 4 and self.mode:
                self.bonus += 1
        
        def speed_update(self):
            self.speed = self.start_speed - (self.level*0.01) if self.start_speed - (self.level*0.01) > speed_limit else speed_limit

        def line_checker(self):
            checker = 0
            clear_line = 0
            for line in range(column):
                for cell in range(row):
                    
                    for color in coloring:
                        if self.field[(line*row)+cell] == color.lower():
                            checker += 1

                    if checker == row:
                        self.shift(line)
                        clear_line += 1
                checker = 0

            if clear_line > 0:
                renpy.vibrate(1.0)
                self.stats_update(clear_line)

        def highscore_update(self):
            if persistent.highscore == [] or self.point > persistent.highscore[-1]:
                persistent.highscore.append(self.point)
                persistent.highscore.sort(reverse=True)
                if len(persistent.highscore) > tops:
                    persistent.highscore = persistent.highscore[:tops]

        def end_checker(self):
            for c in range(row):
                for color in coloring:
                    if self.field[row+c] == color.lower():
                        self.end = True
                        break

        def end_turn(self):
            self.slow()
            self.can_rotation = False
            self.hardening()
            self.end_checker()
            self.point += self.level
            self.block = True
            if self.end:
                self.highscore_update()
                renpy.hide_screen('draw_tetris')
                renpy.show_screen('game_over')

        def restart(self):
            self.level = store.level
            self.mode = store.mode
            self.field = ['·']*(row*column)
            self.speed = self.start_speed
            self.active = 0
            self.block = True
            self.can_rotation = True
            self.lines_counter = 0
            self.lines = 0
            self.point = 0
            self.bonus = 0
            self.end = False
            self.speed_update()

    def draw_next(n):
        t = ''
        l = len(n)
        i = 0
        for cell in n:
            if cell:
                # O
                if n == [1,1, 1,1]:
                    t += '{image=yellow.png}'
                # I
                elif n == [1,1,1,1, 0,0,0,0]:
                    t += '{image=purple.png}'
                # J
                elif n == [1,0,0, 1,1,1]:
                    t += '{image=blue.png}'
                # L
                elif n == [0,0,1, 1,1,1]:
                    t += '{image=orange.png}'
                # S
                elif n == [0,1,1, 1,1,0]:
                    t += '{image=green.png}'
                # Z
                elif n == [1,1,0, 0,1,1]:
                    t += '{image=red.png}'
                # T
                elif n == [0,1,0, 1,1,1]:
                    t += '{image=cyan.png}'
            else:
                t += '{image=empty.png}'

            if l == 4:
                if i == 1:
                    t += '\n'
            elif l == 6:
                if i == 2:
                    t += '\n'            
            elif l == 8:
                if i == 3:
                    t += '\n'            
            i+=1

        return t

    key_left = False
    key_right = False
    import pygame
    class KeyCatcher(renpy.Displayable):
        def render(self,w,h,st,at):
            return Null().render(w,h,st,at)
        def event(self, event, x, y, st):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    store.key_left = True
                elif event.key == pygame.K_RIGHT:
                    store.key_right = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    store.key_left = False
                elif event.key == pygame.K_RIGHT:
                    store.key_right = False

    def brightness(image, b=0.2):
        return im.MatrixColor(image, im.matrix.brightness(b))

image im_key = KeyCatcher()

### TETRIS DRAW SCREEN ###
screen draw_tetris():
    frame xysize 750,940 align .5,.5:
        add 'im_key'
        add '#fff' size 550, 930 xpos 0
        frame xysize 35*row,35*column yalign .5 xalign .37 xanchor .5:
            add 'back.jpg' align .5,.5 size 35*row,35*column

        vbox yalign .5 xalign .37 xanchor .5:
            for clm in range(column):
                hbox:
                    for cell in tetris.field[row*clm : row*(clm+1)]:

                        if cell == symb_red or cell == symb_red.lower():
                            add 'red.png'
                        elif cell == symb_green or cell == symb_green.lower():
                            add 'green.png'
                        elif cell == symb_blue or cell == symb_blue.lower():
                            add 'blue.png'

                        elif cell == symb_yellow or cell == symb_yellow.lower():
                            add 'yellow.png'
                        elif cell == symb_cyan or cell == symb_cyan.lower():
                            add 'cyan.png'
                        elif cell == symb_purple or cell == symb_purple.lower():
                            add 'purple.png'
                        elif cell == symb_orange or cell == symb_orange.lower():
                            add 'orange.png'

                        else:
                            add 'empty.png'

        if renpy.variant("small"):
            $ vboxalign = (1.26, .2)
        else:
            $ vboxalign = (1.18, .2)

        vbox align vboxalign xsize 140:
            text 'NEXT:' xanchor 1.0
            text '%s'%(draw_next(tetris.next)) xanchor 1.0
            
            null height 60
            text 'LEVEL:' xanchor 1.0
            text '%s'%(tetris.level) xanchor 1.0 
            text 'LINES:' xanchor 1.0
            text '%s'%(tetris.lines) xanchor 1.0
            text 'SCORE:' xanchor 1.0
            text '%s'%(tetris.point) xanchor 1.0
            
            text 'HIGHS:' xanchor 1.0
            $ highscore = persistent.highscore[0] if persistent.highscore != [] else 0
            text '%s'%(highscore) xanchor 1.0
            
            if tetris.mode:
                null height 50
                text 'BONUS:' xanchor 1.0
                text '%s'%(tetris.bonus) xanchor 1.0

    # ANDROID
    if renpy.variant("small"):
        button background 'gui/left.png' hover_background brightness('gui/left.png') xysize 250, 250 focus_mask True action Function(tetris.left) align .03,.9
        button background 'gui/right.png' hover_background brightness('gui/right.png') xysize 250, 250 focus_mask True action Function(tetris.right) align .195,.9
        button background 'gui/down.png' hover_background brightness('gui/down.png') xysize 250, 250 focus_mask True action Function(tetris.boost) align .81,.9
        button background 'gui/rotate.png' hover_background brightness('gui/rotate.png') xysize 250, 250 focus_mask True action If(tetris.can_rotation, Function(tetris.rotation)) align .97,.9
        if tetris.bonus:
            button background 'gui/bonus.png' hover_background brightness('gui/bonus.png') xysize 250, 250 focus_mask True action Function(tetris.delete) align .89,.5

    # PC
    else:
        if tetris.can_skip:
            key 'K_RETURN' action Function(tetris.skip)
        else:
            timer .2 action Function(tetris.can_skip_reload)
            
        if tetris.can_rotation:
            key 'mousedown_1' action Function(tetris.rotation)
            key 'K_UP' action Function(tetris.rotation)
        if tetris.bonus:
            key 'mousedown_2' action Function(tetris.delete)
            key 'K_SPACE' action Function(tetris.delete)
        
        key 'mousedown_3' action Function(tetris.boost)
        key 'mouseup_3' action Function(tetris.slow)
        key 'K_DOWN' action Function(tetris.boost)

        key 'K_RIGHT' action Function(tetris.right)
        if key_right:
            use keydown_right_move

        key 'K_LEFT' action Function(tetris.left)
        if key_left:
            use keydown_left_move

    use tetromino_animation

screen keydown_right_move():
    timer 0.05 repeat True action Function(tetris.right)
screen keydown_left_move():
    timer 0.05 repeat True action Function(tetris.left)
screen tetromino_animation():
    timer tetris.speed repeat True action If(tetris.block, Function(tetris.new), Function(tetris.move))

### GAME OVER SCREEN ###
screen game_over():
    add '#000'
    vbox align (.5,.45) xsize 500:
        text 'GAME OVER' size 50 xalign .5
        text 'LEVEL: [tetris.level]' size 40 xalign .5
        text 'LINES: [tetris.lines]' size 40 xalign .5
        text 'SCORE: [tetris.point]' size 40 xalign .5
        null height 20
        $ i = 1
        for highscore in persistent.highscore:
            if highscore == tetris.point:
                text 'top [i]: [highscore]' size 45 xalign .5 color '#f00'
            else:
                text 'top [i]: [highscore]' size 40 xalign .5 
            $ i += 1
    textbutton 'RETRY' action Hide('game_over'), Jump('tetris_reload') align .5,.9

label tetris_start:
    call screen difficulty_choice

    $ tetris = Tetris(speed=speed, mode=mode, level=level, bonus=0)
    $ tetris.speed_update()
    if impossible:
        $ tetris.delete_I()

    call screen draw_tetris

label tetris_reload:
    $ tetris.restart()
    call screen draw_tetris


init python:
    def set_mode_classic():
        store.row = 10
        store.column = 20
        store.speed = 0.4
    def set_mode_new():
        store.row = 12
        store.column = 25
        store.speed = 0.3
        store.mode = True
    def set_mode_hard():
        store.row = 13
        store.column = 25
        store.speed = 0.2
        store.mode = True
    def set_mode_impos():
        store.row = 15
        store.column = 26
        store.speed = 0.2
        store.impossible = True

screen difficulty_choice():
    vbox align .5,.5 spacing 30:
        button background '#888' hover_background '#fff' xysize 800,200 action Function(set_mode_classic), Return():
            text 'Classic' align .5,.5 size 60 color '#000'
        button background '#888' hover_background '#fff' xysize 800,200 action Function(set_mode_new), Return():
            text 'New' align .5,.5 size 60 color '#000'
        button background '#888' hover_background '#fff' xysize 800,200 action Function(set_mode_hard), Return():
            text 'Hardcore' align .5,.5 size 60 color '#000'
        button background '#888' hover_background '#fff' xysize 800,200 action Function(set_mode_impos), Return():
            text 'Impossible' align .5,.5 size 60 color '#000'

#################################################################################
# by sDextra 
#################################################################################
# 1110011 1000100 1100101 1111000 1110100 1110010 1100001
#################################################################################
