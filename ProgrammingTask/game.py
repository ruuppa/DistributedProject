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

        self.p2HasJoined = False
        self.p3HasJoined = False

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

    def allWent(self):
        return self.p1Went and self.p2Went and self.p3Went

    def playerJoined(self, sendto):
        if sendto == 1:
            self.p2HasJoined = True
        elif sendto == 2:
            self.p3HasJoined = True

    def p2Joined(self):
        return self.p2HasJoined

    def p3Joined(self):
        return self.p3HasJoined

    def outcome_for_player(self, player):
        if (
            (self.winner() == [0, 1, 0, 0] and player == 0)
            or (self.winner() == [0, 0, 1, 0] and player == 1)
            or (self.winner() == [0, 0, 0, 1] and player == 2)
            or (self.winner() == [0, 1, 1, 0] and (player == 0 or player == 1))
            or (self.winner() == [0, 1, 0, 1] and (player == 0 or player == 2))
            or (self.winner() == [0, 0, 1, 1] and (player == 1 or player == 2))
        ):
            return "You Won!"
        elif self.winner() == [1, 0, 0, 0]:
            return "Tie Game!"
        else:
            return "You Lost..."

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        p3 = self.moves[2].upper()[0]

        tie = [1, 0, 0, 0]

        # tie:    [1, 0, 0, 0]
        # p1 Win: [0, 1, 0, 0]
        # p2 Win: [0, 0, 1, 0]
        # p3 Win: [0, 0, 0, 1]

        # Tie
        if p1 == p2 == p3:
            return tie
        elif p1 != p2 and p1 != p3 and p2 != p3:
            return tie

        # 2 winners
        elif p1 == p2 == "R" and p3 == "S":
            return [0, 1, 1, 0]
        elif p1 == p2 == "P" and p3 == "R":
            return [0, 1, 1, 0]
        elif p1 == p2 == "S" and p3 == "P":
            return [0, 1, 1, 0]

        elif p1 == p3 == "R" and p2 == "S":
            return [0, 1, 0, 1]
        elif p1 == p3 == "P" and p2 == "R":
            return [0, 1, 0, 1]
        elif p1 == p3 == "S" and p2 == "P":
            return [0, 1, 0, 1]

        elif p2 == p3 == "R" and p1 == "S":
            return [0, 0, 1, 1]
        elif p1 == p2 == "P" and p1 == "R":
            return [0, 0, 1, 1]
        elif p1 == p2 == "S" and p1 == "P":
            return [0, 0, 1, 1]

        # 1 winner
        elif p1 == p2 == "R" and p3 == "P":
            return [0, 0, 0, 1]
        elif p1 == p2 == "P" and p3 == "S":
            return [0, 0, 0, 1]
        elif p1 == p2 == "S" and p3 == "R":
            return [0, 0, 0, 1]

        elif p1 == p3 == "R" and p2 == "P":
            return [0, 0, 1, 0]
        elif p1 == p3 == "P" and p2 == "S":
            return [0, 0, 1, 0]
        elif p1 == p3 == "S" and p2 == "R":
            return [0, 0, 1, 0]

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
