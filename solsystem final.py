import pygame
import math
pygame.init()

BREDDE, HØYDE = 1920, 1080
VINDU = pygame.display.set_mode((BREDDE, HØYDE))
pygame.display.set_caption("Planet Simulering")

SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GUL = (255, 255, 0)
BLÅ = (26, 209, 255)
RØD = (255, 92, 51)
GRÅ = (80, 71, 81)
ORANSJE = (204, 163, 0)

class Planet:
    # astronomisk enhet, avstand fra Solen til Jorden i meter
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SKALA = 80 / AU # 1 AU = 100 piksler
    TIDSSKJEMA = 3600 * 24 # 1 dag (3600 sekunder = 1 time)

    def __init__(self, x, y, radius, farge, masse):
        self.x = x
        self.y = y
        self.radius = radius
        self.farge = farge
        self.masse = masse

        self.solen = False
        self.avstand_til_solen = 0
        self.bane = []

        self.x_fart = 0
        self.y_fart = 0

    def tegn(self, vindu):
        x = self.x * self.SKALA + BREDDE / 2
        y = self.y * self.SKALA + HØYDE / 2

        if len(self.bane) > 2:
            oppdaterte_punkter = []
            for punkt in self.bane:
                x, y = punkt
                x = x * self.SKALA + BREDDE / 2
                y = y * self.SKALA + HØYDE / 2
                oppdaterte_punkter.append((x, y))
        
            pygame.draw.lines(vindu, self.farge, False, oppdaterte_punkter, 1)

        pygame.draw.circle(vindu, self.farge, (x, y), self.radius)

    def tiltrekning(self, annen):
        annen_x, annen_y = annen.x, annen.y
        avstand_x = annen_x - self.x
        avstand_y = annen_y - self.y
        avstand = math.sqrt(avstand_x ** 2 + avstand_y ** 2)
        
        if annen.solen:
            self.avstand_til_solen = avstand
        
        kraft = self.G * self.masse * annen.masse / avstand ** 2
        vinkel = math.atan2(avstand_y, avstand_x)
        kraft_x = math.cos(vinkel) * kraft
        kraft_y = math.sin(vinkel) * kraft
        
        return kraft_x, kraft_y

    def oppdater_posisjon(self, planeter):
        total_kraft_x = total_kraft_y = 0
        for planet in planeter:
            if self == planet:
                continue

            fx, fy = self.tiltrekning(planet)
            total_kraft_x += fx
            total_kraft_y += fy

        self.x_fart += total_kraft_x / self.masse * self.TIDSSKJEMA
        self.y_fart += total_kraft_y / self.masse * self.TIDSSKJEMA

        self.x += self.x_fart * self.TIDSSKJEMA
        self.y += self.y_fart * self.TIDSSKJEMA
        self.bane.append((self.x, self.y))


def hoved():
    kjør = True
    klokke = pygame.time.Clock()

    sol = Planet(0, 0, 15, GUL, 1.98892 * 10**30)
    sol.solen = True

    jorden = Planet(-1 * Planet.AU, 0, 8, BLÅ, 5.9742 * 10**24)
    jorden.y_fart = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 6, RØD, 6.39 * 10**23)
    mars.y_fart = 24.077 * 1000

    merkur = Planet(0.387 * Planet.AU, 0, 4, GRÅ, 0.330 * 10**23)
    merkur.y_fart = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 7, HVIT, 4.8685 * 10**24)
    venus.y_fart = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 10, ORANSJE, 1.898 * 10**27)
    jupiter.y_fart = -13.1 * 1000

    planeter = [sol, jorden, mars, merkur, venus, jupiter]

    while kjør:
        klokke.tick(60)
        VINDU.fill(SVART)

        for hendelse in pygame.event.get():
            if hendelse.type == pygame.QUIT:
                kjør = False
        for planet in planeter:
            planet.oppdater_posisjon(planeter)
            planet.tegn(VINDU)
        pygame.display.update()

    pygame.quit()


hoved()
