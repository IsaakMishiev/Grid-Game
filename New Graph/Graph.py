import pygame, sys, numpy, random, pymunk
from math import *
from pymunk import Vec2d
from sympy import *


pygame.init()

debug = True

screenY = 600
screenX = 1500
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Graph")
space = pymunk.Space()  
space.gravity = (0, -2)
COLLTYPE_BALL = 2
run_physics = True

# ======== Colors =========
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
orange = [255, 99, 71]
yellow = [255, 255, 0]
grey = (150, 150, 150)
colors = [red, blue, green, orange, black]
clock = pygame.time.Clock()

interval = 150

font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 15)
win_sound  = pygame.mixer.Sound('win.wav')
soft_fail  = pygame.mixer.Sound('soft_fail.wav')

all_levels = []

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 5)

        font = pygame.font.Font(None, 25)
        text = font.render((self.text), True, black)
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        screen.blit(text, (text_rect[0] + self.x, text_rect[1]+ self.y))

    def mouseon(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False
        


next_button = Button(screenX-125, screenY-75, 100, 50, blue, "Next Level")

class Level:
    def __init__(self, all_spawn_cord, all_stars_cord, active_graphs, num):
        self.all_spawn_cord = all_spawn_cord
        self.all_stars_cord = all_stars_cord
        self.num = num
        self.active_graphs = active_graphs
        self.all_stars = []
        for i in self.all_stars_cord:
            self.all_stars.append(Star((i[0], i[1])))
        global dynamic, all_types, run_physics
        dynamic = []
        all_types = []
        run_physics = False
        for i in self.all_spawn_cord:
            dynamic.append(create_dynamic(i[0], i[1]))          # run this outside this lol
        for i in range(len(self.active_graphs)):
            all_types.append(Type(i, random.choice(colors), self.active_graphs[i]))
        all_levels.append(self)

        



class Star:
    def __init__(self, pos):
        self.pos = pos
        
        self.collected = False
    def draw(self):
        if not self.collected:
            self.posc = cord_to_pixel(self.pos[0], self.pos[1])
            pygame.draw.circle(screen, yellow, (self.posc[0], self.posc[1]), 10)
    def collide(self):
        for ball in dynamic:
            ballx, bally = cord_to_pixel(ball.body.position[0], ball.body.position[1])
            dist = sqrt((ballx-self.posc[0])**2+(bally-self.posc[1])**2)
            if dist <= 20:
                self.collected = True



def cord_to_pixel(x, y):
    return x * (screenX / grid.max_Lx) + grid.x0, y * -(screenY / grid.max_Ly) + grid.y0

def pixel_to_cord(x, y):
    return (x-grid.x0)/(screenX/ grid.max_Lx), -(y-grid.y0)/(screenY/ grid.max_Ly)



class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def calc_pos(self):
        (self.xc, self.yc) = cord_to_pixel(self.x, self.y)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.xc, self.yc), 2)


class Grid:
    def __init__(self, startx, starty, endx, endy):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
    
    def render_grid(self):
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


def calc_points():
    global all_points, static
    all_points = []

    

    steps = grid.max_Lx / interval

    for i in range(len(all_types)):
        all_points.append([])
        for x in numpy.arange(all_types[i].i_restriction, all_types[i].f_restriction + 1, steps):
            try:
                all_points[i].append(Point(x, float(eval(all_types[i].content)), all_types[i].color))
            except: 
                pass

    
def draw_points():
    for i in all_points:
        for j in i:
            j.calc_pos()
            #j.draw()

def draw_line():
    global static
    for i in static:
        space.remove(i)
    static = []
    for i in all_points:
        for j in range(1, len(i)):
            pygame.draw.line(screen, i[0].color, (i[j].xc, i[j].yc), (i[j-1].xc, i[j-1].yc), 4)
            if j % 2 == 0:
                static.append(create_static(i[j].x, i[j].y, i[j-1].x, i[j-1].y))


grid = Grid(-15, -10, 15, 10)
grid.render_grid()    
   


menu = True
protrusion = screenX//4
def Menu():
    if menu == True:
        pygame.draw.rect(screen, white, (0, 0, protrusion, screenY))
        pygame.draw.rect(screen, black, (0, 0, protrusion, screenY), 5)
        for i in all_types:
            i.draw()
            i.restriction()

class Type:
    def __init__(self, pos, color, content):
        self.pos = pos
        self.color = color
        self.content = content
        self.selected = False
        self.boxcolor = black

        self.restrions = False
        self.i_restriction = grid.startx
        self.f_restriction = grid.endx
        self.r_selected = False

    def draw(self):
        if self.selected:
            self.boxcolor = yellow
        else:
            self.boxcolor = black
        pygame.draw.rect(screen, self.boxcolor, (0, self.pos*75, protrusion, 75), 3)

        self.text = font.render("y = " + self.content, True, black)
        screen.blit(self.text, (20, self.pos*75 + 20))

    def restriction(self):
        if self.r_selected:
            pygame.draw.rect(screen, black, (protrusion, self.pos*75, 150, 50), 2)
            pygame.draw.rect(screen, black, (protrusion+150, self.pos*75, 150, 50), 2)

    

def create_dynamic(x, y):
    body = pymunk.Body(1, 100)
    body.position = (x, y)
    shape = pymunk.Circle(body, .35, (0, 0))
    shape.friction = 0.5
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
        if -25 > ball.body.position[0] or -25 > ball.body.position[1]:
            dynamic.remove(ball)
            soft_fail.play()
        pygame.draw.circle(screen, red, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10)
        pygame.draw.circle(screen, black, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10, 1)



def draw_static():
    global static
    
    for line in static:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = cord_to_pixel(pv1.x, pv1.y)
        p2 = cord_to_pixel(pv2.x, pv2.y)
        pygame.draw.lines(screen, blue, False, [p1, p2])
    


first = Type(0, red, "x")
second = Type(1, blue, "tan(x)")
all_types = [first]


drag = False
point1 = None
click = 0



Level([(0, 5)], [(0, 3), (0, 2)], ["x**2 + 6"], 1) 
Level([(1, 1)], [(1, 1), (1, 1)], ["x+3"], 2) 



current_level = 1

level_passed = False



calc_points()
play = True
while play:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not drag:
                point1 = mouse
                drag = True
            
            if menu:
                for i in all_types:
                    if 0 <= mouse[0] <= protrusion and i.pos*75 <= mouse[1] <= i.pos*75 + 75:
                        if i.selected == False:
                            for j in all_types:
                                if j.selected == True:
                                    j.selected = False
                            i.selected = True
                        else:
                            i.selected = False
            
            if level_passed and next_button.mouseon(mouse):
                current_level += 1
                level_passed = False

        if event.type == pygame.MOUSEBUTTONUP:
            if drag:
                drag = False
                calc_points()
                click = 0


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_TAB:
                if menu:
                    menu = False
                else:
                    menu = True

            elif event.key == pygame.K_1:
                dynamic.append(create_dynamic(random.randint(0, 7), 5))
            
            elif event.key == pygame.K_SPACE:
                if run_physics:
                    run_physics = False
                else:
                    run_physics = True

            if menu:
                for i in all_types:
                    if i.selected:
                        if event.key == pygame.K_BACKSPACE:
                            if len(i.content) == 0:
                                del i
                            else:
                                i.content = i.content[:-1]
                                
                        elif event.key == pygame.K_RETURN:
                            all_types.append(Type(len(all_types), random.choice(colors), ""))
                        else:
                            i.content += event.unicode
                            calc_points()


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            grid.startx += .3
            grid.endx += .3
            calc_points()
        if event.key == pygame.K_LEFT:
            grid.startx += -.3
            grid.endx += -.3
            calc_points()
        if event.key == pygame.K_UP:
            grid.starty += .3
            grid.endy += .3

        if event.key == pygame.K_DOWN:
            grid.starty += -.3
            grid.endy += -.3


    if protrusion - 10 <= mouse[0] <= protrusion + 10:
        pygame.mouse.set_cursor(7)

    elif mouse[0] <= protrusion - 11 and menu:
        for i in all_types:
            if 0 <= mouse[0] <= protrusion and i.pos*75 <= mouse[1] <= i.pos*75 + 75:
                if i.selected:
                    pygame.mouse.set_cursor(1)
                else:
                    pygame.mouse.set_cursor(11)
            if mouse[1] > len(all_types)*75:
                pygame.mouse.set_cursor(0)
    else:
        pygame.mouse.set_cursor(3)
    

    if pygame.mouse.get_pressed()[0]:       # PRESS MOUSE
        if menu and protrusion - 20 <= mouse[0] <= protrusion + 20 and 200 <= mouse[0] <= 500:
            protrusion = mouse[0]
        
        if not menu or protrusion + 11 <= mouse[0]: # Drag
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
        
        
            


    #pygame.mouse.set_cursor(11)          # (7 drag left right)     (9 drag graph)  (3 looking around)    (0 normal mouse)    (11 hand select)
    
    for i in all_types:
        if not i.restrions:
            i.i_restriction = grid.startx
            i.f_restriction = grid.endx



    screen.fill(white)
    if run_physics:
        space.step(1/50)
    grid.render_grid()
    draw_points()
    draw_line()
    draw_dynamic()
    draw_static()
    Menu()

    if level_passed:
        next_button.draw()
    
    for i in all_levels:
        if i.num == current_level:
            amount_collected = 0
            for j in i.all_stars:
                j.draw()
                j.collide()
                if j.collected:
                    amount_collected += 1
                if amount_collected != len(i.all_stars) and level_passed == False:
                    win_sound.play()
                    level_passed = True


    clock.tick(165)
    #print(int(clock.get_fps()))
    pygame.display.update()
    
