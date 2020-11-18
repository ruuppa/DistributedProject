# Note!
This is not a merge-candidate, and should only be used for testing the game-logic, rather than the whole package. The working code is currently in the "temp" -folder, rather than the main folder.
Running the game works as per normal:
1. Run server.py
1. Run the desired amount of client.py, clicking on the window itself to make them join the server.

# DistributedProject
Multiplayer game project for Distributed Systems -course

# Tutorial links
For a base for the game: https://www.youtube.com/watch?v=McoDjOCb2Zo

# Basic concepts etc.
Multiplayer game, small competetitive, real-time
* Using pygame as a framework for graphics and for ease of use
* Using tutorial as a base:
	https://www.youtube.com/watch?v=McoDjOCb2Zo

# Running the game

1. Install python 3 and [pygame](https://www.pygame.org/)
1. Start server with `python3 server.py`
1. Start desired number of clients with `python3 client.py`

# TODO

* Implement minimal class for the KSP game, which contains the game state

* Pressing S key starts the game, and game state changes

* ...

Name:
* Dicing Against Death, or DAD (name pending)

Goal:
* Multiplayer game
* 3 players compete together to see who is the winner

Programming language:
* Python

Repository:
* Git
https://github.com/ruuppa/DistributedProject

Outline for the code:
* Server
* Networking
* Scalable client (3 to X)

Strategy:
* Evaluation:
** Game works
* Demonstration:
** Playing the game

More documentation:
* https://docs.google.com/document/d/1ruCcRXmwBzCM8GiibeN3pV-6m48wwiN59-pK31F6s4A/edit?usp=sharing
