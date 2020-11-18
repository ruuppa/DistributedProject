"""Game

Provides the main game logic, who won, who's turn has gone and reset after each game
"""

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None, None]
        self.wins = [0,0,0]
        self.ties = 0

        #For future:
        self.playersWent = []

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        elif player == 1:
            self.p2Went = True
        else:
            self.p3Went = True

    def connected(self):
        return self.ready

    # Check that all players have gone, so we can evaluate the winner(s)
    def allWent(self):
        return self.p1Went and self.p2Went and self.p3Went

    def winner(self):
        # Minor qualit-of-life improvement: Takes initial letter of the player's choice and capitalizes it
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        p3 = self.moves[2].upper()[0]

        # Rules for the matrix used for this test:
        # tie:    [1, 0, 0, 0]
        # p1 Win: [0, 1, 0, 0]
        # p2 Win: [0, 0, 1, 0]
        # p3 Win: [0, 0, 0, 1]

        tie = [1, 0, 0, 0]
        # It becomes very difficult to make this calculation with if-else hell on more than 3 players. 3^3 = 27 etc. etc.
        # So a better way needs to be found if we want to scale the actual player-count upwards
        # Currently done with if-else hell, so definitely not great.

        # Tie
        if p1 == p2 == p3:
            return tie
        elif p1 != p2 != p3:
            return tie

        # 2 winners:
        ## Players 1 and 2 win
        elif p1 == p2 == "R" and p3 == "S":
            return [0, 1, 1, 0]
        elif p1 == p2 == "P" and p3 == "R":
            return [0, 1, 1, 0]
        elif p1 == p2 == "S" and p3 == "P":
            return [0, 1, 1, 0]

        ## Players 1 and 3 win
        elif p1 == p3 == "R" and p2 == "S":
            return [0, 1, 0, 1]
        elif p1 == p3 == "P" and p2 == "R":
            return [0, 1, 0, 1]
        elif p1 == p3 == "S" and p2 == "P":
            return [0, 1, 0, 1]

        ## Players 2 and 3 win
        elif p2 == p3 == "R" and p1 == "S":
            return [0, 0, 1, 1]
        elif p1 == p2 == "P" and p1 == "R":
            return [0, 0, 1, 1]
        elif p1 == p2 == "S" and p1 == "P":
            return [0, 0, 1, 1]

        # 1 winner:
        ## Player 3 wins
        elif p1 == p2 == "R" and p3 == "P":
            return [0, 0, 0, 1]
        elif p1 == p2 == "P" and p3 == "S":
            return [0, 0, 0, 1]
        elif p1 == p2 == "S" and p3 == "R":
            return [0, 0, 0, 1]

        ## Player 2 wins
        elif p1 == p3 == "R" and p2 == "P":
            return [0, 0, 1, 0]
        elif p1 == p3 == "P" and p2 == "S":
            return [0, 0, 1, 0]
        elif p1 == p3 == "S" and p2 == "R":
            return [0, 0, 1, 0]

        ## Player 1 wins
        elif p2 == p3 == "R" and p1 == "P":
            return [0, 1, 0, 0]
        elif p1 == p2 == "P" and p1 == "S":
            return [0, 1, 0, 0]
        elif p1 == p2 == "S" and p1 == "R":
            return [0, 1, 0, 0]

        # Failsafe
        return tie

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False