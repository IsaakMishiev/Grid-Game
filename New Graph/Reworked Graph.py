from re import T
import pygame, sys, numpy, random, pymunk, time
from math import *
from pymunk import Vec2d
from sympy import *


pygame.init()

screenY = 600
screenX = 1500
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Graph")
space = pymunk.Space()  
space.gravity = (0, -1)
COLLTYPE_BALL = 2
run_physics = False

# ======== Colors =========
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
white = (255, 255, 255)
black = (0, 0, 0)
orange = [255, 99, 71]
yellow = [255, 255, 0]
grey = (150, 150, 150)
colors = [red, blue, green, orange, black]
clock = pygame.time.Clock()

font = pygame.font.Font(None, 38)
font1 = pygame.font.Font('freesansbold.ttf', 15)
click = 0
interval = 150

def cord_to_pixel(x, y):
    return x * (screenX / grid.max_Lx) + grid.x0, y * -(screenY / grid.max_Ly) + grid.y0

def pixel_to_cord(x, y):
    return (x-grid.x0)/(screenX/ grid.max_Lx), -(y-grid.y0)/(screenY/ grid.max_Ly)


class Typewriter:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.all_lines = [self.text]
        if "/" in self.text:
            line_index = self.text.index("/")
            self.all_lines = []
            self.all_lines.append(self.text[:line_index])
            self.all_lines.append(self.text[line_index+1: ])

    def draw(self):
        pygame.draw.rect(screen, grey, (self.x+7, self.y+7, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 3)


        for num, i in enumerate(self.all_lines):
            text = font1.render((i), True, black)
            text_rect = text.get_rect(center=(self.width/2, self.height/2))
            screen.blit(text, (text_rect[0] + self.x, text_rect[1] + self.y + num*font1.size(i)[1]-10))



class Level:
    def __init__(self, all_spawn_cord, all_stars_cord, active_graphs, num, text):
        self.all_spawn_cord = all_spawn_cord
        self.all_stars_cord = all_stars_cord
        self.num = num
        self.active_graphs = active_graphs
        self.all_stars = []
        self.text = text
        self.new_text = Typewriter(screenX-425, 25, 400, 75, self.text, white)


    def set_level(self, reset):        
        global dynamic, all_curves, run_physics
        calc_points()
        for i in dynamic:
            space.remove(i)
        dynamic = []
        self.all_stars = []
        run_physics = False
        menu.launch_button.greyed = False

        for i in self.all_spawn_cord:
            dynamic.append(create_dynamic(i[0], i[1]))
        for i in self.all_stars_cord:
            self.all_stars.append(Star((i[0], i[1])))

        
        self.new_text.draw()

        if not reset:         
            all_curves = []
            for i in range(len(self.active_graphs)):
                new_curve = Curve(i)
                new_curve.color = random.choice(colors)
                new_curve.type.content = self.active_graphs[i]
                all_curves.append(new_curve)


class Star:
    def __init__(self, pos):
        self.pos = pos

        self.collected = False
    def draw(self):
        if not self.collected:
            self.posc = cord_to_pixel(self.pos[0], self.pos[1])
            pygame.draw.circle(screen, yellow, (self.posc[0], self.posc[1]), 10)
            pygame.draw.circle(screen, black, (self.posc[0], self.posc[1]), 10, 1)
    def collide(self):
        for ball in dynamic:
            ballx, bally = cord_to_pixel(ball.body.position[0], ball.body.position[1])
            dist = sqrt((ballx-self.posc[0])**2+(bally-self.posc[1])**2)        # pythag to find dist
            if dist <= 20:
                self.collected = True

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.outline_color = black
        self.outline_width = 4
        self.selected = False
        self.greyed = False


    def draw(self):

        if self.selected:
            self.outline_color = yellow

        else:
            self.outline_color = black


        if self.greyed:
            self.color = grey
        else:
            self.color = light_blue


        pygame.draw.rect(screen, grey, (self.x+5, self.y+5, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), self.outline_width)


        text = font.render((self.text), True, black)
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        screen.blit(text, (text_rect[0] + self.x, text_rect[1]+ self.y))

    def mouseon(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calc_pos(self):
        (self.xc, self.yc) = cord_to_pixel(self.x, self.y)


class Grid:
    def __init__(self):
        self.startx = -15
        self.endx = 15
        self.starty = -10
        self.endy = 10
        self.max_Lx = self.endx - self.startx

    def draw(self):
        self.max_Lx = self.endx - self.startx
        self.max_Ly = self.endy - self.starty
        self.x0 = (self.endx + self.startx) * -(screenX / (self.max_Lx * 2)) + screenX/2
        self.y0 = (self.endy + self.starty) * (screenY / (self.max_Ly * 2)) + screenY/2

        (self.x0c, self.y0c) = pixel_to_cord(self.x0, self.y0)

        for i in range(int(self.startx), int(self.endx)+1):
            x = i * (screenX / self.max_Lx)
            pygame.draw.line(screen, grey, (self.x0 + x , 0), (self.x0 + x , screenY))
            cords = font1.render(str(i), True, black)
            screen.blit(cords,(self.x0 + x+5, self.y0+5))

        for i in range(int(self.starty), int(self.endy)+1):
            y = i * (screenY / self.max_Ly)
            pygame.draw.line(screen, grey, (0 , self.y0 - y), (screenX , self.y0 - y))
            cords = font1.render(str(i), True, black)
            screen.blit(cords,(self.x0+5, self.y0 - y+5))

        pygame.draw.line(screen, black, (self.x0, 0), (self.x0, screenY), 5)
        pygame.draw.line(screen, black, (0, self.y0), (screenX, self.y0), 5)


class Type:
    def __init__(self, x, y, width, height, color, start_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.content = ""
        self.selected = False
        self.index = 0
        self.start_text = start_text

        self.shadow = False

    def draw(self):

        if self.selected:
            self.outline_color = yellow

        else:
            self.outline_color = black
        if self.shadow:
            pygame.draw.rect(screen, grey, (self.x+5, self.y+5, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), 3)

        if self.selected:
            self.location = font.size(self.content[:self.index])[0] + self.x + font.size(self.start_text)[0]
            pygame.draw.line(screen, black, (self.location+self.width//20, self.y+self.height//4), (self.location+self.width//20, self.y + self.height - self.height//4))


        self.text = font.render(self.start_text + self.content, True, black)
        screen.blit(self.text, (self.x+self.width//20, self.y+self.height//3))

    def mouseon(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False


class Menu:
    def __init__(self):
        self.menu = True
        self.protrusion = screenX//3.75
        self.v_p = 0
        self.launch_button = Button(self.protrusion-150, screenY-75, 125, 50, light_blue, "Launch!")
        self.reset_button = Button(self.protrusion-300, screenY-75, 125, 50, light_blue, "Reset")
        self.next_button = Button(screenX-175, screenY-75, 150, 50, light_blue, "Next Level")
        self.settings_button = Button(self.protrusion-375, screenY-75, 50, 50, light_blue, "||")

        self.close_menu = Button(self.protrusion, screenY-30, 30, 30, white, "<")
        self.open_menu = Button(self.protrusion, screenY-30, 30, 30, white, ">")

        self.pause = False
        self.interval_type = Type(screenX/2-100, screenY//2+75, 200, 50, light_blue, "Interval: ")
        self.pause_text = Button(screenX//2-50, -screenY//4+screenY//2+15, 100, 50, light_blue, "Pause")
        self.close_settings = Button(screenX//2-screenX//4+screenX//2-50, -screenY//4+screenY//2+15, 35, 35, light_blue, "X")
        
        self.change_level = Button(screenX//2-screenX//4+screenX//2-700, -screenY//4+screenY//2+100, 200, 50, light_blue, "Change Level")
        self.interval_type.content = "150"


    def draw(self):
        global interval

        self.protrusion += self.v_p

        self.reset_button.x = self.protrusion-300
        self.launch_button.x = self.protrusion-150
        self.settings_button.x = self.protrusion-375

        self.close_menu.x = self.protrusion
        self.open_menu.x = self.protrusion

        pygame.draw.rect(screen, grey, (7, 7, self.protrusion, screenY))
        pygame.draw.rect(screen, white, (0, 0, self.protrusion, screenY))
        pygame.draw.rect(screen, black, (0, 0, self.protrusion, screenY), 5)

        if self.menu:
            self.launch_button.draw()
            self.reset_button.draw()
            self.settings_button.draw()
            for i in all_curves:
                i.draw()

            self.close_menu.draw()
        else:
            self.open_menu.draw()

        if self.protrusion <= 0 or self.protrusion == screenX//3.75: 
            self.v_p = 0



        if self.pause:
            self.menu = False
            try:
                interval = int(self.interval_type.content)
            except: pass
            pygame.draw.rect(screen, light_blue, (0, 0, screenX, screenY))
            pygame.draw.rect(screen, grey, (screenX//2+7-screenX//4, screenY//2+7-screenY//4, screenX//2, screenY//2))
            pygame.draw.rect(screen, white, (screenX//2-screenX//4, screenY//2-screenY//4, screenX//2, screenY//2))
            pygame.draw.rect(screen, black, (screenX//2-screenX//4, screenY//2-screenY//4, screenX//2, screenY//2), 5)
            self.interval_type.draw()
            self.close_settings.draw()
            self.change_level.draw()
            self.pause_text.draw()





class Curve:
    def __init__(self, pos):
        self.pos = pos
        self.restriction_button = Button(menu.protrusion-70, self.pos*75+15, 50, 50, light_blue, "{}")
        self.type = Type(5, self.pos*75, menu.protrusion-10, 75, white, "y = ")

        self.from_restriction = Type(menu.protrusion + 10 , self.pos*75+15, 100, 50, light_blue, "")
        self.to_restriction = Type(menu.protrusion +200, self.pos*75+15, 100, 50, light_blue, "")
        self.info_button = Button(menu.protrusion + 117  , self.pos*75+15, 75, 50, light_blue, "< x <")
        self.from_restriction.shadow, self.to_restriction.shadow = True, True

        self.color = red

        self.i_restriction = grid.startx
        self.f_restriction = grid.endx

    def draw(self):

        self.type.width = menu.protrusion-10
        self.restriction_button.x = menu.protrusion-70

        if self.restriction_button.selected:
            self.from_restriction.draw()
            self.to_restriction.draw()
            self.info_button.draw()


        self.type.draw()
        self.restriction_button.draw()
        try:
            self.i_restriction = int(self.from_restriction.content)
        except: self.i_restriction = grid.startx
        try:
            self.f_restriction = int(self.to_restriction.content)
        except: self.f_restriction = grid.endx



def create_dynamic(x, y):
    body = pymunk.Body(1, 100)
    body.position = (x, y)
    shape = pymunk.Circle(body, .35, (0, 0))
    shape.friction = 0
    shape.collision_type = COLLTYPE_BALL
    space.add(body, shape)
    return shape

def create_static(x1, y1, x2, y2):
    p1 = Vec2d(x1, y1)
    p2 = Vec2d(x2, y2)
    shape = pymunk.Segment(space.static_body, p1, p2, 0.0)
    space.add(shape)
    return shape


dynamic = []
static = []

def draw_dynamic():
    for ball in dynamic:
        pygame.draw.circle(screen, red, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10)
        pygame.draw.circle(screen, black, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10, 1)

def calc_points():
    global all_points
    all_points = []
    steps = grid.max_Lx / interval

    for i in range(len(all_curves)):
        all_points.append([])

        for x in numpy.arange(all_curves[i].i_restriction, all_curves[i].f_restriction, steps):
            try:
                all_points[i].append(Point(x, float(eval(all_curves[i].type.content))))
            except:
                pass

def draw_line():
    global static
    for i in static:
        space.remove(i)
    static = []

    for i in all_points:
        color = all_curves[all_points.index(i)].color
        for j in range(1, len(i)):
            pygame.draw.line(screen, color, (i[j].xc, i[j].yc), (i[j-1].xc, i[j-1].yc), 4)
            static.append(create_static(i[j].x, i[j].y, i[j-1].x, i[j-1].y))

def typing_register(event, typer, restrict):
    if event.key == pygame.K_BACKSPACE:
        if typer.index  != 0:
            typer.content = typer.content[:typer.index-1]+typer.content[typer.index:]
            typer.index -= 1
            calc_points()

    elif event.key == pygame.K_LEFT:
        if typer.index != 0:
            typer.index -= 1

    elif event.key == pygame.K_RIGHT:
        if typer.index != len(typer.content):
            typer.index += 1

    else:
        if event.unicode.isalnum() or event.unicode in ("*", "+", "/", "-", "(", ")", "!", ".", " "):
            if typer.index != restrict:
                typer.content = typer.content[:typer.index] + event.unicode + typer.content[typer.index:]
                typer.index += 1
                calc_points()

grid = Grid()
menu = Menu()

curve1 = Curve(0)
curve2 = Curve(1)
curve3 = Curve(2)
all_curves = [curve1] 
all_points = []
calc_points()


grade9 = [
Level([(0, 5)], [(0, 3), (0, 2)], [""], 1, "Use gravity to collect all the stars using the ball,/for this level just press launch"),                         
Level([(5, 8)], [(1, 3), (0, 2)], [""], 2, "Try giding the ball using functions and press launch!"),                        
Level([(5, 5), (-5, 5)], [(2, 1), (-2, 1)], [""], 3, "When you have a function selected,/press enter to draw a new one"),
Level([(0, 8)], [(4, -2), (.5, 3), (.8, 2), (1.2, 1.2), (2, .4)], ["(x-2)**2", "x - 6"], 4, "Restrict the parobala to make a ramp"),            
Level([(5, 5), (-5, 5)], [(2, 1.5), (-2, 1.5), (0, -5)], ["(x-3.1)**2"], 5, "Symmetry"),                        
Level([(1, 9)], [(4, 0), (6, 1), (8, 2), (10, 3)], [""], 6, ""), # another ez line level
Level([(5, 8)], [(0, 5), (9, 3.3), (5, 0)], [""], 7, ""), 
Level([(-8, 8)], [(0, 3), (-8, -4), (0, -6)], [""], 8, ""), # donkey kong level
Level([(9, 5)], [(7, 2.5), (8, 3), (3, 1.5), (-5, -5)], ["ln(x)"], 9, ""), 
Level([(10, 10)], [(7, 2), (3, 3.5), (3, 2), (4.5, 2.9)], [""], 10, ""), 
Level([(-9, 8)], [(-1, 5), (-2, 2), (-9, 1.5)], [""],  11, ""),
Level([(-9, 8)], [(-1, 5), (-2, 2), (-9, 1.5)], [""],  12, "")
]

grade10 = [
]

grade11 = [
Level([(8,3.9)],[(2,2),(0.5,1)],["x"],1,""), # sqrt(x)
Level([(6,5.7)],[(3,4),(2,3.3),(0.45,1.8)],["x"],2,""), # sqrt(x)*2
Level([(-3,6.5)],[(-2,3.3),(-1,1.3), (2,-1), (4, -2)],["x**2 / 2"],3,"Try thinking about restrictions again."), # y=x^2 restriction at x=0
Level([(8,5)],[(6,4.2),(4,3.5),(2,2.2),(1,0.7),(-1,-2)],["log(x)*2"],4,""), # log(x)*2
Level([(5,6)],[(4,4),(3,2.2),(2,1.2),(1,0.8),(-1,0.4),(-3,-0.2)],["x**3 / 25"],5,"The simplest solution is usually the best."), # x**3 / 25
Level([(0.8,9)],[(1,2),(2,1),(4,0.5),(6,0.4),(8,0.3)],["1/x"],6,""), # 1/x * 5
Level([(-5,6)],[(1,2),(2,1),(4,0.5),(6,0.4),(8,0.3)],["5**2 + 5**2 = r**2"],7,"") # 1/x * 5
]

grade12 = [
]



def intro():
    global all_levels
    global current_level
    #print((screenX - 700) // 3)
    buttons = []
    for i in range(4):
        buttons.append(Button(200 + 300 * i, 400, 125, 50, light_blue, "Grade " + str(i + 9)))
    eType = []
    selectedGrade = 0
    while not selectedGrade:

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():

            eType = event.type
            if eType == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(white)
        [x.draw() for x in buttons]

        screen.blit(pygame.font.Font(None, 64).render("Select your preferred difficulty.", True, black), [screenX / 2 - 370, screenY / 2 - 100])
        clock.tick(60)
        pygame.display.update()

        if eType == pygame.MOUSEBUTTONDOWN:
            for i in buttons:
                if i.mouseon(mouse):
                    selectedGrade = int(i.text.split()[1])
                    print(selectedGrade)
                    all_levels = [grade9, grade10, grade11, grade12][selectedGrade - 9]
                    break

    eType = None
    buttons = []
    row1 = [9 if len(all_levels) > 9 else len(all_levels)][0]
    print(row1)
    for i in range(row1):
        buttons.append(Button(50 + 150 * i, 300, 125, 50, light_blue, str(i+1)))


    if row1 >= 9:
        row2 = len(all_levels) - row1
        for i in range(row2):
            buttons.append(Button(50 + 150 * i, 400, 125, 50, light_blue, str(i+10)))

    selectedLevel = -1
    while selectedLevel < 0:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen.fill(white)
            [x.draw() for x in buttons]

            screen.blit(pygame.font.Font(None, 64).render("Select your level.", True, black), [screenX / 2 - 250, screenY / 2 - 100])
            clock.tick(60)
            pygame.display.update()
            time.sleep(0.1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    if i.mouseon(mouse):
                        selectedLevel = int(i.text)
                        print(selectedLevel)
                        current_level = selectedLevel
                        all_levels[current_level-1].set_level(False)
                        break
intro()

all_levels[current_level-1].set_level(False)
level_passed = True



while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if level_passed and menu.next_button.mouseon(mouse):
                all_curves, all_points = [], []
                current_level += 1
                all_levels[current_level-1].set_level(False)

            if menu.menu and menu.reset_button.mouseon(mouse):
                all_levels[current_level-1].set_level(True)

            if menu.menu and menu.launch_button.mouseon(mouse):
                for i in all_curves:
                    i.type.selected = False
                    i.restriction_button.selected = False
                run_physics = True
                menu.launch_button.greyed = True

            if menu.menu and menu.close_menu.mouseon(mouse):
                menu.v_p = - 5
                menu.menu = False
                for i in all_curves:
                    i.restriction_button.selected = False
                    i.type.selected = False

            if menu.menu and menu.settings_button.mouseon(mouse):
                menu.pause = True
                run_physics = False
                for i in all_curves:
                        i.restriction_button.selected = False
                        i.type.selected = False

            if menu.pause and menu.change_level.mouseon(mouse):
                menu.pause = False
                menu.menu = True
                intro()
                break

            if menu.pause and menu.close_settings.mouseon(mouse):
                menu.pause = False
                menu.menu = True

            if menu.pause and menu.interval_type.mouseon(mouse):
                if not menu.interval_type.selected:
                    menu.interval_type.selected = True
                else:
                    menu.interval_type.seleced = False

            if not menu.menu and menu.open_menu.mouseon(mouse) and menu.protrusion < 200:
                menu.v_p = 5
                menu.menu = True

            for i in all_curves:
                if i.type.mouseon(mouse) and not i.restriction_button.mouseon(mouse):
                    if i.type.selected:
                        i.type.selected = False
                    else:
                        i.type.selected = True
                        i.restriction_button.selected = False
                        i.to_restriction.selected = False
                        i.from_restriction.selected = False
                        for j in all_curves:
                            if j != i:
                                j.restriction_button.selected = False       # unselects everything
                                j.type.selected = False


                elif i.restriction_button.mouseon(mouse): 
                    if i.restriction_button.selected:

                        i.restriction_button.selected = False

                    else:
                        i.restriction_button.selected = True
                        i.to_restriction.selected = False
                        i.from_restriction.selected = False
                        i.type.selected = False

                        for j in all_curves:
                            if j != i:
                                j.restriction_button.selected = False       # unselects everything
                                j.type.selected = False

                if i.restriction_button.selected:
                    if i.to_restriction.mouseon(mouse):
                        if i.to_restriction.selected:
                            i.to_restriction.selected = False
                        else:
                            i.to_restriction.selected = True
                            i.type.selected = False
                            i.from_restriction.selected = False

                            for j in all_curves:
                                if j != i:
                                    j.restriction_button.selected = False       # unselects everything
                                    j.type.selected = False

                    elif i.from_restriction.mouseon(mouse):
                        if i.from_restriction.selected:
                            i.from_restriction.selected = False
                        else:
                            i.from_restriction.selected = True
                            i.type.selected = False
                            i.to_restriction.selected = False

                            for j in all_curves:
                                if j != i:
                                    j.restriction_button.selected = False       # unselects everything
                                    j.type.selected = False


        if event.type == pygame.KEYDOWN:
            if menu.pause:
                if menu.interval_type.selected:
                    typing_register(event, menu.interval_type, 4)


            for i in all_curves:
                if i.type.selected:
                    typing_register(event, i.type, 20)

                    if event.key == pygame.K_RETURN:
                        new_curve = Curve(i.pos+1)
                        new_curve.color = random.choice(colors)
                        all_curves.append(new_curve)

                if i.restriction_button.selected:
                    if i.from_restriction.selected:
                        typing_register(event, i.from_restriction, 6)

                    elif i.to_restriction.selected:
                        typing_register(event, i.to_restriction, 6)



        if event.type == pygame.MOUSEBUTTONUP:
            calc_points()
            click = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if menu.menu:
                    menu.v_p = - 5
                    menu.menu = False
                    for i in all_curves:
                        i.restriction_button.selected = False
                        i.type.selected = False

                else:
                    menu.v_p = 5
                    menu.menu = True

            elif event.key == pygame.K_SPACE:
                if run_physics:
                    run_physics = False
                else:
                    run_physics = True

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()




    screen.fill(white)
    grid.draw()
    for i in all_points:
        for j in i:
            j.calc_pos()
    draw_line()
    draw_dynamic()


    def drag():    
        global click
        if pygame.mouse.get_pressed()[0]:   
            pygame.mouse.set_cursor(9)
            rel_pos = pygame.mouse.get_rel()
            if click != 0:
                addx = rel_pos[0]/(screenX/ grid.max_Lx)
                addy = rel_pos[1]/(screenY/ grid.max_Ly)

                grid.startx -= addx
                grid.endx -= addx
                grid.starty += addy
                grid.endy += addy

            click+=1

    for i in all_levels:
        if i.num == current_level:
            amount_collected = 0
            for j in i.all_stars:
                j.draw()
                j.collide()
                if j.collected:
                    amount_collected += 1

                if amount_collected == len(i.all_stars):
                    level_passed = True
                else:
                    level_passed = False



    if mouse[0] <= menu.protrusion - 11 and menu:
        for i in all_curves:
            if 0 <= mouse[0] <= menu.protrusion and i.pos*75 <= mouse[1] <= i.pos*75 + 75:
                if i.type.selected:
                    pygame.mouse.set_cursor(1)
                else:
                    pygame.mouse.set_cursor(11)
            if mouse[1] > len(all_curves)*75:
                pygame.mouse.set_cursor(0)
    else:
        pygame.mouse.set_cursor(3)

    if menu.menu and mouse[0] >= menu.protrusion:
        drag()
    elif not menu.menu:
        drag()

    if level_passed:
        menu.next_button.draw()

    fps = int(clock.get_fps())

    if run_physics:
        space.step(1/25)

    for i in all_levels:
        if i.num == current_level:
            if i.text != "":
                i.new_text.draw()

    menu.draw()

    clock.tick(60)
    pygame.display.update()