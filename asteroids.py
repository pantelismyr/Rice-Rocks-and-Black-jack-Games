# "RiceRocks" (Asteroids)
# Introduction to Interactive Programming in Python Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
friction_c = .01
vel_angle_list = [-.05, .05]
x_velocity_sign = [1, -1]
y_velocity_sign = [1, -1]
started = False
count = 0
game_start = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    sprites = set(group)
    
    for sprite in sprites:
        if sprite.update():
            group.remove(sprite)
        sprite.draw(canvas)
        sprite.update()

def group_collide(group, other_object):        			# Sprite other object
    remove_collided = set(group)
    
    for element in remove_collided:
        if element.collide(other_object):
            group.remove(element)
            new_explosion = Sprite(element.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(new_explosion)
            explosion_sound.play()
            
            return True
            
def group_group_collide(rock_group, missile_group):
    global count
    rock_gr = set(rock_group)
    
    for rock in rock_gr:
        if group_collide(missile_group, rock):
            count += 1
            rock_group.discard(rock)
            rock.vel
    return count
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward_v = []
       
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] * 3, self.image_center[1]),
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
            
       
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # friction
        self.vel[0] *= 1 - friction_c
        self.vel[1] *= 1 - friction_c
        
        self.angle += self.angle_vel
        self.forward_v = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += self.forward_v[0] * 0.1
            self.vel[1] += self.forward_v[1] * 0.1
         
            
        if self.pos[0] > WIDTH:
            self.pos[0] = 0 # WIDTH - self.pos[0]
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0 # HEIGHT - self.pos[1]
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT 
        
        
    def increment_ang_vel(self):
        self.angle_vel += .1
        
        
    def decrement_ang_vel(self):
        self.angle_vel -= .1
    
    def activate_thrusters(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def deactivate_thrusters(self):
        self.thrust = False 
        ship_thrust_sound.rewind()    
    
    def shoot(self):
        a_missile = Sprite([self.pos[0] + (self.forward_v[0] * self.radius),
                            self.pos[1] + (self.forward_v[1] * self.radius)], 
                           [self.vel[0] + 5 * self.forward_v[0],
                            self.vel[1] + 5 * self.forward_v[1]],
                            0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image,self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]),
                              self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        
        if self.age >= self.lifespan:
            return True 
        
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        if self.pos[0]  > WIDTH + self.radius:
            self.pos[0] = 0 
        elif self.pos[0] < - self.radius:
            self.pos[0] = WIDTH
        elif self.pos[1]  > HEIGHT + self.radius:
            self.pos[1] = 0 
        elif self.pos[1] < - self.radius:
            self.pos[1] = HEIGHT 
            
        self.age += 1
            
                
    
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        
    
    
    
def keydown(key):
    
    if key == simplegui.KEY_MAP["left"]:
        my_ship.decrement_ang_vel()     
        
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.increment_ang_vel()
    
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.activate_thrusters()    
    
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()    
    
def keyup(key):    
    
    if key == simplegui.KEY_MAP["left"]:
         my_ship.increment_ang_vel()     
    
    elif key == simplegui.KEY_MAP["right"]:
         my_ship.decrement_ang_vel() 
    
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.deactivate_thrusters()
         
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()
        
        
def draw(canvas):
    global time, lives, score, started, game_start				
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Score: ", [WIDTH - 100, 20], 20, "White")
    canvas.draw_text(str(score), [WIDTH - 100, 40], 20, "White")
    canvas.draw_text("Lives: ", [30, 20], 20, "White")
    canvas.draw_text(str(lives), [30, 40], 20, "White")
    
    # draw ship 
    my_ship.draw(canvas)

    
    # update ship and sprites
    my_ship.update()
    
    
    # draw splash screen if not started
    if not started or lives == 0:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        new_game()
       

           
        
    else:
        game_start = True
        
        
        
    # collisions
    process_sprite_group(rock_group, canvas)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    process_sprite_group(missile_group, canvas)
    
    points = group_group_collide(rock_group, missile_group)
    if points != None:
        score = points * 10
    
    process_sprite_group(explosion_group, canvas)
    
    
        
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global vel_angle_list, x_velocity_sign, y_velocity_sign
    global game_start, score  
    
    if game_start:
        x_velocity = random.choice(x_velocity_sign)
        y_velocity = random.choice(y_velocity_sign)
        
        if score != 0 and score % 50 == 0:
            x_velocity *= 1.1
            y_velocity *= 1.1
        
        x_pos = random.randrange(0, WIDTH)
        y_pos = random.randrange(0, HEIGHT)
    
        vel_angle = random.choice(vel_angle_list)
    
        a_rock = Sprite([x_pos, y_pos], [x_velocity, y_velocity], 0, vel_angle, asteroid_image, asteroid_info)
        
        if len(rock_group) < 12:    
            rock_group.add(a_rock)
            if dist(my_ship.pos, a_rock.pos) <= 2.5 * my_ship.radius:
                rock_group.remove(a_rock)
         

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize 
def new_game():
    global started, game_start, lives, score, rock_group, missile_group, explosion_group
    
    started = False
    game_start = False
    lives = 3
    score = 0
    my_ship.pos = [WIDTH / 2, HEIGHT / 2]       
    my_ship.vel = [0, 0]
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    
        
# initialize ship    
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#rock_group = set([])
#missile_group = set([])
#explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)


timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
