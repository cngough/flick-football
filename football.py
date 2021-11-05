import pygame
import random
import math

background_colour = (77, 189, 51)
(width, height) = (640, 480)
mass_of_air = 0.2
elasticity = 0.75
gravity = (math.pi, 0.002)

orig_x = 0
orig_y = 0

def drawBackground():
    # Top line
    pygame.draw.line(screen, (255,255,255), (30, 30), (610, 30), 5)
    # Bottom line
    pygame.draw.line(screen, (255,255,255), (30, 450), (610, 450), 5)
    # Left line
    pygame.draw.line(screen, (255,255,255), (30, 30), (30, 450), 5)
    # Right line
    pygame.draw.line(screen, (255,255,255), (610, 30), (610, 450), 5)
    # Half way line
    pygame.draw.line(screen, (255,255,255), (320, 30), (320, 450), 5)
    # Center spot
    pygame.draw.circle(screen, (255,255,255), (320, 240), 60, 5)
    pygame.draw.circle(screen, (255,255,255), (320, 240), 5, 5)
    # Draw left penalty area
    pygame.draw.line(screen, (255,255,255), (30, 140), (110, 140), 5)
    pygame.draw.line(screen, (255,255,255), (30, 340), (110, 340), 5)
    pygame.draw.line(screen, (255,255,255), (110, 140), (110, 340), 5)
    # Draw right penalty area
    pygame.draw.line(screen, (255,255,255), (530, 140), (610, 140), 5)
    pygame.draw.line(screen, (255,255,255), (530, 340), (610, 340), 5)
    pygame.draw.line(screen, (255,255,255), (530, 140), (530, 340), 5)

def addVectors(v1, v2):
    angle1, length1 = v1
    angle2, length2 = v2

    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap

class Particle():
    def __init__(self, coords, size, mass=1):
        self.x = coords[0]
        self.y = coords[1]
        self.size = size
        self.colour = (random.randint(0, 255),
                       random.randint(0, 255),
                       random.randint(0, 255))
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
        self.ball = False

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

    def bounds(self):
        bx = self.x - orig_x
        by = self.y - orig_y
        dist = math.hypot(bx, by)

        ax = self.x - orig_x
        ay = self.y - orig_y
        angle = math.atan2(ay, ax) + 0.5 * math.pi

        if dist >= 65:
            sin_x = (64 * math.sin(angle)) + orig_x
            cos_y = (64 * -math.cos(angle)) + orig_y
            pygame.mouse.set_pos(sin_x, cos_y)

    def score(self):
        if self.ball == True:
            if self.x <= 30:
                self.x = 320
                self.y = 240
                self.speed = 0
            if self.x >= 450:
                self.x = 320
                self.y = 240
                self.speed = 0
                
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Football')

my_particles = []
def setup():
    size = 20
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    # Draw the reds
    x = 170
    y = 140
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = red
    my_particles.append(particle)

    x = 170
    y = 240
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = red
    my_particles.append(particle)

    x = 170
    y = 340
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = red
    my_particles.append(particle)

    # Draw the blues
    x = 470
    y = 140
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = blue
    my_particles.append(particle)

    x = 470
    y = 240
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = blue
    my_particles.append(particle)

    x = 470
    y = 340
    density = random.randint(8, 20)
    particle = Particle((x, y), size, density*size**2)
    particle.colour = blue
    my_particles.append(particle)

    # Draw the ball
    x = 320
    y = 240
    size = 12
    density = 20
    particle = Particle((x, y), size, density*size**2)
    particle.colour = yellow
    particle.ball = True
    my_particles.append(particle) 

selected_particle = None
running = True
drawnBounds = False

setup()
while running:
    screen.fill(background_colour)
    drawBackground()
    pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = (orig_x, orig_y) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
            drawnBounds = False

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()
        particle.score()

    if selected_particle and selected_particle.ball == False:
        selected_particle.bounds()
        if drawnBounds == False:
            orig_x = mouseX
            orig_y = mouseY
            drawnBounds = True
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1
        pygame.draw.circle(screen, (0, 0, 0), (int(orig_x), int(orig_y)), 65, 1)

    pygame.display.flip()

pygame.quit()
