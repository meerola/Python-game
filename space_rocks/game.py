import pygame

from utils import load_sprite, get_random_position
from models import SpaceShip, Asteroid

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    
    # Constructor
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800,600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        
        # Skapa tom lista med asteroider
        self.asteroids = []
        # Bullets, empty list to store bullets
        self.bullets = []
        # Spaceship x 1
        self.spaceship = SpaceShip((400,300), self.bullets.append) # callback funktion för bullets
        
        # Definiera random position (inte för nära spaceship) för alla asteroider och append ny asteroid till listan. 
        for i in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append)) # --Hmm?--
        
    # Initiate pygame package, needs to be done.
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    # Vid start bildar __main__.py SpaceRocks objektet, och skickar den till main_loop() för att hålla igång spelet
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _get_game_objects(self):
        # Skapa nya objekten i __init__() och lägg till dem  här för att de ska tas med i _process_game_logic() och _draw()
        # self.asteroids listans objekt läggs in i nya listan mde '*', inte "list-in-list"
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship: # Går inte vidare ifall kollision, då self.spaceship = None
            game_objects.append(self.spaceship)
        
        return game_objects

    def _handle_input(self):
        for event in pygame.event.get():
            # QUIT game
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

                      
        # pygame.key.get_pressed() kollar kontinuerligt ifall knappen är intryckt, till skillnad från pygame.event.key.
        is_key_pressed = pygame.key.get_pressed()
        
        # Bara ifall vi har ett spaceship försöker vi styra det
        if self.spaceship:
            # Rotation, left/right
            if is_key_pressed[pygame.K_RIGHT]: #is_key_pressed is a list. True if pygame.K_RIGHT är 1 i den listan
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            
            # Acceleration, up
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

        # Restart with brand new spaceship by pressing a specific key
        if is_key_pressed[pygame.K_r]:
            self.spaceship = SpaceShip((400,300), self.bullets.append)

    def _process_game_logic(self):
        # MOVE - Loopar över alla objekt istället för att skriva in dem skilt
        for game_object in self._get_game_objects():   
            game_object.move(self.screen)

        # Collision
        if self.spaceship: # when the spaceship is destroyed, there’s no reason to check any collisions with it. Error if checking collision with None object
            for asteroid in self.asteroids: # Loopar genom alla asteroider
                if asteroid.collides_with(self.spaceship): # Kolla ifall kollision
                    self.spaceship = None # No more spaceship
                    break 
     
        # Remove old bullets from bullet list
        for bullet in self.bullets[:]: # this makes a copy of self.bullets, don't iterate over list that is being edited
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # Bullet hit --> removes asteroid and bullet --> Calls split() on asteroid 
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:  
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

    def _draw(self):
        self.screen.blit(self.background, (0,0))
        # Loopar över alla objekt istället för att skriva in dem skilt
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        
        # Uppdaterar skärmen enligt tick rate
        pygame.display.flip()
        self.clock.tick(60)
        # print("Collides:", self.spaceship.collides_with(self.asteroid))

