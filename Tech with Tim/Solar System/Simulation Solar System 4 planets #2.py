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
CYAN =  (0, 255, 255)
PURPLE = (255, 0, 255)

RED_MARS = (188, 39, 50)
DARK_GREY = (81, 78, 81)
BLUE_EARTH = (100, 149, 237)


FONT = pygame.font.SysFont("comicsans", 16)
WIN.blit(FONT.render("Distance par rapport au Soleil", 1, WHITE), (0, 0))
class Planet():

    AU = 146.6e6 *1000
    G = 6.6728e-11
    SCALE = 250 / AU #1AU = 100 pixels
    TIMESTEP = 3600 # 1 hour

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
        self.date = [0, 0, 0, 0, 0]

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
            WIN.blit(distance_text2, (5, planets.index(self) * 20 + 120))
            
        #Name
        name =self.name
        distance_text3 = FONT.render(name.strip(), 1, GREEN)
        WIN.blit(distance_text3, (x - distance_text3.get_width() // 2, y - distance_text3.get_height() - self.radius))

    def revolution(self, planets, h, d, w, m, y):
        
        if not self.sun:
            if planets.index(self) <= 2:

                if self.y > 0:
                    self.make_revolution = True
                
                if self.y < 0 and self.make_revolution == True:
                    
                    
                    new_h = h - self.date[0]
                    new_d = d - self.date[1]
                    new_w = w - self.date[2]
                    new_m = m - self.date[3]
                    new_y = y - self.date[4]

                    print(str(self.name).strip() + " a fait une revolution en " + str(new_h) + "H / " + str(new_d) + " D / " + str(new_w) + " W / " + str(new_m) + " M / " + str(new_y) + " Y")
                    self.make_revolution = False

                    self.date[0] = h
                    self.date[1] = d
                    self.date[2] = w
                    self.date[3] = m
                    self.date[4] = y

            else:
                if self.y < 0:
                    self.make_revolution = True
                
                if self.y > 0 and self.make_revolution == True:

                    new_h = h - self.date[0]
                    new_d = d - self.date[1]
                    new_w = w - self.date[2]
                    new_m = m - self.date[3]
                    new_y = y - self.date[4]

                    print(str(self.name).strip() + " a fait une revolution en " + str(new_h) + "H / " + str(new_d) + " D / " + str(new_w) + " W / " + str(new_m) + " M / " + str(new_y) + " Y")
                    self.make_revolution = False

                    self.date[0] = new_h
                    self.date[1] = new_d
                    self.date[2] = new_w
                    self.date[3] = new_m
                    self.date[4] = new_y                    

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

    def show_force(self, WIN,  planets):

        new_x = self.x * self.SCALE + WIDTH // 2
        new_y = self.y * self.SCALE + HEIGHT // 2

        for i in range(planets.index(self) +1, len(planets)):
            new_planete_x = planets[i].x * self.SCALE + WIDTH // 2
            new_planete_y = planets[i].y * self.SCALE + HEIGHT // 2
            
            _, _, force, _ = self.attraction(planets[i])
            nombre = format(force, ".1E")
            indice_plus = nombre.find('+')                          # Trouver l'indice du signe '+'
            partie_apres_exposant = nombre[indice_plus + 1:]        # Extraire la partie après le '+'

            pygame.draw.line(WIN, RED, (new_x, new_y), (new_planete_x, new_planete_y), int(partie_apres_exposant)//3)

    def show_vecteur(self, WIN, sun):

        if not self.sun:
        
            _, _, _, theta_radain = self.attraction(sun)

            #Force gravitionnelle

            #X1, y1 sont les coordonnées de la distaance entre la planete est le soleil moins 1/10 de la distance planete soleil
            x1 = -math.cos(theta_radain) * (self.distance_to_sun - self.distance_to_sun * 0.5) *self.SCALE // 2 
            y1 = -math.sin(theta_radain) * (self.distance_to_sun - self.distance_to_sun * 0.5) *self.SCALE // 2 

            #x2, y2 sont les coordonnées de la distaance entre la planete est le soleil
            x2 = -math.cos(theta_radain) * self.distance_to_sun *self.SCALE + WIDTH // 2
            y2 = -math.sin(theta_radain) * self.distance_to_sun *self.SCALE + HEIGHT // 2

            #En faisant x1-x2 et y1-y2 ont garde la différence entre les deux 
            pygame.draw.line(WIN, CYAN, (x2-x1, y2-y1), (x2, y2), 2)

            #Inertie
            phi_radian = math.pi / 4
            AB = math.sqrt(x1**2 + y1**2)
            AC = AB / math.cos(phi_radian)

            omega_radian = theta_radain + phi_radian
            x3 = x2 + x1 + AC * math.cos(omega_radian) 
            y3 = y2 + y1 + AC * math.sin(omega_radian) 
            pygame.draw.line(WIN, PURPLE, (x2, y2), (x3, y3), 2)
            
def main():

    run = True
    clock = pygame.time.Clock()

    #Planete
    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet("Earth    ", - 1 * Planet.AU, 0, 16,  BLUE_EARTH, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 

    mars = Planet("Mars     ", -1.524 * Planet.AU, 0, 12, RED_MARS, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus    ", 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, mercury, venus, earth, mars]

    i = 0
    print("")
    h = d = w = m = y = 0
    show_interaction_gravitaionelle = False
    show_force = False
    press1 = True
    press2 = True

    while run :

        clock.tick(60)
        WIN.fill(BLACK)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Press
        key = pygame.key.get_pressed()
        
        #Interaction gravitionelle
        if not key[pygame.K_g] and press1 == False:
            press1 = True

        if key[pygame.K_g] and press1 == True:
            show_interaction_gravitaionelle = not show_interaction_gravitaionelle
            press1 = False

        if show_interaction_gravitaionelle :
            for planet in planets:
                planet.show_force(WIN, planets)

        #Force 
        if not key[pygame.K_f] and press2 == False:
            press2 = True

        if key[pygame.K_f] and press2 == True:
            show_force = not show_force
            press2 = False

        if show_force :
            for planet in planets:
                planet.show_vecteur(WIN, planets[0])    
            
        for planet in planets:
            planet.update_position(planets)
            planet.revolution(planets, h, d, w, m, y)
            
            planet.draw(WIN, planets)

        WIN.blit(FONT.render("Distance par rapport au Soleil", 1, WHITE), (5, 0))
        WIN.blit(FONT.render("Vitesse par rapport au Soleil", 1, WHITE), (5, 120))

        h = i
        d = h // 24
        w = d // 7
        m = d // 30
        y = m // 12

        WIN.blit(FONT.render("Time: "+ str(h) +"H / "+ str(d) +"Day / "+ str(w) +"Week / "+ str(m) +"Month / " + str(y) +"Years", 1, WHITE), (300, 0))
        pygame.display.flip()
        i += 1

    pygame.quit()

main()


