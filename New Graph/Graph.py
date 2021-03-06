from re import T

import pygame, sys, numpy, random, pymunk
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
run_physics = True

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

interval = 150

font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 15)


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.greyed = False
        self.original_color = self.color
        self.outline_color = black

        self.outlight_width = 5

    def draw(self):
        if self.greyed:
            self.color = grey
        else:
            self.color = self.original_color
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), self.outlight_width)

        font = pygame.font.Font(None, 25)
        text = font.render((self.text), True, black)
        text_rect = text.get_rect(center=(self.width/2, self.height/2))
        screen.blit(text, (text_rect[0] + self.x, text_rect[1]+ self.y))

    def mouseon(self, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False
        


next_button = Button(screenX-125, screenY-75, 100, 50, light_blue, "Next Level")
reset_button = Button(25, screenY-75, 100, 50, light_blue, "Reset")
launch_button = Button(150, screenY-75, 100, 50, light_blue, "Launch!")

class Level:
    def __init__(self, all_spawn_cord, all_stars_cord, active_graphs, num):
        self.all_spawn_cord = all_spawn_cord
        self.all_stars_cord = all_stars_cord
        self.num = num
        self.active_graphs = active_graphs
        self.all_stars = []
        

    def set_level(self, reset):        
        global dynamic, all_types, run_physics
        for i in dynamic:
            space.remove(i)
        dynamic = []
        self.all_stars = []
        run_physics = False
        launch_button.greyed = False
        
        for i in self.all_spawn_cord:
            dynamic.append(create_dynamic(i[0], i[1]))
        for i in self.all_stars_cord:
            self.all_stars.append(Star((i[0], i[1])))
     
        if not reset:         
            all_types = []
            for i in range(len(self.active_graphs)):
                all_types.append(Type(i, random.choice(colors), self.active_graphs[i]))

    


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
            dist = sqrt((ballx-self.posc[0])**2+(bally-self.posc[1])**2)        # pythag to find dist
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

        for x in numpy.arange(all_types[i].i_restriction, all_types[i].f_restriction, steps):
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
v_p = 0
def Menu():
    global protrusion, v_p
    protrusion += v_p
    pygame.draw.rect(screen, white, (0, 0, protrusion, screenY))
    pygame.draw.rect(screen, black, (0, 0, protrusion, screenY), 5)
    if protrusion <= 0 or protrusion == screenX//4: 
        v_p = 0

    if menu == True and v_p == 0:
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
        self.index = 0

        
        self.i_restriction = grid.startx
        self.f_restriction = grid.endx
        self.r_selected = False

        self.restrict_button = Button(protrusion-75, self.pos*75+15, 50, 50, light_blue, "{}")      # when drawing just do .draw() for the button
        self.from_x_button = Button(protrusion+25, self.pos*75+15, 75, 50, light_blue, "")       # text
        self.to_x_button = Button(protrusion+300, self.pos*75+15, 75, 50, light_blue, "")        # text
        self.info_button = Button(protrusion+750, self.pos*75+15, 50, 5 > 750, li100t_blue, "< x <")      
  > 100       self.re[]outlight_width, self.to_x_button.outlight_width, self.info_button.outlight_width = 2, 1, 1, 1
        
        self.to_selected = False
        self.from_selected = False

        

    def draw(self):
        if self.selected:
            self.boxcolor = yellow

            self.location = font.size(self.content[:self.index])[0]

            pygame.draw.line(screen, black, (self.location+75, self.pos*75+15), (self.location+75, self.pos*75+60))
        else:
            self.boxcolor = black
        pygame.draw.rect(screen, self.boxcolor, (0, self.pos*75, protrusion, 75), 3)

        self.text = font.render("y = " + self.content, True, black)
        screen.blit(self.text, (20, self.pos*75 + 20))


    def restriction(self):
        self.restrict_button.x = protrusion - 75      # updates the x cords
        self.from_x_button.x = protrusion + 25
        self.to_x_button.x = protrusion + 155
        self.info_button.x = protrusion + 102.5
        
        self.i_restriction = grid.startx
        self.f_restriction = grid.endx
        

        self.restrict_button.draw()
        if self.r_selected:
            self.from_x_button.draw()
            self.to_x_button.draw()
            self.info_button.draw()
            self.restrict_button.outline_color = yellow
        else:
            self.restrict_button.outline_color = black

        if self.to_selected:
            self.to_x_button.outline_color = yellow
        else:
            self.to_x_button.outline_color = black
        
        if self.from_selected:
            self.from_x_button.outline_color = yellow
        else:
            self.from_x_button.outline_color = black

        try:
            self.f_restriction = int(self.to_x_button.text)
        except: 
            pass

        try:
            self.i_restriction = int(self.from_x_button.text)
        except:
            pass


    

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
click = 0                                                                       # sample levels (difficulty level 1- 10)
level1 = Level([(0, 5)], [(0, 3), (0, 2)], [""], 1)                         # 1
level2 = Level([(5, 8)], [(1, 3), (0, 2)], [""], 2)                          # 1
level3 = Level([(1, 6)], [(4, 2), (2, 5), (3, 3.5)], [""], 3)               # 3
level4 = Level([(10, 10)], [(7, 2), (3, 3.5), (3, 2), (4.5, 2.9)], [""], 4)                            # 8     (currently imposible gotta add restrictions) lvl 20 on marble slides
level5 = Level([(5, 8)], [(1, 3), (0, 2)], [""], 5) 

all_levels = [level1, level2, level3, level4, level5]
current_level = 1
level_passed = True

all_levels[0].set_level(False)


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
                    if 0 <= mouse[0] <= protrusion and i.pos*75 <= mouse[1] <= i.pos*75 + 75 and not (i.restrict_button.mouseon(mouse)):
                        if i.selected == False:
                            for j in all_types:
                                if j.selected == True:
                                    j.selected = False
                            i.selected = True
                        else:
                            i.selected = False
            
            if level_passed and next_button.mouseon(mouse):
                current_level += 1
                all_levels[current_level-1].set_level(False)
            
            if menu and reset_button.mouseon(mouse):
                all_levels[current_level-1].set_level(True)

            if menu and launch_button.mouseon(mouse):
                run_physics = True
                launch_button.greyed = True

            for i in all_types:
                if i.restrict_button.x <= mouse[0] <= i.restrict_button.x + 50 and i.restrict_button.y <= mouse[1] <= i.restrict_button.y + 50:
                    if i.r_selected:
                        i.r_selected = False
                    else:
                        i.r_selected = True

                if i.to_x_button.x <= mouse[0] <= i.to_x_button.x + 75 and i.to_x_button.y <= mouse[1] <= i.to_x_button.y + 50:
                    if i.to_selected:
                        i.to_selected = False
                    else:
                        i.to_selected = True
                        i.from_selected = False

                if i.from_x_button.x <= mouse[0] <= i.from_x_button.x + 75 and i.from_x_button.y <= mouse[1] <= i.from_x_button.y + 50:
                    if i.from_selected:
                        i.from_selected = False
                    else:
                        i.from_selected = True
                        i.to_selected = False

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
                    for i in all_types:
                        i.selected = False
                        i.to_selected = False
                        i.from_selected = False
                        i.r_selected = False
                    menu = False
                    v_p = -5
                    protrusion -= 10
                else:
                    menu = True
                    v_p = 5
            for i in all_types:
                if i .selected:
                    if event.key == pygame.K_LEFT:
                        if i.index != 0:
                            i.index -= 1
                        
                    elif event.key == pygame.K_RIGHT:
                        if i.index != len(i.content):
                            i.index += 1

                    

            #elif event.key == pygame.K_1:
                #dynamic.append(create_dynamic(random.randint(0, 7), 5))
            
            if event.key == pygame.K_SPACE:
                if run_physics:
                    run_physics = False
                else:
                    run_physics = True
                    

            if menu:
                for i in all_types:                     # TYPING
                    if i.selected:
                        if event.key == pygame.K_BACKSPACE:
                            if i.index != 0:
                                i.content = i.content[:i.index-1] + i.content[i.index:]
                                i.index -= 1
                                calc_points()
                                
                        elif event.key == pygame.K_RETURN:
                            all_types.append(Type(len(all_types), random.choice(colors), ""))
                        else:
                            if event.unicode.isalnum() or event.unicode in ("*", "+", "/", "-", "(", ")", "!", "."):
                                i.content = i.content[:i.index] + event.unicode + i.content[i.index:]
                                i.index += 1
                                calc_points()

                            
                    if i.to_selected:
                        if event.key == pygame.K_BACKSPACE:
                            i.to_x_button.text = i.to_x_button.text[:-1]
        
                        else:
                            i.to_x_button.text += event.unicode
                            calc_points()
                    
                    if i.from_selected:
                        if event.key == pygame.K_BACKSPACE:
                            i.from_x_button.text = i.from_x_button.text[:-1]
        
                        else:
                            i.from_x_button.text += event.unicode
                            calc_points()
                    


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
        if menu and protrusion - 20 <= mouse[0] <= protrusion + 20 and 300 <= mouse[0] <= 500:
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

    screen.fill(white)
    if run_physics:
        space.step(1/25)
    grid.render_grid()
    draw_points()
    draw_line()
    draw_dynamic()
    #draw_static()
    
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
                
                if amount_collected == len(i.all_stars):
                    level_passed = True
                else:
                    level_passed = False

    Menu()
    if menu:
        launch_button.x = protrusion - 225
        reset_button.x = protrusion - 350
        reset_button.draw()
        launch_button.draw()
    
    
    clock.tick(165)
    print(int(clock.get_fps()))
    pygame.display.update()
    #print(protrusion, menu, v_p)