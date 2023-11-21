# Formal_Methods_in_Robotic-reinforcement-learning-projects-Creating user-friendly Wumpus Game.
files = POMDP_Wumpus.py, Wumpus_POMDP.py, and all images of gold, pit, wumpus, and robots.

Wumpus World POMDP Game
Introduction
This repository contains the implementation of a Partially Observable Markov Decision Process (POMDP) game, "Wumpus World", with a graphical interface using Pygame. The game simulates a robot navigating a grid world with pitfalls and a randomly moving Wumpus. The objective is to safely navigating the robot to collect gold while avoiding the Wumpus and pits.

Features
Implementation of POMDP in a grid world environment.
Graphical animation using Pygame, showing the robot's actions and Wumpus's movements.
Attractor for reachability objectives to guide the robot.
Randomized Wumpus movement and environment generation.
Installation
To run this project, you'll need Python and Pygame installed on your system.

Prerequisites
Python (Version 3. x)
Pygame
Setup
Clone the repository:
bash
Copy code
git clone https://github.com/[your-username]/wumpus-world-pomdp.git
Navigate to the cloned directory:
bash
Copy code
cd wumpus-world-pomdp
Usage
To start the game, run the following command in the terminal:

Copy code
python wumpus_game.py
Structure
wumpus_game.py: Main game script that integrates POMDP logic with Pygame.
WumpusWorldPOMDP.py: Contains the POMDP model of the game.
/assets: Directory containing graphical assets like images and sound files.
README.md: This file, contains project documentation.
Contributing
Contributions to this project are welcome. To contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
License
It is distributed under the MIT License. See LICENSE for more information.

Acknowledgments
Mention any inspirations, code snippets, etc.

