#henter inn python programm
import pygame
import math
pygame.init()

#definerer og setter opp vindu for simuleringen
BREDDE, HØYDE = 1920, 1080
VINDU = pygame.display.set_mode((BREDDE, HØYDE))
pygame.display.set_caption("Planet Simulering")

#definerer farger for enklere bruk senere
SVART = (0, 0, 0)
HVIT = (255, 255, 255)
GUL = (255, 255, 0)
BLÅ = (26, 209, 255)
RØD = (255, 92, 51)
GRÅ = (80, 71, 81)
ORANSJE = (204, 163, 0)

class Planet:
    AU = 149.6e6 * 1000 # gravitasjonskonstant
    G = 6.67428e-11 # gravitasjonskonstant
    SKALA = 80  / AU # 1 AU = 100 piksler
    TIDSENDRING = 3600 * 24 # 1 dag (3600 sekunder = 1 time)

    #initialiserer planetklassen
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
        
    #funksjonen for tegning av planeter
    def tegn(self, vindu):
        #definerer kordinetene for x og y etter størrelsen på vinduet
        x = self.x * self.SKALA + BREDDE / 2
        y = self.y * self.SKALA + HØYDE / 2

        if len(self.bane) > 2:
            oppdaterte_punkter = [] #lager en liste for kordinater
            for punkt in self.bane:
                x, y = punkt
                x = x * self.SKALA + BREDDE / 2
                y = y * self.SKALA + HØYDE / 2
                oppdaterte_punkter.append((x, y))

            #linjer for planetenes bane
            pygame.draw.lines(vindu, self.farge, False, oppdaterte_punkter, 1)
        #tegner en sirkel/planet i punktet
        pygame.draw.circle(vindu, self.farge, (x, y), self.radius)



    
    def tiltrekning(self, annen):
        #her definerer vi en funksjon for å regne ut avstanden mellom to punkter
        #finner avstanden i kordinater mellom punktene
        annen_x, annen_y = annen.x, annen.y
        avstand_x = annen_x - self.x
        avstand_y = annen_y - self.y
        #bruker pytagoras til å regne ut avstanden mellom to punkter
        avstand = math.sqrt(avstand_x ** 2 + avstand_y ** 2)

        #sjekker om det andre punktet er solen
        if annen.solen:
            self.avstand_til_solen = avstand

        #bruker Newtons gravitasjonslov til å regne ut gravitasjonskraften mellom de to legmene 
        kraft = self.G * self.masse * annen.masse / avstand ** 2
        #regner ut redianen mellom x-aksen og linjen
        vinkel = math.atan2(avstand_y, avstand_x)
        #dekomponerer kraften i x og y rettning
        kraft_x = math.cos(vinkel) * kraft
        kraft_y = math.sin(vinkel) * kraft
        
        return kraft_x, kraft_y

    
    #funksjon for å oppdatere posisjonen til planetene
    def oppdater_posisjon(self, planeter):
        total_kraft_x = total_kraft_y = 0
        for planet in planeter:
            if self == planet:
                continue

            #legger til den komponentene i den totale kraften i x og y rettning
            fx, fy = self.tiltrekning(planet)
            total_kraft_x += fx
            total_kraft_y += fy

        #oppdaterer farten i x og y rettning
        #farten er skalert i forhold til tidsendringen
        self.x_fart += total_kraft_x / self.masse * self.TIDSENDRING
        self.y_fart += total_kraft_y / self.masse * self.TIDSENDRING

       #oppdaterer kordinatene for planeten
        self.x += self.x_fart * self.TIDSENDRING
        self.y += self.y_fart * self.TIDSENDRING
        self.bane.append((self.x, self.y))


def hoved():
    kjør = True
    klokke = pygame.time.Clock()

    #her lager vi tillfeller av alle planetene vi ønsker
    #(kordinater (0,0), radius 15, farge gul, masse 1.98892 * 10**30kg) 
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

    #lager en liste med alle planetene
    planeter = [sol, jorden, mars, merkur, venus, jupiter]


    
    while kjør:
        klokke.tick(60) #60 frames per second
        VINDU.fill(SVART)

        #instillinger for viduet til simulasjonen
        for hendelse in pygame.event.get():
            if hendelse.type == pygame.QUIT: #topper programmet hvis vinduert lukkes
                kjør = False
        #oppdaterer posisjonen til planetene
        for planet in planeter:
            planet.oppdater_posisjon(planeter)
            planet.tegn(VINDU)
        pygame.display.update()

    pygame.quit()


hoved()
