import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1_000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

RED_MARS = (188, 39, 50)
GREY_MERCURY = (81, 78, 81)
BLUE_EARTH = (100, 149, 237)
WHITE_VENUS = (210, 180, 140)
BRUN_JUPITER = (210, 180, 140) 
BRUN_SATURNE = (210, 180, 140)
BLEU_URANUS = (173, 216, 230)
BLEU_NEPTUNE=  (0, 0, 128)

FONT = pygame.font.SysFont("comicsans", 16)
WIN.blit(FONT.render("Distance par rapport au Soleil", 1, WHITE), (0, 0))

#Class Planet
class Planet():

    AU = 149.6e6 *1000
    SCALE =  21 / AU  #1AU = 21 pixel, la demi largeur fait 35 UA 

    RADUIS_SUN =  (SCALE * AU ) / 20
    
    RADUIS_EARTH = RADUIS_SUN / 40
    G = 6.6728e-11

    TIMESTEP = 3600*24

    def __init__(self, name, x, y, radius, color, mass) -> None:

        self.x = x
        self.y = y 
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.vitesse = 0
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.make_revolution = False
        self.date = [0, 0, 0, 0]

        #Vitesse
        self.x_vel = 0  
        self.y_vel = 0

    def draw(self, WIN, planets):

        x = self.x * self.SCALE + WIDTH // 2
        y = self.y * self.SCALE + HEIGHT //2

        if len(self.orbit) > 2:
            update_points = []

            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH // 2
                y = y * self.SCALE + HEIGHT // 2
                update_points.append((x, y))

            pygame.draw.lines(WIN, self.color, False, update_points, 2)
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)

        if not self.sun:
            #Distance to the Sun
            distance_text1 = FONT.render(str(self.name) +" :" + format(self.distance_to_sun/1000, ".3E")+ " Km", 1, WHITE)
            WIN.blit(distance_text1, (5, planets.index(self) * 20))
            
            #Vitesse orbital
            distance_text2 = FONT.render(str(self.name) +" :" + str(self.vitesse/1000)[:4] + " Km/S", 1, WHITE)
            WIN.blit(distance_text2, (5, planets.index(self) * 20 + (len(planets) +1 ) * 20))
            
        #Name
        name =self.name
        distance_text3 = FONT.render(name.strip(), 1, GREEN)
        WIN.blit(distance_text3, (x - distance_text3.get_width() // 2, y - distance_text3.get_height() - self.radius))

    def revolution(self, planets, d, w, m, y):
        
        if not self.sun:
            if planets.index(self) == 1 or planets.index(self) ==2 or planets.index(self) == 5:

                if self.y > 0:
                    self.make_revolution = True
                
                if self.y < 0 and self.make_revolution == True:
                    
                    
                    new_d = d - self.date[0]
                    new_w = w - self.date[1]
                    new_m = m - self.date[2]
                    new_y = y - self.date[3]

                    print(str(self.name).strip() + " a fait une revolution en " + str(new_d) + " D / " + str(new_w) + " W / " + str(new_m) + " M / " + str(new_y) + " Y")
                    self.make_revolution = False

                    self.date[0] = d
                    self.date[1] = w
                    self.date[2] = m
                    self.date[3] = y

            else:
                if self.y < 0:
                    self.make_revolution = True
                
                if self.y > 0 and self.make_revolution == True:

                    new_d = d - self.date[0]
                    new_w = w - self.date[1]
                    new_m = m - self.date[2]
                    new_y = y - self.date[3]

                    print(str(self.name).strip() + " a fait une revolution en " + str(new_d) + " D / " + str(new_w) + " W / " + str(new_m) + " M / " + str(new_y) + " Y")
                    self.make_revolution = False

                    self.date[0] = new_d
                    self.date[1] = new_w
                    self.date[2] = new_m
                    self.date[3] = new_y                    

    def attraction(self, other):

        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
            self.vitesse = math.sqrt(self.x_vel**2 + self.y_vel**2)

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y, force, theta
    
    def update_position(self, planets):

        total_fx = total_fy =0

        for planet in planets:
            if self == planet:
                continue

            fx, fy, _, _ = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        # A = F / M
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))

#Fonction
def mouvement(planets, sun, resolution, x_camera, y_camera):
    
    #Press
    key = pygame.key.get_pressed()
    
    #Dézoom
    if key[pygame.K_a] :
        if  Planet.SCALE - 1 / Planet.AU > 0:

            Planet.SCALE -= 1 / Planet.AU 
            Planet.RADUIS_SUN = (Planet.SCALE * Planet.AU ) / 20
            resolution -= 1

            for planet in planets:
                if planet == sun:
                    sun.radius = Planet.RADUIS_SUN
                else:
                    continue

    #Zoom
    if key[pygame.K_q] :

        Planet.SCALE += 1 / Planet.AU 
        Planet.RADUIS_SUN = (Planet.SCALE * Planet.AU ) / 20
        resolution += 1

        for planet in planets:
                if planet == sun:
                    sun.radius = Planet.RADUIS_SUN
                else:
                    continue
    #Droite
    if key[pygame.K_RIGHT] :
        x_camera += 1
        for planet in planets:
            if resolution == -10:
                planet.x += Planet.AU
            else:
                planet.x += Planet.AU / (10 + resolution)
            planet.orbit.clear()

    #Gauche
    if key[pygame.K_LEFT] :
        x_camera -= 1
        for planet in planets:
            if resolution == -10:
                planet.x -= Planet.AU
            else:
                planet.x -= Planet.AU / (10 + resolution)
            planet.orbit.clear()
    
    #Haut
    if key[pygame.K_UP] :
        y_camera -= 1
        for planet in planets:
            if resolution == -10:
                planet.x -= Planet.AU
            else:
                planet.y -= Planet.AU / (10 + resolution)
            planet.orbit.clear()

    #Bas
    if key[pygame.K_DOWN] :
        y_camera += 1
        for planet in planets:
            if resolution == -10:
                planet.x += Planet.AU
            else:
                planet.y += Planet.AU / (10 + resolution)
            planet.orbit.clear()

    return resolution, x_camera, y_camera  


def follow_planet(planets ,x_camera, y_camera, resolution):

    #Press
    key = pygame.key.get_pressed()
    
    if key[pygame.K_s] :
        for planet in planets:
            if resolution == -10:

                planet.x -= x_camera * Planet.AU 
                planet.y -= y_camera * Planet.AU 
            else:

                planet.x -= x_camera * Planet.AU / (10 + resolution)
                planet.y -= y_camera * Planet.AU / (10 + resolution)
            planet.orbit.clear()

        x_camera = 0
        y_camera = 0

    return x_camera, y_camera


def main():

    run = True
    clock = pygame.time.Clock()

    #Planete
    sun = Planet("Sun", 0, 0, Planet.RADUIS_SUN, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet("Earth    ", - 1 * Planet.AU, 0, Planet.RADUIS_EARTH,  BLUE_EARTH, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 

    mars = Planet("Mars     ", -1.524 * Planet.AU, 0, int(Planet.RADUIS_EARTH * 0.75), RED_MARS, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, int(Planet.RADUIS_EARTH * 0.38), GREY_MERCURY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus    ", 0.723 * Planet.AU, 0, int(Planet.RADUIS_EARTH * 0.95), WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet("Jupiter ", 5.2 * Planet.AU, 0, Planet.RADUIS_EARTH * 11, BRUN_JUPITER, 1.8986 * 10**27 )
    jupiter.y_vel = -13.0585 * 1000

    saturne = Planet("Saturne", -9.5 * Planet.AU, 0, Planet.RADUIS_EARTH * 9.4, BRUN_SATURNE, 5.6846 * 26)
    saturne.y_vel = 9.6407 * 1000

    uranus = Planet("Uranus ", 19 * Planet.AU, 0, Planet.RADUIS_EARTH * 3.9, BLEU_URANUS, 8.681 * 10**25 )
    uranus.y_vel = -6.796732 * 1000

    neptune = Planet("Neptune", -30.1 * Planet.AU, 0, Planet.RADUIS_EARTH * 3.8, BLEU_NEPTUNE, 1.0243 * 10**26)
    neptune.y_vel = 5.432 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturne, uranus, neptune]

    i = 0 # Ittération
    resolution = 0 # Puissance du zoom

    x_camera = 0
    y_camera = 0

    d = w = m = y = 0 #Time
    print("")

    while run :

        clock.tick(60)
        WIN.fill(BLACK)

        resolution, x_camera, y_camera = mouvement(planets, sun, resolution, x_camera, y_camera)
        x_camera, y_camera = follow_planet(planets ,x_camera, y_camera, resolution)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            
        for planet in planets:
            planet.update_position(planets)
            planet.revolution(planets, d, w, m, y)
            planet.draw(WIN, planets)

        WIN.blit(FONT.render("Distance par rapport au Soleil", 1, WHITE), (5, 0))
        WIN.blit(FONT.render("Vitesse par rapport au Soleil", 1, WHITE), (5, (len(planets) +1 )* 20 ))

        d = i
        w = d // 7
        m = d // 30
        y = m // 12

        WIN.blit(FONT.render("Time: "+ str(d) +"Day / "+ str(w) +"Week / "+ str(m) +"Month / " + str(y) +"Years", 1, WHITE), (300, 0))

        WIN.blit(FONT.render("Unité Astronomique " + str((WIDTH //2) / (Planet.SCALE * Planet.AU)) + " ou " + format((WIDTH //2) / (Planet.SCALE * 1000), ".3E") + " km", 1,  RED), (WIDTH //100 , HEIGHT - HEIGHT //20))
        pygame.draw.line(WIN, WHITE, (WIDTH//100 , HEIGHT - HEIGHT //100), (WIDTH //2, HEIGHT - HEIGHT //100 ), 3)
        pygame.display.flip()
        i += 1

    pygame.quit()

main()


