from re import T # imports the regex module
import pygame, sys, numpy, random, pymunk, time # imports the pygame, sys, numpy, random, pymunk, and time modules
from math import * # imports the math module
from pymunk import Vec2d # imports the Vec2d module from the pymunk module

pygame.init() # initializes pygame

screenY = 600 # sets the screenY variable to 600
screenX = 1500 # sets the screenX variable to 1500
screen = pygame.display.set_mode((screenX, screenY)) # sets the screen variable to the pygame display set mode function with the screenX and screenY variables as parameters
pygame.display.set_caption("Graph") # sets the pygame display caption to "Graph"
space = pymunk.Space()  # sets the space variable to the pymunk space function
space.gravity = (0, -1) # sets the space gravity to 0, -1
COLLTYPE_BALL = 2 # sets the COLLTYPE_BALL variable to 2
run_physics = False # sets the run_physics variable to False

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
colors = [red, blue, green, orange, black] # defines the colors table to be used for the game
clock = pygame.time.Clock() # initializes the clock variable with the pygame clock object

font = pygame.font.Font(None, 38) # defines the font to be used for the game
font1 = pygame.font.Font('freesansbold.ttf', 15) # defines the secondary font to be used for the game
win = pygame.mixer.Sound('win.wav') # defines the sound to be played when the player wins
lose = pygame.mixer.Sound('soft_fail.wav') # defines the sound to be played when the player loses
clicks = pygame.mixer.Sound('click.wav') # defines the sound to be played when the player clicks on a button
click = 0 # defines the click variable to be used for the game
interval = 150 # defines the interval variable to be used for the game

def cord_to_pixel(x, y):
   '''
   Converts the coordinates of the graph to the coordinates of the screen.
   Returns the sum of two decimal numbers in binary digits.

    Parameters:
        x (float): The x coordinate of the graph.
        y (float): The y coordinate of the graph.

    Returns:
        (float, float): The x and y coordinates of the screen.
   '''
   return x * (screenX / grid.max_Lx) + grid.x0, y * -(screenY / grid.max_Ly) + grid.y0 # returns the calculated coordinates of the screen

def pixel_to_cord(x, y):
   '''
   Converts the coordinates of the screen to the coordinates of the graph.
   Returns the sum of two decimal numbers in binary digits.

    Parameters:
        x (float): The x coordinate of the screen.
        y (float): The y coordinate of the screen.

    Returns:
        (float, float): The x and y coordinates of the graph.
   '''
   return (x-grid.x0)/(screenX/ grid.max_Lx), -(y-grid.y0)/(screenY/ grid.max_Ly) # returns the calculated coordinates of the graph

class Typewriter:
   '''
   Defines the typewriter object to be used for the game.
   '''
   def __init__(self, x, y, width, height, text, color):
      '''
      Initializes the typewriter object.

       Parameters:
           x (float): The x coordinate of the screen
           y (float): The y coordinate of the screen
           width (float): The width of the typewriter
           height (float): The height of the typewriter
           text (string): The text to be written
           color (tuple): The color
      '''
      self.x = x # defines the x coordinate
      self.y = y # defines the y coordinate
      self.width = width # defines the width
      self.height = height # defines the height
      self.text = text # defines the text
      self.color = color # defines the color
      self.all_lines = [self.text] # defines the all_lines variable
      if "/" in self.text: # checks if there is a "/" in the text
         line_index = self.text.index("/") # defines the line_index variable
         self.all_lines = [] # defines the all_lines variable
         self.all_lines.append(self.text[:line_index]) # appends the first line of the text to the all_lines variable
         self.all_lines.append(self.text[line_index+1: ]) # appends the second line of the text to the all_lines variable

   def draw(self):
      '''
      Draws the text on the screen.
      
    Parameters:
        None

    Returns:
        None
      '''
      pygame.draw.rect(screen, grey, (self.x+7, self.y+7, self.width, self.height)) # draws the background of the text
      pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height)) # draws the text
      pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 3) # draws the border of the text
      for num, i in enumerate(self.all_lines): # loops through the all_lines variable
         text = font1.render((i), True, black) # defines the text variable
         text_rect = text.get_rect(center=(self.width/2, self.height/2)) # defines the text_rect variable
         screen.blit(text, (text_rect[0] + self.x, text_rect[1] + self.y + num*font1.size(i)[1]-10)) # draws the text on the screen

class Level:
   '''
   Defines the level object to be used for the game.
   '''
   def __init__(self, all_spawn_cord, all_stars_cord, active_graphs, num, text):
      '''
      Initializes the level object.

       Parameters:
           all_spawn_cord (list): The list of all the spawn coordinates
           all_stars_cord (list): The list of all the star coordinates
           active_graphs (list): The list of all the active graphs
           num (int): The level number
           text (string): The text to be written
      '''
      self.all_spawn_cord = all_spawn_cord # defines the all_spawn_cord variable
      self.all_stars_cord = all_stars_cord # defines the all_stars_cord variable
      self.num = num # defines the num variable
      self.active_graphs = active_graphs # defines the active_graphs variable
      self.all_stars = [] # defines the all_stars variable
      self.text = text # defines the text variable
      self.new_text = Typewriter(screenX-425, 25, 400, 75, self.text, white) # defines the new_text variable

   def set_level(self, reset):
      '''
      Sets the level.

       Parameters:
           reset (boolean): The boolean to check if the level is being reset

       Returns:
           None
      '''
      global dynamic, all_curves, run_physics # defines the global variables
      calc_points() # calculates the points
      for i in dynamic: # loops through the dynamic variable
         space.remove(i) # removes the i variable from the space variable
      dynamic = [] # defines the dynamic variable
      self.all_stars = [] # defines the all_stars variable
      run_physics = False # defines the run_physics variable
      menu.launch_button.greyed = False # defines the greyed variable
      for i in self.all_spawn_cord: # loops through the all_spawn_cord variable
         dynamic.append(create_dynamic(i[0], i[1])) # appends the i variable to the dynamic variable
      for i in self.all_stars_cord: # loops through the all_stars_cord variable
         self.all_stars.append(Star((i[0], i[1]))) # appends the i variable to the all_stars variable
      self.new_text.draw() # draws the text
      if not reset: # checks if the level is not being reset
         all_curves = [] # defines the all_curves variable
         for i in range(len(self.active_graphs)): # loops through the active_graphs variable
            new_curve = Curve(i) # defines the new_curve variable
            new_curve.color = random.choice(colors) # defines the color variable
            new_curve.type.content = self.active_graphs[i] # defines the content variable
            all_curves.append(new_curve) # appends the new_curve variable to the all_curves variable


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
    '''
    This class is used to create buttons.
    '''
    def __init__(self, x, y, width, height, color, text):
        '''
        This function is used to initialize the button.
        :param x: The x coordinate of the button.
        :param y: The y coordinate of the button.
        :param width: The width of the button.
        :param height: The height of the button.
        :param color: The color of the button.
        :param text: The text of the button.
        '''
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
        '''
        This function is used to draw the button.
        :param self: The button.
        :return: None.
        '''

        if self.selected: # If the button is selected, the outline color will be yellow.
            self.outline_color = yellow

        else: # If the button is not selected, the outline color will be black.
            self.outline_color = black


        if self.greyed: # If the button is greyed, the color will be grey.
            self.color = grey
        else: # If the button is not greyed, the color will be light blue.
            self.color = light_blue


        pygame.draw.rect(screen, grey, (self.x+5, self.y+5, self.width, self.height)) # Draw a grey rectangle.
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height)) # Draw a rectangle.
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), self.outline_width) # Draw a rectangle outline.


        text = font.render((self.text), True, black) # Render the text.
        text_rect = text.get_rect(center=(self.width/2, self.height/2)) # Get the center of the text.
        screen.blit(text, (text_rect[0] + self.x, text_rect[1]+ self.y)) # Draw the text.

    def mouseon(self, mouse):
        '''
        This function is used to check if the mouse is on the button.
        :param self: The button.
        :param mouse: The mouse.
        :return: True if the mouse is on the button.
        '''
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height: # If the mouse is on the button, return True.
            return True
        return False


class Point:
    '''
    This class is used to create points.
    '''
    def __init__(self, x, y):
        '''
        This function is used to initialize the point.
        :param x: The x coordinate of the point.
        :param y: The y coordinate of the point.
        '''
        self.x = x
        self.y = y

    def calc_pos(self):
        '''
        This function is used to calculate the position of the point.
        :param self: The point.
        :return: None.
        '''
        (self.xc, self.yc) = cord_to_pixel(self.x, self.y) # Calculate the position of the point.


class Grid:
    '''
    This class is used to create grids.
    '''
    def __init__(self):
        '''
        This function is used to initialize the grid.
        '''
        self.startx = -15
        self.endx = 15
        self.starty = -10
        self.endy = 10
        self.max_Lx = self.endx - self.startx

    def draw(self):
        '''
        This function is used to draw the grid.
        :param self: The grid.
        :return: None.
        '''
        self.max_Lx = self.endx - self.startx # Calculate the maximum x length.
        self.max_Ly = self.endy - self.starty # Calculate the maximum y length.
        self.x0 = (self.endx + self.startx) * -(screenX / (self.max_Lx * 2)) + screenX/2 # Calculate the x coordinate of the origin.
        self.y0 = (self.endy + self.starty) * (screenY / (self.max_Ly * 2)) + screenY/2 # Calculate the y coordinate of the origin.

        (self.x0c, self.y0c) = pixel_to_cord(self.x0, self.y0) # Calculate the position of the origin.

        for i in range(int(self.startx), int(self.endx)+1): # Draw the x axis.
            x = i * (screenX / self.max_Lx)
            pygame.draw.line(screen, grey, (self.x0 + x , 0), (self.x0 + x , screenY))
            cords = font1.render(str(i), True, black)
            screen.blit(cords,(self.x0 + x+5, self.y0+5))

        for i in range(int(self.starty), int(self.endy)+1): # Draw the y axis.
            y = i * (screenY / self.max_Ly)
            pygame.draw.line(screen, grey, (0 , self.y0 - y), (screenX , self.y0 - y))
            cords = font1.render(str(i), True, black)
            screen.blit(cords,(self.x0+5, self.y0 - y+5))

        pygame.draw.line(screen, black, (self.x0, 0), (self.x0, screenY), 5) # Draw the x axis.
        pygame.draw.line(screen, black, (0, self.y0), (screenX, self.y0), 5) # Draw the y axis.


class Type:
    '''
    This class is used to create text boxes.
    '''
    def __init__(self, x, y, width, height, color, start_text):
        '''
        This function is used to initialize the text box.
        :param x: The x coordinate of the text box.
        :param y: The y coordinate of the text box.
        :param width: The width of the text box.
        :param height: The height of the text box.
        :param color: The color of the text box.
        :param start_text: The text of the text box.
        '''
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
        '''
        This function is used to draw the text box.
        :param self: The text box.
        :return: None.
        '''

        if self.selected: # If the text box is selected, the outline color will be yellow.
            self.outline_color = yellow

        else: # If the text box is not selected, the outline color will be black.
            self.outline_color = black
        if self.shadow: # If the text box is shadowed, draw a grey rectangle.
            pygame.draw.rect(screen, grey, (self.x+5, self.y+5, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height)) # Draw a rectangle.
        pygame.draw.rect(screen, self.outline_color, (self.x, self.y, self.width, self.height), 3) # Draw a rectangle outline.

        if self.selected: # If the text box is selected, draw a line.
            self.location = font.size(self.content[:self.index])[0] + self.x + font.size(self.start_text)[0]
            pygame.draw.line(screen, black, (self.location+self.width//20, self.y+self.height//4), (self.location+self.width//20, self.y + self.height - self.height//4))


        self.text = font.render(self.start_text + self.content, True, black) # Render the text.
        screen.blit(self.text, (self.x+self.width//20, self.y+self.height//3)) # Draw the text.

    def mouseon(self, mouse):
        '''
        This function is used to check if the mouse is on the text box.
        :param self: The text box.
        :param mouse: The mouse.
        :return: True if the mouse is on the text box.
        '''
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height: # If the mouse is on the text box, return True.
            return True
        return False


class Menu:
    '''
    This class is used to create the menu.
    '''
    def __init__(self):
        '''
        This function is used to initialize the menu.
        :param self: The menu.
        :return: None.
        '''
        self.menu = True # This variable is used to determine if the menu is open or not.
        self.protrusion = screenX//3.75 # This variable is used to determine how far the menu protrudes from the left side of the screen.
        self.v_p = 0 # This variable is used to determine the speed of the menu.
        self.launch_button = Button(self.protrusion-150, screenY-75, 125, 50, light_blue, "Launch!") # Create the launch button.
        self.reset_button = Button(self.protrusion-300, screenY-75, 125, 50, light_blue, "Reset") # Create the reset button.
        self.next_button = Button(screenX-175, screenY-75, 150, 50, light_blue, "Next Level") # Create the next level button.
        self.settings_button = Button(self.protrusion-375, screenY-75, 50, 50, light_blue, "||") # Create the settings button.

        self.close_menu = Button(self.protrusion, screenY-30, 30, 30, white, "<") # Create the close menu button.
        self.open_menu = Button(self.protrusion, screenY-30, 30, 30, white, ">") # Create the open menu button.

        self.pause = False # This variable is used to determine if the game is paused or not.
        self.interval_type = Type(screenX/2-100, screenY//2+75, 200, 50, light_blue, "Interval: ") # Create the interval type.
        self.pause_text = Button(screenX//2-50, -screenY//4+screenY//2+15, 100, 50, light_blue, "Pause") # Create the pause text.
        self.close_settings = Button(screenX//2-screenX//4+screenX//2-50, -screenY//4+screenY//2+15, 35, 35, light_blue, "X") # Create the close settings button.
        
        self.change_level = Button(screenX//2-screenX//4+screenX//2-700, -screenY//4+screenY//2+100, 200, 50, light_blue, "Change Level") # Create the change level button.
        self.interval_type.content = "150" # Set the interval type to 150.


    def draw(self):
        '''
        This function is used to draw the menu.
        :param self: The menu.
        :return: None.
        '''
        global interval

        self.protrusion += self.v_p # Add the speed to the protrusion.

        self.reset_button.x = self.protrusion-300 # Set the x position of the reset button.
        self.launch_button.x = self.protrusion-150 # Set the x position of the launch button.
        self.settings_button.x = self.protrusion-375 # Set the x position of the settings button.

        self.close_menu.x = self.protrusion # Set the x position of the close menu button.
        self.open_menu.x = self.protrusion # Set the x position of the open menu button.

        pygame.draw.rect(screen, grey, (7, 7, self.protrusion, screenY)) # Draw the grey background of the menu.
        pygame.draw.rect(screen, white, (0, 0, self.protrusion, screenY)) # Draw the white background of the menu.
        pygame.draw.rect(screen, black, (0, 0, self.protrusion, screenY), 5) # Draw the black border of the menu.

        if self.menu: # If the menu is open:
            self.launch_button.draw() # Draw the launch button.
            self.reset_button.draw() # Draw the reset button.
            self.settings_button.draw() # Draw the settings button.
            for i in all_curves: # For every curve in all_curves:
                i.draw() # Draw the curve.

            self.close_menu.draw() # Draw the close menu button.
        else: # If the menu is closed:
            self.open_menu.draw() # Draw the open menu button.

        if self.protrusion <= 0 or self.protrusion == screenX//3.75: # If the protrusion is less than or equal to 0 or the protrusion is equal to the default protrusion:
            self.v_p = 0 # Set the speed to 0.



        if self.pause: # If the game is paused:
            self.menu = False # Close the menu.
            try:
                interval = int(self.interval_type.content) # Try to set the interval to the interval type.
            except: pass # If it fails, pass.
            pygame.draw.rect(screen, light_blue, (0, 0, screenX, screenY)) # Draw the light blue background.
            pygame.draw.rect(screen, grey, (screenX//2+7-screenX//4, screenY//2+7-screenY//4, screenX//2, screenY//2)) # Draw the grey background of the settings.
            pygame.draw.rect(screen, white, (screenX//2-screenX//4, screenY//2-screenY//4, screenX//2, screenY//2)) # Draw the white background of the settings.
            pygame.draw.rect(screen, black, (screenX//2-screenX//4, screenY//2-screenY//4, screenX//2, screenY//2), 5) # Draw the black border of the settings.
            self.interval_type.draw() # Draw the interval type.
            self.close_settings.draw() # Draw the close settings button.
            self.change_level.draw() # Draw the change level button.
            self.pause_text.draw() # Draw the pause text.





class Curve:
    '''
    This class is used to create the curves.
    '''
    def __init__(self, pos):
        '''
        This function is used to initialize the curves.
        :param self: The curve.
        :param pos: The position of the curve.
        :return: None.
        '''
        self.pos = pos # Set the position of the curve.
        self.restriction_button = Button(menu.protrusion-70, self.pos*75+15, 50, 50, light_blue, "{}") # Create the restriction button.
        self.type = Type(5, self.pos*75, menu.protrusion-10, 75, white, "y = ") # Create the type.

        self.from_restriction = Type(menu.protrusion + 10 , self.pos*75+15, 100, 50, light_blue, "") # Create the from restriction type.
        self.to_restriction = Type(menu.protrusion +200, self.pos*75+15, 100, 50, light_blue, "") # Create the to restriction type.
        self.info_button = Button(menu.protrusion + 117  , self.pos*75+15, 75, 50, light_blue, "< x <") # Create the info button.
        self.from_restriction.shadow, self.to_restriction.shadow = True, True # Set the shadow of the from restriction type and the to restriction type to True.

        self.color = red # Set the color of the curve to red.

        self.i_restriction = grid.startx # Set the initial restriction to the start x of the grid.
        self.f_restriction = grid.endx # Set the final restriction to the end x of the grid.

    def draw(self):
        '''
        This function is used to draw the curve.
        :param self: The curve.
        :return: None.
        '''

        self.type.width = menu.protrusion-10 # Set the width of the type.
        self.restriction_button.x = menu.protrusion-70 # Set the x position of the restriction button.

        if self.restriction_button.selected: # If the restriction button is selected:
            self.from_restriction.draw() # Draw the from restriction type.
            self.to_restriction.draw() # Draw the to restriction type.
            self.info_button.draw() # Draw the info button.


        self.type.draw() # Draw the type.
        self.restriction_button.draw() # Draw the restriction button.
        try:
            self.i_restriction = int(self.from_restriction.content) # Try to set the initial restriction to the from restriction type.
        except: self.i_restriction = grid.startx # If it fails, set the initial restriction to the start x of the grid.
        try:
            self.f_restriction = int(self.to_restriction.content) # Try to set the final restriction to the to restriction type.
        except: self.f_restriction = grid.endx # If it fails, set the final restriction to the end x of the grid.



def create_dynamic(x, y):
    '''
    This function is used to create the dynamic objects.
    :param x: The x position of the dynamic object.
    :param y: The y position of the dynamic object.
    :return: The shape of the dynamic object.
    '''
    body = pymunk.Body(1, 100) # Create the body of the dynamic object.
    body.position = (x, y) # Set the position of the body.
    shape = pymunk.Circle(body, .35, (0, 0)) # Create the shape of the dynamic object.
    shape.friction = 0 # Set the friction of the shape to 0.
    shape.collision_type = COLLTYPE_BALL # Set the collision type of the shape to COLLTYPE_BALL.
    space.add(body, shape) # Add the body and the shape to the space.
    return shape # Return the shape.

def create_static(x1, y1, x2, y2):
    '''
    This function is used to create the static objects.
    :param x1: The x position of the first point.
    :param y1: The y position of the first point.
    :param x2: The x position of the second point.
    :param y2: The y position of the second point.
    :return: The shape of the static object.
    '''
    p1 = Vec2d(x1, y1) # Create the first point.
    p2 = Vec2d(x2, y2) # Create the second point.
    shape = pymunk.Segment(space.static_body, p1, p2, 0.0) # Create the shape of the static object.
    space.add(shape) # Add the shape to the space.
    return shape # Return the shape.


dynamic = [] # Create the dynamic list.
static = [] # Create the static list.

def draw_dynamic():
    '''
    This function is used to draw the dynamic objects.
    :return: None.
    '''
    for ball in dynamic: # For every ball in dynamic:
        pygame.draw.circle(screen, red, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10) # Draw the ball.
        pygame.draw.circle(screen, black, (cord_to_pixel(ball.body.position[0], ball.body.position[1])), 10, 1) # Draw the border of the ball.

def calc_points():
    '''
    This function is used to calculate the points of the curves.
    :return: None.
    '''
    global all_points # Set the global variable all_points.
    all_points = [] # Set all_points to an empty list.

    steps = grid.max_Lx / interval # Calculate the steps.

    for i in range(len(all_curves)): # For every curve in all_curves:
        all_points.append([]) # Append an empty list to all_points.

        for x in numpy.arange(all_curves[i].i_restriction, all_curves[i].f_restriction, steps): # For every x in the range of the initial restriction and the final restriction with the steps:
            try:
                all_points[i].append(Point(x, float(eval(all_curves[i].type.content)))) # Try to append the point to all_points.
            except:
                pass # If it fails, pass.

def draw_line():
    '''
    This function is used to draw the lines.
    :return: None.
    '''
    global static # Set the global variable static.
    for i in static: # For every i in static:
        space.remove(i) # Remove i from the space.
    static = [] # Set static to an empty list.

    for i in all_points: # For every i in all_points:
        try:
            color = all_curves[all_points.index(i)].color # Try to set the color to the color of the curve in all_curves.
        except:
            pass # If it fails, pass.
        for j in range(1, len(i)): # For every j in the range of 1 and the length of i:
            pygame.draw.line(screen, color, (i[j].xc, i[j].yc), (i[j-1].xc, i[j-1].yc), 4) # Draw the line.
            static.append(create_static(i[j].x, i[j].y, i[j-1].x, i[j-1].y)) # Append the static object to static.

def typing_register(event, typer, restrict):
    '''
    This function is used to register the typing.
    :param event: The event.
    :param typer: The typer.
    :param restrict: The restrict.
    :return: None.
    '''
    if event.key == pygame.K_BACKSPACE: # If the event key is the backspace key:
        if typer.index  != 0: # If the typer index is not 0:
            typer.content = typer.content[:typer.index-1]+typer.content[typer.index:] # Set the content of the typer.
            typer.index -= 1 # Subtract 1 from the typer index.
            calc_points() # Calculate the points.

    elif event.key == pygame.K_LEFT: # If the event key is the left key:
        if typer.index != 0: # If the typer index is not 0:
            typer.index -= 1 # Subtract 1 from the typer index.

    elif event.key == pygame.K_RIGHT: # If the event key is the right key:
        if typer.index != len(typer.content): # If the typer index is not the length of the typer content:
            typer.index += 1 # Add 1 to the typer index.

    else: # If the event key is not the backspace key, the left key, or the right key:
        if event.unicode.isalnum() or event.unicode in ("*", "+", "/", "-", "(", ")", "!", ".", " "): # If the event unicode is alphanumeric or in the specified list:
            if typer.index != restrict: # If the typer index is not the restrict:
                typer.content = typer.content[:typer.index] + event.unicode + typer.content[typer.index:] # Set the content of the typer.
                typer.index += 1 # Add 1 to the typer index.
                calc_points() # Calculate the points.



grid = Grid() # Create the grid.
menu = Menu() # Create the menu.

curve1 = Curve(0) # Create the first curve.
curve2 = Curve(1) # Create the second curve.
curve3 = Curve(2) # Create the third curve.
all_curves = [curve1] # Set all_curves to a list containing the first curve.
all_points = [] # Set all_points to an empty list.
calc_points() # Calculate the points


grade9 = [ # Defines the list of Grade 9 levels.
Level([(0, 5)], [(0, 3), (0, 2)], [""], 1, "Use gravity to collect all the stars using the ball,/for this level just press launch"),                         
Level([(5, 8)], [(1, 3), (0, 2)], [""], 2, "Try giding the ball using functions and press launch!"),                        
Level([(5, 5), (-5, 5)], [(2, 1), (-2, 1)], [""], 3, "When you have a function selected,/press enter to draw a new one"),
Level([(0, 8)], [(4, -2), (.5, 3), (.8, 2), (1.2, 1.2), (2, .4)], ["(x-2)**2", "x - 6"], 4, "Restrict the parobala to make a ramp"),            
Level([(5, 5), (-5, 5)], [(2, 1.5), (-2, 1.5), (0, -5)], ["(x-3.1)**2"], 5, "Symmetry"),                        
Level([(1, 9)], [(4, 0), (6, 1), (8, 2), (10, 3)], [""], 6, ""), # another ez line level
Level([(5, 8)], [(0, 5), (9, 3.3), (5, 0)], [""], 7, "Problems are not stop signs, they are guidelines"), 
Level([(-8, 8)], [(0, 3), (-8, -4), (0, -6)], [""], 8, "Donkey Kong"), # donkey kong level
Level([(9, 5)], [(7, 2.5), (8, 3), (3, 1.5), (-5, -5)], ["ln(x)"], 9, ""), 
Level([(10, 10)], [(7, 2), (3, 3.5), (3, 2), (4.5, 2.9)], [""], 10, "It always seems impossible until it's done"), 
Level([(-9, 8)], [(-1, 5), (-2, 2), (-9, 1.5)], [""],  11, "Never trust a man who doesn't like cats")
]

grade10 = [ # Defines the list of Grade 10 levels.
Level([(9,15)],[(3,8.5),(7,12.5),(-2,3.5),(-4,1.5)], ["x + 5"],1,""), # x + 5
Level([(3.5,15)],[(2.5,8.5),(4,12.5),(-2,3.5),(-4,1.5)], [""],2,"you miss 100 percent of the shots u dont take"), # x*3
Level([(5,15.5)],[(2.5,8.5),(4,13),(0,0.5)], [""],3,""), # x*3
Level([(1.7,2.5)],[(5.5,-0.7),(3,0.6),(4,-0.7),(4.7,-1.6)], ["sin(x) * 2"],4,""), # x*3
Level([(0.3,2.5)],[(4,-0.7),(1.5,0.6),(2.5,-0.7),(3.2,-1.6)], ["cos(x) * 2"],5,"The harder you fall the higher you bounce"), # x*3
Level([(1.7,8)],[(1.5,6),(1,3),(0,0.5),(-1,-1.6)], ["sinh(x) * 2"],6,"") # x*3
]

grade11 = [ # Defines the list of Grade 11 levels.
Level([(8,3.9)],[(2,2),(0.5,1)],["x"],1,""), # sqrt(x)
Level([(6,5.7)],[(3,4),(2,3.3),(0.45,1.8)],["x"],2,""), # sqrt(x)*2
Level([(-3,6.5)],[(-2,3.3),(-1,1.3), (2,-1), (4, -2)],["x**2 / 2"],3,"Try thinking about restrictions again."), # y=x^2 restriction at x=0
Level([(8,5)],[(6,4.2),(4,3.5),(2,2.2),(1,0.7),(-1,-2)],["log(x)*2"],4,""), # log(x)*2
Level([(5,6)],[(4,4),(3,2.2),(2,1.2),(1,0.8),(-1,0.4),(-3,-0.2)],["x**3 / 25"],5,"The simplest solution is usually the best."), # x**3 / 25
Level([(0.8,9)],[(1,2),(2,1),(4,0.5),(6,0.4),(8,0.3)],["1/x"],6,""), # 1/x * 5
]

grade12 = [ # Defines the list of Grade 12 levels.
Level([(3.8,18)],[(3,10),(2,5.5),(1,2.5),(0,1.5)],["2**x"],1,"Good Luck!"),
Level([(-2.9,13)],[(-2,5.7),(-1,2.2),(0,1.5),(1,2.3)],["cosh(x)"],2,"Think about all that you are /instead of all you are not"),
Level([(7,4.7)],[(4,3.5),(3,2.6),(2,2),(1,0.5)],["log(x**2)"],3,"your future needs you. /Your past doesn't"),
Level([(0.5,1.5)],[(1,-0.5),(3,-1.5),(6,-2.6),(9,-2.8)],["-ln(e*x)"],4,"Dogs come when they're called; /cats take a message and get back to you later"),
Level([(4,10.5)],[(3,6.5),(2,3.5),(1,2.3),(0,1.5),(-3,0.55)],["sqrt(3**x)"],5,""),
Level([(0.8,3)],[(0,1.2),(-0.5,0),(-1,-1.8),(-2,-2.5),(-4,-2.5),(-6,-2.5)],["erf(x)*3"],6,"")
]



def first():
    '''
    This function is used to display the first screen.
    :return: None.
    '''
    global all_levels, current_level # Set the global variables.
    buttons = [] # Set the buttons to an empty list.
    for i in range(4): # For i in range 4:
        buttons.append(Button(200 + 300 * i, 400, 125, 50, light_blue, "Grade " + str(i + 9))) # Append a button to the buttons list.
    eType = [] # Set the eType to an empty list.
    selectedGrade = 0 # Set the selectedGrade to 0.
    while not selectedGrade: # While the selectedGrade is not 0:

        mouse = pygame.mouse.get_pos() # Set the mouse to the mouse position.
        for event in pygame.event.get(): # For each event in the event queue:

            eType = event.type # Set the eType to the event type.
            if eType == pygame.QUIT: # If the eType is the quit event:
                pygame.quit() # Quit pygame.
                sys.exit() # Exit the program.
        screen.fill(white) # Fill the screen with white.
        [x.draw() for x in buttons] # Draw each button in the buttons list.

        screen.blit(pygame.font.Font(None, 64).render("Select your preferred difficulty.", True, black), [screenX / 2 - 370, screenY / 2 - 100]) # Render the specified text.
        clock.tick(60) # Tick the clock.
        pygame.display.update() # Update the display.

        if eType == pygame.MOUSEBUTTONDOWN: # If the eType is the mouse button down event:
            for i in buttons: # For each button in the buttons list:
                if i.mouseon(mouse): # If the mouse is on the button:
                    clicks.play() # Play the clicks sound.
                    selectedGrade = int(i.text.split()[1]) # Set the selectedGrade to the specified integer.
                    all_levels = [grade9, grade10, grade11, grade12][selectedGrade - 9] # Set the all_levels to the specified list.
                    second() # Call the second function.
                    break # Break out of the loop.

def second():
    '''
    This function is used to display the second screen.
    :return: None.
    '''
    global all_levels, current_level # Set the global variables.
    eType = None # Set the eType to None.
    buttons = [] # Set the buttons to an empty list.
    row1 = [9 if len(all_levels) > 9 else len(all_levels)][0] # Set the row1 to the specified integer.
    for i in range(row1): # For i in range row1:
        buttons.append(Button(50 + 150 * i, 300, 125, 50, light_blue, str(i+1))) # Append a button to the buttons list.


    if row1 >= 9: # If the row1 is greater than or equal to 9:
        row2 = len(all_levels) - row1 # Set the row2 to the specified integer.
        for i in range(row2): # For i in range row2:
            buttons.append(Button(50 + 150 * i, 400, 125, 50, light_blue, str(i+10))) # Append a button to the buttons list.

    selectedLevel = -1 # Set the selectedLevel to -1.
    while selectedLevel < 0: # While the selectedLevel is less than 0:
        back_button = Button(50, 50, 50, 50, light_blue, "<") # Create the back button.
        mouse = pygame.mouse.get_pos() # Set the mouse to the mouse position.
        for event in pygame.event.get(): # For each event in the event queue:
            if event.type == pygame.QUIT: # If the event type is the quit event:
                pygame.quit() # Quit pygame.
                sys.exit() # Exit the program.
            screen.fill(white) # Fill the screen with white.
            [x.draw() for x in buttons] # Draw each button in the buttons list.

            screen.blit(pygame.font.Font(None, 64).render("Select your level.", True, black), [screenX / 2 - 200, screenY / 2 - 100]) # Render the specified text.
            clock.tick(60) # Tick the clock.
            back_button.draw() # Draw the back button.
            pygame.display.update() # Update the display.

            if event.type == pygame.MOUSEBUTTONDOWN: # If the event type is the mouse button down event:
                for i in buttons: # For each button in the buttons list:
                    if i.mouseon(mouse): # If the mouse is on the button:
                        clicks.play() # Play the clicks sound.
                        selectedLevel = int(i.text) # Set the selectedLevel to the specified integer.
                        current_level = selectedLevel # Set the current_level to the selectedLevel.
                        all_levels[current_level-1].set_level(False) # Set the level to the specified boolean.
                        break # Break out of the loop.
                if back_button.mouseon(mouse): # If the mouse is on the back button:
                    first() # Call the first function.
first() # Call the first function.

all_levels[current_level-1].set_level(False) # Set the level to the specified boolean.
level_passed = True # Set the level_passed to True.



while True: # While True:
    mouse = pygame.mouse.get_pos() # Set the mouse to the mouse position.
    for event in pygame.event.get(): # For each event in the event list:
        if event.type == pygame.QUIT: # If the event type is the quit event:
            pygame.quit() # Quit pygame.
            sys.exit() # Exit the system.

        if event.type == pygame.MOUSEBUTTONDOWN: # If the event type is the mouse button down event:

            if level_passed and menu.next_button.mouseon(mouse): # If the level is passed and the mouse is on the next button:
                try: # Try:
                    all_curves, all_points = [], [] # Set the all curves and all points to empty lists.
                    current_level += 1 # Add 1 to the current level.
                    all_levels[current_level-1].set_level(False) # Set the level to False.
                    win.play() # Play the win sound.
                except: # Except:
                    first() # Call the first function.

            if menu.menu and menu.reset_button.mouseon(mouse): # If the menu is open and the mouse is on the reset button:
                lose.play() # Play the lose sound.
                all_levels[current_level-1].set_level(True) # Set the level to True.

            if menu.menu and menu.launch_button.mouseon(mouse): # If the menu is open and the mouse is on the launch button:
                clicks.play() # Play the clicks sound.
                for i in all_curves: # For each curve in the all curves list:
                    i.type.selected = False # Set the type selected to False.
                    i.restriction_button.selected = False # Set the restriction button selected to False.
                run_physics = True # Set the run physics to True.
                menu.launch_button.greyed = True # Set the launch button greyed to True.

            if menu.menu and menu.close_menu.mouseon(mouse): # If the menu is open and the mouse is on the close menu button:
                clicks.play() # Play the clicks sound.
                menu.v_p = - 5 # Set the menu vertical protrusion to -5.
                menu.menu = False # Set the menu to False.
                for i in all_curves: # For each curve in the all curves list:
                    i.restriction_button.selected = False # Set the restriction button selected to False.
                    i.type.selected = False # Set the type selected to False.

            if menu.menu and menu.settings_button.mouseon(mouse): # If the menu is open and the mouse is on the settings button:
                clicks.play() # Play the clicks sound.
                menu.pause = True # Set the menu pause to True.
                run_physics = False # Set the run physics to False.
                for i in all_curves: # For each curve in the all curves list:
                        i.restriction_button.selected = False # Set the restriction button selected to False.
                        i.type.selected = False # Set the type selected to False.

            if menu.pause and menu.change_level.mouseon(mouse): # If the menu is paused and the mouse is on the change level button:
                clicks.play() # Play the clicks sound.
                menu.pause = False # Set the menu pause to False.
                menu.menu = True # Set the menu to True.
                first() # Call the first function.
                break # Break.

            if menu.pause and menu.close_settings.mouseon(mouse): # If the menu is paused and the mouse is on the close settings button:
                clicks.play() # Play the clicks sound.
                menu.pause = False # Set the menu pause to False.
                menu.menu = True # Set the menu to True.

            if menu.pause and menu.interval_type.mouseon(mouse): # If the menu is paused and the mouse is on the interval type:
                clicks.play() # Play the clicks sound.
                if not menu.interval_type.selected: # If the interval type is not selected:
                    menu.interval_type.selected = True # Set the interval type selected to True.
                else: # Else:
                    menu.interval_type.seleced = False # Set the interval type selected to False.

            if not menu.menu and menu.open_menu.mouseon(mouse) and menu.protrusion < 200: # If the menu is not open and the mouse is on the open menu button and the menu protrusion is less than 200:
                menu.v_p = 5 # Set the menu vertical protrusion to 5.
                menu.menu = True # Set the menu to True.

            for i in all_curves: # For each curve in the all curves list:
                if i.type.mouseon(mouse) and not i.restriction_button.mouseon(mouse): # If the mouse is on the type and not on the restriction button:
                    if i.type.selected: # If the type is selected:
                        i.type.selected = False # Set the type selected to False.
                    else: # Else:
                        i.type.selected = True # Set the type selected to True.
                        i.restriction_button.selected = False # Set the restriction button selected to False.
                        i.to_restriction.selected = False # Set the to restriction selected to False.
                        i.from_restriction.selected = False # Set the from restriction selected to False.
                        for j in all_curves: # For each curve in the all curves list:
                            if j != i: # If the curve is not the curve:
                                j.restriction_button.selected = False # Set the restriction button selected to False.
                                j.type.selected = False # Set the type selected to False.


                elif i.restriction_button.mouseon(mouse): # If the mouse is on the restriction button:
                    if i.restriction_button.selected: # If the restriction button is selected:

                        i.restriction_button.selected = False # Set the restriction button selected to False.

                    else: # Else:
                        i.restriction_button.selected = True # Set the restriction button selected to True.
                        i.to_restriction.selected = False # Set the to restriction selected to False.
                        i.from_restriction.selected = False # Set the from restriction selected to False.
                        i.type.selected = False # Set the type selected to False.

                        for j in all_curves: # For each curve in the all curves list:
                            if j != i: # If the curve is not the curve:
                                j.restriction_button.selected = False # Set the restriction button selected to False.
                                j.type.selected = False # Set the type selected to False.

                if i.restriction_button.selected: # If the restriction button is selected:
                    if i.to_restriction.mouseon(mouse): # If the mouse is on the to restriction:
                        if i.to_restriction.selected: # If the to restriction is selected:
                            i.to_restriction.selected = False # Set the to restriction selected to False.
                        else: # Else:
                            i.to_restriction.selected = True # Set the to restriction selected to True.
                            i.type.selected = False # Set the type selected to False.
                            i.from_restriction.selected = False # Set the from restriction selected to False.

                            for j in all_curves: # For each curve in the all curves list:
                                if j != i: # If the curve is not the curve:
                                    j.restriction_button.selected = False # Set the restriction button selected to False.
                                    j.type.selected = False # Set the type selected to False.

                    elif i.from_restriction.mouseon(mouse): # If the mouse is on the from restriction:
                        if i.from_restriction.selected: # If the from restriction is selected:
                            i.from_restriction.selected = False # Set the from restriction selected to False.
                        else: # Else:
                            i.from_restriction.selected = True # Set the from restriction selected to True.
                            i.type.selected = False # Set the type selected to False.
                            i.to_restriction.selected = False # Set the to restriction selected to False.

                            for j in all_curves: # For each curve in the all curves list:
                                if j != i: # If the curve is not the curve:
                                    j.restriction_button.selected = False # Set the restriction button selected to False.
                                    j.type.selected = False # Set the type selected to False.


        if event.type == pygame.KEYDOWN: # If the event type is the key down event:
            if menu.pause: # If the menu is paused:
                if menu.interval_type.selected: # If the interval type is selected:
                    typing_register(event, menu.interval_type, 4) # Call the typing register function.


            for i in all_curves: # For each curve in the all curves list:
                if i.type.selected: # If the type is selected:
                    typing_register(event, i.type, 20) # Call the typing register function.

                    if event.key == pygame.K_RETURN: # If the event key is the return key:
                        new_curve = Curve(i.pos+1) # Set the new curve to a new curve.
                        new_curve.color = random.choice(colors) # Set the new curve color to a random color.
                        all_curves.append(new_curve) # Add the new curve to the all curves list.

                if i.restriction_button.selected: # If the restriction button is selected:
                    if i.from_restriction.selected: # If the from restriction is selected:
                        typing_register(event, i.from_restriction, 6) # Call the typing register function.

                    elif i.to_restriction.selected: # If the to restriction is selected:
                        typing_register(event, i.to_restriction, 6) # Call the typing register function.



        if event.type == pygame.MOUSEBUTTONUP: # If the event type is the mouse button up event:
            calc_points() # Calculate the points.
            click = 0 # Set the click to 0.

        if event.type == pygame.KEYDOWN: # If the event type is the key down event:
            if event.key == pygame.K_TAB: # If the event key is the tab key:
                if menu.menu: # If the menu is open:
                    menu.v_p = - 5 # Set the menu vertical protrusion to -5.
                    menu.menu = False # Set the menu to False.
                    for i in all_curves: # For each curve in the all curves list:
                        i.restriction_button.selected = False # Set the restriction button selected to False.
                        i.type.selected = False # Set the type selected to False.

                else: # Else:
                    menu.v_p = 5 # Set the menu vertical protrusion to 5.
                    menu.menu = True # Set the menu to True.

            elif event.key == pygame.K_SPACE: # If the event key is the space key:
                if run_physics: # If the run physics is True:
                    run_physics = False # Set the run physics to False.
                else: # Else:
                    run_physics = True # Set the run physics to True.

            elif event.key == pygame.K_ESCAPE: # If the event key is the escape key:
                pygame.quit() # Quit pygame.
                sys.exit() # Exit the system.



    screen.fill(white) # Fill the screen with white.
    grid.draw() # Draw the grid.
    for i in all_points: # For each point in the all points list:
        for j in i: # For each point in the point:
            j.calc_pos() # Calculate the position of the point.
    draw_line() # Call the draw line function.
    draw_dynamic() # Call the draw dynamic function.


    def drag(): # Define the drag function:
        global click # Set the click to global.
        if pygame.mouse.get_pressed()[0]: # If the left mouse button is pressed:
            pygame.mouse.set_cursor(9) # Set the mouse cursor to 9.
            rel_pos = pygame.mouse.get_rel() # Set the relative position to the mouse relative position.
            if click != 0: # If the click is not 0:
                addx = rel_pos[0]/(screenX/ grid.max_Lx) # Set the addx to the relative position x divided by the screen x divided by the grid max x.
                addy = rel_pos[1]/(screenY/ grid.max_Ly) # Set the addy to the relative position y divided by the screen y divided by the grid max y.

                grid.startx -= addx # Subtract the addx from the grid start x.
                grid.endx -= addx # Subtract the addx from the grid end x.
                grid.starty += addy # Add the addy to the grid start y.
                grid.endy += addy # Add the addy to the grid end y.

            click+=1 # Add 1 to the click.

    for i in all_levels: # For each level in the all levels list:
        if i.num == current_level: # If the level number is the current level:
            amount_collected = 0 # Set the amount collected to 0.
            for j in i.all_stars: # For each star in the level all stars list:
                j.draw() # Draw the star.
                j.collide() # Call the collide function.
                if j.collected: # If the star is collected:
                    amount_collected += 1 # Add 1 to the amount collected.

                if amount_collected == len(i.all_stars): # If the amount collected is the length of the level all stars list:
                    level_passed = True # Set the level passed to True.
                else: # Else:
                    level_passed = False # Set the level passed to False.



    if mouse[0] <= menu.protrusion - 11 and menu: # If the mouse x is less than or equal to the menu protrusion minus 11 and the menu is open:
        for i in all_curves: # For each curve in the all curves list:
            if 0 <= mouse[0] <= menu.protrusion and i.pos*75 <= mouse[1] <= i.pos*75 + 75: # If the mouse x is between 0 and the menu protrusion and the mouse y is between the curve position times 75 and the curve position times 75 plus 75:
                if i.type.selected: # If the type is selected:
                    pygame.mouse.set_cursor(1) # Set the mouse cursor to 1.
                else: # Else:
                    pygame.mouse.set_cursor(11) # Set the mouse cursor to 11.
            if mouse[1] > len(all_curves)*75: # If the mouse y is greater than the length of the all curves list times 75:
                pygame.mouse.set_cursor(0) # Set the mouse cursor to 0.
    else: # Else:
        pygame.mouse.set_cursor(3) # Set the mouse cursor to 3.

    if menu.menu and mouse[0] >= menu.protrusion: # If the menu is open and the mouse x is greater than or equal to the menu protrusion:
        drag() # Call the drag function.
    elif not menu.menu: # Else if the menu is not open:
        drag() # Call the drag function.

    if level_passed: # If the level is passed:
        menu.next_button.draw() # Draw the next button.

    fps = int(clock.get_fps()) # Set the fps to the clock fps.

    if run_physics: # If the run physics is True:
        space.step(1/25) # Step the space.

    for i in all_levels: # For each level in the all levels list:
        if i.num == current_level: # If the level number is the current level:
            if i.text != "": # If the level text is not empty:
                i.new_text.draw() # Draw the new text.

    menu.draw() # Call the menu draw function.

    clock.tick(60) # Tick the clock.
    pygame.display.update() # Update the display.