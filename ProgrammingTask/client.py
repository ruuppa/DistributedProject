import pygame

from network import Network

#testi#
width = 500
height = 500
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Player")

clientNumbet = 0

FPS_LIMIT = 24

class Player():
    def __init__(self, x, y, width, height, color, connection):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 30
        self.connection = connection

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.connection.send(b"moving left...")

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.connection.send(b"moving right...")

        if keys[pygame.K_UP]:
            self.y -= self.vel
            self.connection.send(b"moving up...")

        if keys[pygame.K_DOWN]:
            self.y += self.vel
            self.connection.send(b"moving down...")

        self.rect = (self.x, self.y, self.width, self.height)

def redrawWindow(win, player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

def read_pos(str): # what is the position of player, reads the pos
    str = str.split(",")
    return int(str[0], int(str[1]))

def make_pos(tup):# this is making pos
    return str(tup[0]) + "," + str(tup[1])



def main():
    run = True
    networking = Network() # Connect to the server

    p = Player(50,50,100,100,(0,255,0), networking.create_connection()) # this is the starting point

    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting the game")
                run = False
                pygame.quit()
                return

        clock.tick(FPS_LIMIT)  # throttle game to specific framerate
        p.move()
        redrawWindow(win, p)

main()
