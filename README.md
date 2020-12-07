# DistributedProject
Multiplayer game project for Distributed Systems course.

# Tutorial links
We used the code in this video as a base for the game: https://www.youtube.com/watch?v=McoDjOCb2Zo

# Running the game

1. Install python 3 and [pygame](https://www.pygame.org/)
1. Start server with `python3 server.py`
1. Start desired number of clients with `python3 client.py`

# Extra info

The game is a multiplayer Rock Paper Scissors with 3 players in a game session. The game will start when all 3 players have joined the session. The amount of game sessions scale as the server will create more sessions if more players join. The application uses Master-Slave architecture, and all communication goes through the server. Made with Python and Pygame.

More documentation:
* Pinned in telegram





