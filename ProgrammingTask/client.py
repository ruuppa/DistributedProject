import pickle
import logging
from datetime import datetime

import pygame

from network import Network
from config import LOG_LEVEL

pygame.font.init()
width = 1000
height = 700
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Player")

FPS_LIMIT = 60

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

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

def redrawWindow(win, game, player, ping):
    win.fill((128,128,128))

    if not (game.connected):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Players...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)

        ping = font.render(f"Ping: {ping} ms", 1, (255,255,255))
        win.blit(ping, (680, 50))

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
    logger.info(f"You are a player: {player}")

    clock = pygame.time.Clock()

    p2HasJoinedFlag = False
    p3HasJoinedFlag = False
    ping = "..."

    while run:
        clock.tick(FPS_LIMIT)  # throttle game to specific framerate

        try:
            game = n.send("get")
        except:
            run = False
            logger.warning("No game detected")
            break

        pingResult = n.ping()
        if pingResult != None:
            ping = pingResult

        if game.p2Joined() == True and p2HasJoinedFlag == False:
            logger.info(f"Player 1 has joined")
            p2HasJoinedFlag = True
        if game.p3Joined() == True and p3HasJoinedFlag == False:
            logger.info(f"Player 2 has joined")
            p3HasJoinedFlag = True

        if game.allWent():
            redrawWindow(win, game, player, ping)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                logger.warning("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            benchmark_start = datetime.now()
            outcome_text = game.outcome_for_player(player)
            benchmark_duration = datetime.now() - benchmark_start
            microseconds = benchmark_duration.microseconds

            logger.info(f'calculated player outcome in {microseconds} us')
            outcome_font = font.render(outcome_text, 1, (255,0,0))

            win.blit(outcome_font, (width/2 - outcome_font.get_width()/2, height/2 - outcome_font.get_height()/2))
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

        redrawWindow(win, game, player, ping)

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

if __name__ == '__main__':
    while True:
        menu_screen()
