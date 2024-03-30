import pygame
import sys
from math import floor, ceil

pygame.init()

FPS = 60

GRID_SIZE = (100, 80)
PREFFERED_PIXEL_SIZE = (1000, 800)
MIN_HEIGHT = 800
MAX_HEIGHT = 800
NODE_GAP = 0

BACKGROUND_COLOR = (255, 255, 255)
BUTTON_PLACE_COLOR = (240, 240, 240)
NODE_COLOR = (220, 220, 220)

TEXT_COLOR = (255, 255, 255)
PRESSED_BUTTON_COLOR = (213, 213, 255)
HOVERED_OVER_BUTTON_COLOR = (183, 183, 255)
NORMAL_BUTTON_COLOR = (153, 153, 255)
BUTTON_SIZE = (80, 50)
BUTTON_PLACE_SIZE = BUTTON_SIZE[0] + 20

ANIMATION_FRAME_CYCLE = 0
ANIMATION_SPEED = 40

STRAIGHT_WEIGHT = 10
DIAGONAL_WEIGHT = 14

DRAW_WIDTH = 1

def update_all_positions(NEW_GRID_X_SIZE, NEW_GRID_Y_SIZE):
    if NEW_GRID_X_SIZE < 10 or NEW_GRID_Y_SIZE < 10 or NEW_GRID_X_SIZE > 999 or NEW_GRID_Y_SIZE > 999 or (NEW_GRID_X_SIZE / NEW_GRID_Y_SIZE) > 2:
        pass
    else:
        global GRID_SIZE, NODE_PIXEL_SIZE, GRID_WIDTH, WIDTH, HEIGHT, NODE_AMOUNT, ANIMATION_FRAME_SPEED, grid
        GRID_SIZE = (NEW_GRID_X_SIZE, NEW_GRID_Y_SIZE)

        NODE_PIXEL_SIZE = min(ceil(PREFFERED_PIXEL_SIZE[0] / GRID_SIZE[0]), ceil(PREFFERED_PIXEL_SIZE[1] / GRID_SIZE[1]))
        NODE_PIXEL_SIZE = max(NODE_PIXEL_SIZE, round(MIN_HEIGHT / GRID_SIZE[1]))
        NODE_PIXEL_SIZE = min(NODE_PIXEL_SIZE, round(MAX_HEIGHT / GRID_SIZE[1]))

        GRID_WIDTH = GRID_SIZE[0] * NODE_PIXEL_SIZE + (GRID_SIZE[0] + 1) * NODE_GAP
        WIDTH = GRID_WIDTH + BUTTON_PLACE_SIZE
        HEIGHT = GRID_SIZE[1] * NODE_PIXEL_SIZE + (GRID_SIZE[1] + 1) * NODE_GAP

        NODE_AMOUNT = (GRID_SIZE[0] * GRID_SIZE[1]) / 30000
        ANIMATION_FRAME_SPEED = ceil(ANIMATION_SPEED * NODE_AMOUNT)

        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        grid = Grid()
        grid.draw(True)

        global start_text, end_text, wall_text, clear_text
        start_text = Button("START", 24, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE + 10, 10), BUTTON_SIZE))
        end_text = Button("END", 24, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE + 10, 20 + BUTTON_SIZE[1]), BUTTON_SIZE))
        wall_text = Button("WALL", 24, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE + 10, 30 + BUTTON_SIZE[1] * 2), BUTTON_SIZE))
        clear_text = Button("CLEAR", 24, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE + 10, 40 + BUTTON_SIZE[1] * 3), BUTTON_SIZE))

        global mode_button_group
        mode_button_group = pygame.sprite.Group()
        mode_button_group.add(start_text, end_text, wall_text, clear_text)
        start_text.press()

        global clear_all_text, reset_text, run_text
        clear_all_text = Button("CLEARALL", 20, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE + 10, 50 + BUTTON_SIZE[1] * 4), BUTTON_SIZE), (255, 140, 140), (255, 170, 170), (255, 200, 200))
        reset_text = Button("RESET", 20, pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, HEIGHT - 100), (BUTTON_SIZE[0], 30)))
        run_text = Button("RUN", 30, pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, HEIGHT - 60), BUTTON_SIZE), (130, 255, 130), (150, 255, 150), (180, 255, 180))

        global algo_select
        algo_select = DropDownButton("ALGO:", ["DIJKSTRA", "ASTAR"], 20, pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, 60 + BUTTON_SIZE[1] * 5), BUTTON_SIZE), (150, 123, 255), (170, 153, 255), (200, 183, 255))
        algo_select.select("DIJKSTRA")
        
        global animation_slider, width_slider
        animation_slider = Slider("ANIM SPEED", pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, HEIGHT - 140), (BUTTON_SIZE[0], BUTTON_SIZE[1] - 30)), [1, 100], ANIMATION_SPEED)
        width_slider = Slider("DRAW WIDTH", pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, HEIGHT - 200), (BUTTON_SIZE[0], BUTTON_SIZE[1] - 30)), [1, 10], DRAW_WIDTH)

        global x_size_window, y_size_window
        x_size_window = TextEnterWindow("X SIZE", pygame.Rect((WIDTH - BUTTON_SIZE[0] - 15, HEIGHT - 300), (BUTTON_SIZE[0] // 2, BUTTON_SIZE[1] - 20)), 3, (200, 200, 200), (225, 225, 225), (250, 250, 250))
        y_size_window = TextEnterWindow("Y SIZE", pygame.Rect((WIDTH - BUTTON_SIZE[0] + 35, HEIGHT - 300), (BUTTON_SIZE[0] // 2, BUTTON_SIZE[1] - 20)), 3, (200, 200, 200), (225, 225, 225), (250, 250, 250))

        global grid_size_button
        grid_size_button = Button("SET SIZE", 20, pygame.Rect((WIDTH - BUTTON_SIZE[0] - 10, HEIGHT - 260), (BUTTON_SIZE[0], BUTTON_SIZE[1] - 25)), (180, 180, 180), (200, 200, 200), (220, 220, 220))

        global ALL_BUTTONS
        ALL_BUTTONS = [start_text, end_text, wall_text, clear_text, clear_all_text, reset_text, run_text, grid_size_button]

def get_pixel_size(pos):
    return [pos[0] * NODE_PIXEL_SIZE + (pos[0] + 1) * NODE_GAP, pos[1] * NODE_PIXEL_SIZE + (pos[1] + 1) * NODE_GAP]

def get_grid_pos(pos):
    x, y = pos[0], pos[1]
    if x >= GRID_WIDTH or y >= HEIGHT:
        return [-1, -1]

    grids_taken, gaps_taken = 0, 0
    i = 0
    temp = 1
    while 1:
        temp = x - NODE_PIXEL_SIZE * i - NODE_GAP * (i + 1)
        if (temp < NODE_PIXEL_SIZE):
            break
        i += 1
    if temp < 0:
        return [-1, -1] 
    x = i
    i = 0
    while 1:
        temp = y - NODE_PIXEL_SIZE * i - NODE_GAP * (i + 1)
        if (temp < NODE_PIXEL_SIZE):
            break
        i += 1
    if temp < 0:
        return [-1, -1] 
    y = i
    return [x, y]


class Node:
    def __init__(self, pos):
        self.str = "CLEAR"
        self.pos = pos
        self.pixel_pos = get_pixel_size(pos)
        self.surf = pygame.Surface((NODE_PIXEL_SIZE, NODE_PIXEL_SIZE))
        self.surf.fill(NODE_COLOR)
        self.rect = self.surf.get_rect(topleft = tuple(self.pixel_pos))
    def set_point(self, str):
        if str == "START":
            self.surf.fill((0, 255, 0))
        elif str == "END":
            self.surf.fill((255, 0, 0))
        elif str == "WALL":
            self.surf.fill((50, 50, 50))
        elif str == "CLEAR":
            self.surf.fill(NODE_COLOR)
        self.str = str
    

class Grid:
    def __init__(self):
        self.NodeList = [[Node((j, i)) for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
        self.start_point = [-1, -1]
        self.end_point = [-1, -1]
        self.walls = []
        self.changed_pos = None
        self.prev_mouse_pos = None
        self.prev_mouse_pressed = False

    def clear(self, x, y):
        if self.start_point == [x, y]:
            self.start_point = [-1, -1]
        if self.end_point == [x, y]:
            self.end_point = [-1, -1]
        if self.NodeList[y][x].str == "WALL":
            self.walls.remove([x, y])
        self.NodeList[y][x].set_point("CLEAR")
        self.changed_pos.append([x, y])
        
    def set_point(self, x, y, str):
        if str == "START":
            if self.start_point != [-1, -1] and self.NodeList[y][x].str != "START":
                self.clear(self.start_point[0], self.start_point[1])
            self.start_point = [x, y]
        elif str ==  "END":
            if self.end_point != [-1, -1] and self.NodeList[y][x].str != "END":
                self.clear(self.end_point[0], self.end_point[1])
            self.end_point = [x, y]
        elif str == "WALL":
            if self.NodeList[y][x].str != "WALL":
                self.clear(x, y)
                self.walls.append([x, y])
                self.NodeList[y][x].set_point(str)
        elif str == "CLEAR":
            self.clear(x, y)
        if str == "WALL" or str == "CLEAR" and DRAW_WIDTH != 1:
            left = top = floor((DRAW_WIDTH - 1) / 2 - 0.5)
            right = bottom = floor((DRAW_WIDTH - 1) / 2 + 0.5)
            for cur_x in range(-left, right + 1):
                for cur_y in range(-top, bottom + 1):
                    pos = [x + cur_x, y + cur_y]
                    if pos[0] < 0 or pos[0] >= GRID_SIZE[0] or pos[1] < 0 or pos[1] >= GRID_SIZE[1]:
                        continue
                    if str == "WALL":
                        if self.NodeList[pos[1]][pos[0]].str != "WALL":
                            self.clear(pos[0], pos[1])
                            self.walls.append(pos)
                            self.NodeList[pos[1]][pos[0]].set_point(str)
                    elif str == "CLEAR":
                        self.clear(pos[0], pos[1])
        self.NodeList[y][x].set_point(str)
        
    def update(self, mouse_pos, mouse_pressed):
        if not mouse_pressed:
            self.prev_mouse_pressed = False
            self.prev_mouse_pos = mouse_pos
            return
        if not self.prev_mouse_pressed:
            self.prev_mouse_pos = mouse_pos    
        grid_pos = get_grid_pos(mouse_pos)
        if grid_pos == [-1, -1]:
            return
        prev_grid_pos = get_grid_pos(self.prev_mouse_pos)
        x_diff = grid_pos[0] - prev_grid_pos[0]
        y_diff = grid_pos[1] - prev_grid_pos[1]
        if x_diff != 0:
            x_add = int(x_diff / abs(x_diff))
        if y_diff != 0:
            y_add = int(y_diff / abs(y_diff))
        while prev_grid_pos[0] != grid_pos[0] or prev_grid_pos[1] != grid_pos[1]:
            self.set_point(prev_grid_pos[0], prev_grid_pos[1], CHOSEN_MODE)
            self.changed_pos.append(prev_grid_pos.copy())
            if prev_grid_pos[0] != grid_pos[0]:
                prev_grid_pos[0] += x_add
            if prev_grid_pos[1] != grid_pos[1]:
                prev_grid_pos[1] += y_add
        self.set_point(grid_pos[0], grid_pos[1], CHOSEN_MODE)
        self.changed_pos.append(grid_pos)
        self.prev_mouse_pos = mouse_pos
        self.prev_mouse_pressed = True

    def draw(self, full = False):
        if full:
            screen.fill(BACKGROUND_COLOR)
            for i in range(GRID_SIZE[1]):
                for j in range(GRID_SIZE[0]):
                    screen.blit(self.NodeList[i][j].surf, self.NodeList[i][j].rect)
            pygame.display.flip()
            self.changed_pos = []
            return
        for pos in self.changed_pos:
            changed_node = self.NodeList[pos[1]][pos[0]]
            screen.blit(changed_node.surf, changed_node.rect)
            pygame.display.update(changed_node.rect)
        self.changed_pos.clear()

    def pathfind(self):
        self.animation_nodes = []
        class ANode:
            def __init__(self, parent, pos, weight, start_weight):
                self.parent = parent
                self.pos = pos
                self.weight = weight
                self.start_weight = start_weight
            def copy(self, node):
                self.parent = node.parent
                self.weight = node.weight
                self.start_weight = node.start_weight

        node_list = [ANode(None, grid.start_point, 0, 0)]
        closed = [[False for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
        walls = [[False for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
        for wall in self.walls:
            walls[wall[1]][wall[0]] = True
            closed[wall[1]][wall[0]] = True

        def get_idx(val):
            left, right = 0, len(node_list) - 1
            if left > right: 
                return 0
            while left <= right:
                mid = (left + right) // 2
                if val < node_list[mid].weight:
                    if mid == 0 or node_list[mid - 1].weight < val:
                        return max(0, mid - 1)
                    else:
                        right = mid - 1
                elif val > node_list[mid].weight:
                    if mid == (len(node_list) - 1) or node_list[mid + 1].weight > val:
                        return mid + 1
                    else:
                        left = mid + 1
                else:
                    while mid > 0 and node_list[mid - 1].weight == val:
                        mid -= 1
                    return mid
                
        def remove_if_needed(new_node):
            if node_grid[new_node.pos[1]][new_node.pos[0]] != None and node_grid[new_node.pos[1]][new_node.pos[0]].weight <= new_node.weight:
                return
            if node_grid[new_node.pos[1]][new_node.pos[0]] != None:
                existing_node =  node_grid[new_node.pos[1]][new_node.pos[0]]
                idx = node_list.index(existing_node)
                existing_node.copy(new_node)
                while idx > 0 and node_list[idx - 1].weight > existing_node.weight:
                    temp = node_list[idx - 1]
                    node_list[idx - 1] = existing_node
                    node_list[idx] = temp
                    idx -= 1
            else:
                node_list.insert(get_idx(new_node.weight), new_node)
                node_grid[new_node.pos[1]][new_node.pos[0]] = new_node

        if CHOSEN_ALGO == 'DIJKSTRA':
            node_grid = [[None for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
            while len(node_list) > 0:
                top_node = node_list[0]
                closed[top_node.pos[1]][top_node.pos[0]] = True
                self.animation_nodes.append(top_node.pos)
                node_list.pop(0)

                positions = [[top_node.pos[0] + 1, top_node.pos[1]], [top_node.pos[0] - 1, top_node.pos[1]],[top_node.pos[0], top_node.pos[1] + 1],[top_node.pos[0], top_node.pos[1] - 1]]
                diagonal_positions = [[top_node.pos[0] + 1, top_node.pos[1] + 1], [top_node.pos[0] - 1, top_node.pos[1] + 1],[top_node.pos[0] + 1, top_node.pos[1] - 1],[top_node.pos[0] - 1, top_node.pos[1] - 1]]
                all_positions = positions + diagonal_positions
                for pos in all_positions:
                    new_weight = top_node.start_weight + (STRAIGHT_WEIGHT if pos in positions else DIAGONAL_WEIGHT)
                    if pos[0] < 0 or pos[0] >= GRID_SIZE[0] or pos[1] < 0 or pos[1] >= GRID_SIZE[1] or closed[pos[1]][pos[0]]:
                        continue
                    if pos in diagonal_positions:
                        if walls[pos[1]][top_node.pos[0]] and walls[top_node.pos[1]][pos[0]]:
                            continue
                    new_node = ANode(top_node, pos, new_weight, new_weight)
                    remove_if_needed(new_node)

                    if pos == self.end_point:
                        normal_list = []
                        new_node_copy = new_node
                        while new_node_copy != None:
                            normal_list.insert(0, new_node_copy.pos)
                            new_node_copy = new_node_copy.parent
                        return normal_list
                    
        elif CHOSEN_ALGO == 'ASTAR':
            node_grid = [[None for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
            while len(node_list) > 0:
                top_node = node_list[0]
                closed[top_node.pos[1]][top_node.pos[0]] = True
                self.animation_nodes.append(top_node.pos)
                node_list.pop(0)

                positions = [[top_node.pos[0] + 1, top_node.pos[1]], [top_node.pos[0] - 1, top_node.pos[1]],[top_node.pos[0], top_node.pos[1] + 1],[top_node.pos[0], top_node.pos[1] - 1]]
                diagonal_positions = [[top_node.pos[0] + 1, top_node.pos[1] + 1], [top_node.pos[0] - 1, top_node.pos[1] + 1],[top_node.pos[0] + 1, top_node.pos[1] - 1],[top_node.pos[0] - 1, top_node.pos[1] - 1]]
                all_positions = positions + diagonal_positions
                for pos in all_positions:

                    new_start_weight = top_node.start_weight + (STRAIGHT_WEIGHT if pos in positions else DIAGONAL_WEIGHT)
                    x_diff = abs(self.end_point[0] - pos[0])
                    y_diff = abs(self.end_point[1] - pos[1])
                    new_end_weight = min(x_diff, y_diff) * DIAGONAL_WEIGHT + abs(x_diff - y_diff) * STRAIGHT_WEIGHT
                    new_weight = new_start_weight + new_end_weight

                    if pos[0] < 0 or pos[0] >= GRID_SIZE[0] or pos[1] < 0 or pos[1] >= GRID_SIZE[1] or closed[pos[1]][pos[0]]:
                        continue
                    if pos in diagonal_positions:
                        if walls[pos[1]][top_node.pos[0]] and walls[top_node.pos[1]][pos[0]]:
                            continue

                    new_node = ANode(top_node, pos, new_weight, new_start_weight)
                    remove_if_needed(new_node)
                    if pos == self.end_point:
                        normal_list = []
                        new_node_copy = new_node
                        while new_node_copy != None:
                            normal_list.insert(0, new_node_copy.pos)
                            new_node_copy = new_node_copy.parent
                        return normal_list   

class Button(pygame.sprite.Sprite):
    def __init__(self, str, font_size, background_rect, normal_button_color = NORMAL_BUTTON_COLOR, hovered_button_color = HOVERED_OVER_BUTTON_COLOR, pressed_button_color = PRESSED_BUTTON_COLOR):
        super().__init__()
        self.str = str
        self.text_font = pygame.font.SysFont('Calibri', font_size) 
        self.text = self.text_font.render(str, True, TEXT_COLOR)
        self.notpressed_rect =  pygame.Rect(background_rect)
        self.pressed_rect = self.notpressed_rect.inflate((-(self.notpressed_rect.width / 20), -(self.notpressed_rect.height / 15)))
        self.rect = self.notpressed_rect
        self.normal_color = normal_button_color
        self.hovered_color = hovered_button_color
        self.presed_color = pressed_button_color
        self.rect_color = self.normal_color
        self.mouse_on = False
        self.pressed = False
        self.last_update = pygame.time.get_ticks()

    def press(self):
        if self.pressed:
            return
        global drawing_active
        self.rect = self.pressed_rect
        self.rect_color = self.presed_color
        self.pressed = True

        groups = self.groups()
        if len(groups) > 0:
            sprite_list = groups[0].sprites()
            for i in range(len(sprite_list)):
                if sprite_list[i] != self:
                    sprite_list[i].unpress()
            if groups[0] is mode_button_group:
                global CHOSEN_MODE
                CHOSEN_MODE = self.str
            elif groups[0] is algo_select.drop_button_group:
                global CHOSEN_ALGO
                CHOSEN_ALGO = self.str

        if self.str == "RUN" and (grid.start_point != [-1, -1] and grid.end_point != [-1, -1]):
            global edit_phase
            edit_phase = False
            self.unpress()
            if drawing_active:
                reset_text.press()
        elif self.str == "CLEARALL":
            for i in range(GRID_SIZE[1]):
                for j in range(GRID_SIZE[0]):
                    grid.NodeList[i][j].set_point("CLEAR")
            grid.start_point = [-1, -1]
            grid.end_point = [-1, -1]
            grid.walls.clear()
            grid.draw(True)
            self.unpress()
        elif self.str == "RESET":
            grid.NodeList = [[Node((j, i)) for j in range(GRID_SIZE[0])] for i in range(GRID_SIZE[1])]
            grid.NodeList[grid.start_point[1]][grid.start_point[0]].set_point("START")
            grid.NodeList[grid.end_point[1]][grid.end_point[0]].set_point("END")
            for wall in grid.walls:
                grid.NodeList[wall[1]][wall[0]].set_point("WALL")
            grid.draw(True)
            self.unpress()
            drawing_active = False
        elif self.str == "SET SIZE":
            x_size = x_size_window.current_num
            y_size = y_size_window.current_num
            update_all_positions(x_size, y_size)
            self.unpress()

    def unpress(self):
        if not self.pressed:
            return
        self.rect = self.notpressed_rect
        self.rect_color = self.normal_color
        self.pressed = False
        groups = self.groups()
        if len(groups) > 0:
            if groups[0] is mode_button_group:
                global CHOSEN_MODE
                CHOSEN_MODE = ""
            elif groups[0] is algo_select.drop_button_group:
                global CHOSEN_ALGO
                CHOSEN_ALGO = ""
                
    def update(self, mouse_pos, mouse_pressed):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < 200:
            return False
        hover = self.rect.contains(pygame.Rect(mouse_pos, (0, 0)))
        if hover:
            if mouse_pressed:
                if self.pressed:
                    self.unpress()
                else:
                    self.press()
                self.last_update = pygame.time.get_ticks()
                return self.pressed
            else:
                self.rect_color = self.hovered_color
            self.mouse_on = True
        else:
            if self.mouse_on == True:
                self.rect_color = self.presed_color if self.pressed else self.normal_color
                self.rect = self.pressed_rect if self.pressed else self.notpressed_rect
                self.mouse_on = False
        return False

class DropDownButton():
    def __init__(self, main_string, drop_strings, font_size, background_rect, normal_button_color = NORMAL_BUTTON_COLOR, hovered_button_color = HOVERED_OVER_BUTTON_COLOR, pressed_button_color = PRESSED_BUTTON_COLOR):
        self.main_button = Button(main_string, font_size, background_rect, normal_button_color, hovered_button_color, pressed_button_color)
        self.drop_button_group = pygame.sprite.Group()
        temp_rect = pygame.Rect(background_rect)
        for str in drop_strings:
            temp_rect.y += background_rect.height
            drop_button = Button(str, font_size, pygame.Rect(temp_rect), normal_button_color, hovered_button_color, pressed_button_color)
            self.drop_button_group.add(drop_button)
    def update(self, mouse_pos, mouse_pressed):
        self.main_button.update(mouse_pos, mouse_pressed)
        if self.main_button.pressed:
            drop_down_list = self.drop_button_group.sprites()
            for i in range(len(drop_down_list)):
                drop_down_list[i].update(mouse_pos, mouse_pressed)
                if drop_down_list[i].pressed:
                    self.main_button.str = drop_down_list[i].str
                    self.main_button.text = self.main_button.text_font.render(self.main_button.str, True, TEXT_COLOR)
    def select(self, str):
        drop_down_list = self.drop_button_group.sprites()
        for i in range(len(drop_down_list)):
            if drop_down_list[i].str == str:
                drop_down_list[i].press()
                self.main_button.text = self.main_button.text_font.render(str, True, TEXT_COLOR)
                return
    def draw(self):
        pygame.draw.rect(screen, self.main_button.rect_color, self.main_button.rect)
        screen.blit(self.main_button.text, self.main_button.text.get_rect(center = self.main_button.rect.center))
        pygame.display.update(self.main_button.notpressed_rect)
        if self.main_button.pressed:
            button_list = self.drop_button_group.sprites()
            for i in range(len(button_list)):
                pygame.draw.rect(screen, button_list[i].rect_color, button_list[i].rect)
                screen.blit(button_list[i].text, button_list[i].text.get_rect(center = button_list[i].rect.center))
                pygame.display.update(button_list[i].notpressed_rect)

class Slider:
    def __init__(self, string, rect, range, start_x):
        self.string = string
        self.font = pygame.font.SysFont('Calibri', 16)
        self.surf = self.font.render(string, True, (30, 30, 30))
        self.rect = pygame.Rect(rect)
        self.range = range
        self.line_pos = [[rect.left, rect.centery], [rect.right, rect.centery]]
        percent = (start_x / (range[1] - range[0]))
        self.moving_x = ((rect.right - rect.left) * percent) + rect.left
    def update(self, mouse_pos, mouse_pressed):
        if not mouse_pressed:
            return
        hover = self.rect.contains(pygame.Rect(mouse_pos, (0, 0)))
        if not hover:
            return
        x_diff = mouse_pos[0] - self.rect.left
        percent = x_diff / self.rect.width
        if percent < 0 or percent > 100:
            return
        self.moving_x = round(((self.rect.right - self.rect.left) * percent) + self.rect.left)
        current_val = self.range[0] + round((self.range[1] - self.range[0]) * percent)
        if self.string == "ANIM SPEED":
            global ANIMATION_FRAME_SPEED
            ANIMATION_FRAME_SPEED = ceil(current_val * NODE_AMOUNT)
        elif self.string == "DRAW WIDTH":
            global DRAW_WIDTH
            DRAW_WIDTH = current_val
    def draw(self):
        screen.blit(self.surf, self.surf.get_rect(center = (self.rect.centerx, self.rect.top - 10)))
        pygame.draw.line(screen, (150, 150, 200), (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 2)
        surf = pygame.Surface((5, self.rect.height))
        surf.fill((50, 50, 50))
        screen.blit(surf, surf.get_rect(center = (self.moving_x, self.rect.centery)))
        pygame.display.update(pygame.Rect((self.rect.left - 10, self.rect.top - 20), (self.rect.width + 40, self.rect.height + 40)))

class TextEnterWindow:
    def __init__(self, str, rect, max_symbols, normal_color, hovered_color, pressed_color):
        self.str = str
        self.button = Button("", 14, rect, normal_color, hovered_color, pressed_color)
        self.current_num = GRID_SIZE[0] if str == "X SIZE" else GRID_SIZE[1]
        self.last_update = pygame.time.get_ticks()
        self.last_key_pressed = -1
        self.text = self.button.text_font.render(str, True, (30, 30, 30))
    def update(self, mouse_pos, mouse_pressed, keys_pressed):
        if self.button.update(mouse_pos, mouse_pressed):
            if self.str == "X SIZE": 
                if y_size_window.button.pressed:
                    y_size_window.button.unpress()
            elif self.str == "Y SIZE":
                if x_size_window.button.pressed:
                    x_size_window.button.unpress()
        if self.button.pressed:
            current_time = pygame.time.get_ticks()
            for key in range(pygame.K_0, pygame.K_9 + 1):
                if not keys_pressed[key]:
                    continue
                if self.current_num >= 100:
                    break
                if self.last_key_pressed == key:
                    if current_time - self.last_update < 200:
                        continue
                self.last_update = current_time
                self.last_key_pressed = key
                self.current_num = self.current_num * 10 + (key - pygame.K_0)
            if keys_pressed[pygame.K_BACKSPACE]:
                if self.last_key_pressed != pygame.K_BACKSPACE or current_time - self.last_update > 100:
                    self.current_num = self.current_num // 10
                    self.last_key_pressed = pygame.K_BACKSPACE
                    self.last_update = current_time
        self.button.text = self.button.text_font.render(str(self.current_num), True, (30, 30, 30))
    def draw(self):
        screen.blit(self.text, self.text.get_rect(center = (self.button.rect.centerx, self.button.rect.top - 6)))
        pygame.draw.rect(screen, self.button.rect_color, self.button.rect)
        screen.blit(self.button.text, self.button.text.get_rect(center = self.button.rect.center))

CHOSEN_MODE = "START"
CHOSEN_ALGO = "DIJKSTRA"

clock = pygame.time.Clock()

app_running = True
edit_phase = True
path_found = False
drawing_active = False

pygame.display.set_caption("Pathfinding")
update_all_positions(GRID_SIZE[0], GRID_SIZE[1])

while app_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    keys_pressed = pygame.key.get_pressed()

    animation_slider.update(mouse_pos, mouse_pressed)
    pygame.draw.rect(screen, BUTTON_PLACE_COLOR, pygame.Rect((WIDTH - BUTTON_PLACE_SIZE, 0), (BUTTON_PLACE_SIZE, HEIGHT)))
    animation_slider.draw()

    if edit_phase:  
        width_slider.update(mouse_pos, mouse_pressed)

        x_size_window.update(mouse_pos, mouse_pressed, keys_pressed)
        y_size_window.update(mouse_pos, mouse_pressed, keys_pressed)

        for i in range(len(ALL_BUTTONS)):
            ALL_BUTTONS[i].update(mouse_pos, mouse_pressed)
        algo_select.update(mouse_pos, mouse_pressed)
        grid.update(mouse_pos, mouse_pressed)

        grid.draw()
        for button in ALL_BUTTONS:
            pygame.draw.rect(screen, button.rect_color, button.rect)
            screen.blit(button.text, button.text.get_rect(center = button.rect.center))
        width_slider.draw()
        x_size_window.draw()
        y_size_window.draw()
        algo_select.draw()
        pygame.display.update(pygame.Rect((WIDTH - BUTTON_PLACE_SIZE, 0), (BUTTON_PLACE_SIZE, HEIGHT)))
    else:
        if not path_found:
            final_path = grid.pathfind()
            path_found = True
            idx = 0
            current_frame = 0
            drawing_active = True
        if idx < len(grid.animation_nodes):
            if current_frame != ANIMATION_FRAME_CYCLE:
                current_frame += 1
                continue
            current_frame = 0
            for i in range(ANIMATION_FRAME_SPEED):
                if idx >= len(grid.animation_nodes):
                    break
                pos = grid.animation_nodes[idx]
                if pos != grid.start_point and pos != grid.end_point:
                    node = grid.NodeList[pos[1]][pos[0]]
                    node.surf.fill((153, 153, 255))
                    screen.blit(node.surf, node.rect)
                    pygame.display.update(node.rect)
                idx += 1
        else:
            if final_path != None:
                final_path_len = len(final_path)
                for pos in final_path:
                    if pos == grid.start_point or pos == grid.end_point:
                        continue
                    grid.NodeList[pos[1]][pos[0]].surf.fill((100, 170, 100))
                    screen.blit(grid.NodeList[pos[1]][pos[0]].surf, grid.NodeList[pos[1]][pos[0]].rect)
                    pygame.display.update(grid.NodeList[pos[1]][pos[0]].rect)
                    pygame.time.wait(round(1000 / final_path_len))
            path_found = False
            edit_phase = True
    clock.tick(FPS)
