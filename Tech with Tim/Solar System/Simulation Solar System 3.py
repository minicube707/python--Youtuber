import pygame
import math
import numpy as np
pygame.init()

WIDTH, HEIGHT = 1_500, 800 #Taille en pixel
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

rapport_size_bet_earth_sun = 109

#Class Planet
class Planet():

    AU = 149_597_870_700 #Metre
    SCALE =  21 / AU  #1AU = 21 pixel, la demi largeur fait 35 UA 

    RADUIS_SUN =  (SCALE * AU ) / 20
    
    RADUIS_EARTH = RADUIS_SUN / rapport_size_bet_earth_sun
    G = 6.67428e-11

    TIMESTEP = 3600

    def __init__(self, name, x, y, radius, color, mass, type) -> None:

        self.x = x
        self.y = y 
        self.color = color
        self.mass = mass
        self.name = name
        self.type = type
        self.vitesse = 0
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.make_revolution = False
        self.date = [0, 0, 0, 0]

        self.press = True
        self.focus = False

        #Vitesse en Km/s
        self.x_vel = 0  
        self.y_vel = 0

        #Raduis
        if name == "Sun":
            self.radius = Planet.RADUIS_SUN
        else:
            self.radius =  Planet.RADUIS_EARTH * radius

    def draw(self, WIN, planets, show_satelite):

        if( self.type =="satellite" and show_satelite) or self.type =="planet" or self.type =="star":
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
        
        if self.type == "planet":
            if planets.index(self) == 1 or planets.index(self) ==2 or planets.index(self) == 5 or planets.index(self) == 7:

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

    def follow_planet(self, planets, WIDTH_HEIGHT, x_camera, y_camera , resolution, touch, index_planete_focus):
    
        epsilon = 1.e-9

        self.focus, self.press = switch_on_off( self.focus, self.press, touch)

        if self.focus == True and self.press == False:

            for planet in planets:
                planet.orbit.clear()
                if not self == planet:
                    planet.press = True
                    planet.focus = False
                

        if self.focus:
            if resolution == -10:

                #Coordonate bettween the Sun and border of window in pixel
                coordonnee_to_the_sun_PX = np.array([WIDTH_HEIGHT[0] + x_camera / epsilon * Planet.AU * Planet.SCALE,
                                                     WIDTH_HEIGHT[1] + y_camera / epsilon * Planet.AU * Planet.SCALE])
            else:
                coordonnee_to_the_sun_PX = np.array([WIDTH_HEIGHT[0] + x_camera / (10 + resolution) * Planet.AU * Planet.SCALE,
                                                     WIDTH_HEIGHT[1] + y_camera / (10 + resolution) * Planet.AU * Planet.SCALE])

            planete_focus_x_px = Planet.SCALE * planets[index_planete_focus].x
            planete_focus_y_px = Planet.SCALE * planets[index_planete_focus].y

            new_x = WIDTH // 2 - coordonnee_to_the_sun_PX[0] - planete_focus_x_px
            new_y = HEIGHT // 2 - coordonnee_to_the_sun_PX[1] - planete_focus_y_px

            for planet in planets:

                planet.x += new_x / Planet.SCALE 
                planet.y += new_y / Planet.SCALE  

            x_camera = 0
            y_camera = 0

        return x_camera, y_camera

#Fonction
def mouvement(planets, sun, resolution, x_camera, y_camera, num):
    
    epsilon = 1.e-9
    rapport_to_the_sun = [0, 0.38, 0.95, 1, 0.75, 11, 9.4, 3.9, 3.8, 0.2, 0.082, 0.245, 0.413, 0.378, 0.0395, 0.404]

    #Press
    key = pygame.key.get_pressed()
    
    #Dézoom
    if key[pygame.K_KP_MINUS] :
        if  Planet.SCALE - 1 / Planet.AU > 0:
            
            Planet.SCALE -= num / Planet.AU 
            Planet.RADUIS_SUN = (Planet.SCALE * Planet.AU ) / 20
            Planet.RADUIS_EARTH = Planet.RADUIS_SUN / rapport_size_bet_earth_sun
            resolution -= num

            for planet in planets:
                if planet == sun:
                    sun.radius = Planet.RADUIS_SUN
                else:
                    planet.radius = rapport_to_the_sun[planets.index(planet)] * Planet.RADUIS_EARTH

    #Zoom
    if key[pygame.K_KP_PLUS] :

        Planet.SCALE += num / Planet.AU 
        Planet.RADUIS_SUN = (Planet.SCALE * Planet.AU ) / 20
        Planet.RADUIS_EARTH = Planet.RADUIS_SUN / rapport_size_bet_earth_sun
        resolution += num

        for planet in planets:
                if planet == sun:
                    sun.radius = Planet.RADUIS_SUN
                else:
                    planet.radius = rapport_to_the_sun[planets.index(planet)] * Planet.RADUIS_EARTH
    #Droite
    if key[pygame.K_RIGHT] :
        x_camera += 1 
        for planet in planets:
            if resolution == -10:
                planet.x += Planet.AU / epsilon
            else:
                planet.x += Planet.AU / (10 + resolution)
            planet.orbit.clear()

    #Gauche
    if key[pygame.K_LEFT] :
        x_camera -= 1 
        for planet in planets:
            if resolution == -10:
                planet.x -= Planet.AU / epsilon
            else:
                planet.x -= Planet.AU / (10 + resolution)
            planet.orbit.clear()
    
    #Haut
    if key[pygame.K_UP] :
        y_camera -= 1 
        for planet in planets:
            if resolution == -10:
                planet.x -= Planet.AU / epsilon
            else:
                planet.y -= Planet.AU / (10 + resolution)
            planet.orbit.clear()

    #Bas
    if key[pygame.K_DOWN] :
        y_camera += 1 
        for planet in planets:
            if resolution == -10:
                planet.x += Planet.AU / epsilon
            else:
                planet.y += Planet.AU / (10 + resolution)
            planet.orbit.clear()

    return resolution, x_camera, y_camera, num

def switch_on_off(bool_show, bool_press, key_press):

    #Press
    key = pygame.key.get_pressed()

    #Switch on/off
    if not key[key_press] and bool_press == False:
        bool_press = True

    if key[key_press] and bool_press == True:
        bool_show = not bool_show
        bool_press = False

    return bool_show, bool_press
    

def main():

    run = True
    clock = pygame.time.Clock()

    #Planete
    #Vitesse en Km/s
    sun = Planet("Sun", 0, 0, 0, YELLOW, 1.98892 * 10**30, "star")
    sun.sun = True

    earth = Planet("Earth    ", - 1 * Planet.AU, 0, 1,  BLUE_EARTH, 5.9736 * 10**24, "planet")
    earth.y_vel = 29.783 * 1000 

    mars = Planet("Mars     ", -1.524 * Planet.AU, 0, 0.75, RED_MARS, 6.39 * 10**23, "planet")
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 0.38, GREY_MERCURY, 3.30 * 10**23, "planet")
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus    ", 0.723 * Planet.AU, 0, 0.95, WHITE, 4.8685 * 10**24, "planet")
    venus.y_vel = -35.02 * 1000

    jupiter = Planet("Jupiter ", 5.2 * Planet.AU, 0, 11, BRUN_JUPITER, 1.8986 * 10**27, "planet")
    jupiter.y_vel = -13.0585 * 1000

    saturne = Planet("Saturne ", -9.5 * Planet.AU, 0, 9.4, BRUN_SATURNE, 5.6846 *10**26, "planet")
    saturne.y_vel = 9.6407 * 1000

    uranus = Planet("Uranus   ", 19 * Planet.AU, 0, 3.9, BLEU_URANUS, 8.681 * 10**25, "planet")
    uranus.y_vel = -6.796732 * 1000

    neptune = Planet("Neptune", -30.1 * Planet.AU, 0, 3.8, BLEU_NEPTUNE, 1.0243 * 10**26, "planet")
    neptune.y_vel = 1.0022 * 1000

    #Satelite
    moon = Planet("Moon      ", - (1 + 0.002_4) * Planet.AU, 0, 0.2, GREY_MERCURY, 7.347 * 10**22, "satellite")
    moon.y_vel = earth.y_vel + 1.0232195041666667 * 1000

    io = Planet("Io          ", (5.2 + 0.0028) * Planet.AU, 0, 0.082, GREY_MERCURY, 8.93 * 10**22, "satellite")
    io.y_vel = (-17.334 * 1000 + jupiter.y_vel)

    europa = Planet("Europa   ", (5.2 -0.004) * Planet.AU, 0, 0.245, GREY_MERCURY , 4.80 * 10**22, "satellite")
    europa.y_vel = (13.740 * 1000 + jupiter.y_vel)

    ganymede = Planet("Ganymede", (5.2 - 0.0071) * Planet.AU, 0, 0.413, GREY_MERCURY , 1.4819 * 10**23, "satellite")
    ganymede.y_vel = (10.880 * 1000 + jupiter.y_vel)

    calisto = Planet("Calisto     ", (5.2 + 0.0124) * Planet.AU, 0, 0.378, GREY_MERCURY , 1.075 * 10**23, "satellite")
    calisto.y_vel = (-8.204 * 1000 + jupiter.y_vel)

    encelade = Planet("Enceladus ", (-9.5 + 0.00159) * Planet.AU, 0, 0.0395, GREY_MERCURY , 1.080318 * 10**20, "satellite")
    encelade.y_vel = (12.6 * 1000 + saturne.y_vel)

    titan = Planet("Titan        ", (-9.5 + 0.00793) * Planet.AU, 0, 0.404, GREY_MERCURY , 1.3452 * 10**23, "satellite")
    titan.y_vel = (5.57 * 1000 + saturne.y_vel)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturne, uranus, neptune, moon, io, europa, ganymede, calisto, encelade, titan]

    i = 0 # Ittération
    resolution = 0 # Puissance du zoom

    x_camera = 0
    y_camera = 0

    WIDTH_HEIGHT = np.array([WIDTH //2 , HEIGHT //2])
    
    d = w = m = y = 0 #Time

    num = 1
    
    show_satelite = False
    press_sat = True

    print("")
    while run :

        clock.tick(60)
        WIN.fill(BLACK)

        show_satelite, press_sat = switch_on_off(show_satelite, press_sat, pygame.K_q)
        #Mouvement
        resolution, x_camera, y_camera, num = mouvement(planets, sun, resolution, x_camera, y_camera, num)

        #Focus on planet
        x_camera, y_camera = sun.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_s, 0)
        x_camera, y_camera = mercury.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_m, 1)
        x_camera, y_camera = venus.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_v, 2)
        x_camera, y_camera = earth.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_e, 3)
        x_camera, y_camera = mars.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_a, 4)
        x_camera, y_camera = jupiter.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_j, 5)
        x_camera, y_camera = saturne.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_t, 6)
        x_camera, y_camera = uranus.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_u, 7)
        x_camera, y_camera = neptune.follow_planet(planets, WIDTH_HEIGHT, x_camera, y_camera, resolution, pygame.K_n, 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            
        for planet in planets:
            planet.update_position(planets)
            planet.revolution(planets, d, w, m, y)
            planet.draw(WIN, planets, show_satelite)

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


