import pygame
from network import Network
import pickle
pygame.font.init()

width = 1000
height = 700
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Player")

FPS_LIMIT = 60

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, player):
    win.fill((128,128,128))

    if not (game.connected):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Players...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponent", 1, (150, 0, 150))
        win.blit(text, (380, 200))

        text = font.render("Opponent", 1, (150, 0, 150))
        win.blit(text, (680, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        move3 = game.get_player_move(2)
        if game.allWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
            text3 = font.render(move3, 1, (0, 0, 0))
        else:
            if game.p1Went and player == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))
            
            if game.p2Went and player == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p3Went and player == 2:
                text3 = font.render(move3, 1, (0,0,0))
            elif game.p3Went:
                text3 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text3 = font.render("Waiting...", 1, (0, 0, 0))

        if player == 0:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))
            win.blit(text3, (700, 350))
        elif player == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
            win.blit(text3, (700, 350))
        else:
            win.blit(text3, (100, 350))
            win.blit(text1, (400, 350))
            win.blit(text2, (700, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 200, 500, (0,0,0)), Button("Scissors", 400, 500, (255,0,0)), Button("Paper", 600, 500, (0,255,0))]
def main():
    run = True
    n = Network()
    
    player = int(n.getPlayerId())
    print("You are a player: ", player)

    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS_LIMIT)  # throttle game to specific framerate

        try:
            game = n.send("get")
        except:
            run = False
            print("No game detected")
            break

        if game.allWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            # tie:    [1, 0, 0, 0]
            # p1 Win: [0, 1, 0, 0]
            # p2 Win: [0, 0, 1, 0]
            # p3 Win: [0, 0, 0, 1]

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == [0, 1, 0, 0] and player == 0) or (game.winner() == [0, 0, 1, 0] and player == 1) or (game.winner() == [0,0,0,1] and player == 2) or (game.winner() == [0, 1, 1, 0] and (player == 0 or player == 1)) or (game.winner() == [0, 1, 0, 1] and (player == 0 or player == 2)) or (game.winner() == [0, 0, 1, 1] and (player == 1 or player == 2)):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == [1, 0, 0, 0]:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        elif player == 1:
                            if not game.p2Went:
                                n.send(btn.text)
                        else:
                            if not game.p3Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
