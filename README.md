# BATTLESHIPS GAME

## Introduction
This project is my modern take on the classic retro game battleships, bringing it to life on a web interface using Flask. This project was created as part of an assessment. Inspired by the nostalgia of old-school naval warfare games, the battleships game features two competitors — a player and an AI. Each participant has a 10x10 grid and strategically places five ships on their board. The game unfolds as both the player and AI take turns attempting to sink each other's ships until only one competitor remains victorious. There are three game modes for the player to play in:
- Single-player interface
- Multi-player interface
- Webpage interface
This instalment of battleships involves a variety of difficulty levels to choose from, incorporating tactics and stratagems to increase the probability of winning, which can bring about some challenge towards the player in achieving victory. A few parts of this project have been quite challenging to create and quite time-consuming, but it was overall fun to make, especially the usage of Flask and creating advanced AI.

## Prerequisites
- Python 3.11.5 64-bit
- Pylance
- flask-snippets v0.1.3
	- To install, type in the terminal: pip install flask
- Pylint 3.0.2
- Pytest
	- Pytest-depends
	- Pytest-cov

## How to play
### Single-player interface
- Run the 'game_engine.py' module
- Enter an input when it asks for the user's input
	- *NOTE: MUST ENTER INPUT AS [0-9],[0-9]*
- Repeat until you win the game and all the ships have sunk

### Multi-player interface
- Run the 'mp_game_engine.py' module
- Enter an input when it asks for the user's input
	- *NOTE: MUST ENTER INPUT AS [0-9],[0-9]*
- Repeat until either:
	- You win the game by sinking all the AI's ships
	- The AI wins the game by sinking all your ships

### Webpage interface
- Open the 'programming coursework' folder in vscode
- Run the 'main.py' module
- Open the file 'flask.log'
- On the line: 'Running on http://127.0.0.1:5000', open the hyperlink or copy the URL onto your desired web browser
- To attack, click on a coordinate in the main template
- Repeat until either:
	- You win the game by sinking all the Ai's ships (message pop-up will display)
	- The AI wins the game by sinking all your ships (message pop-up will display)

#### Placement:
- Add '/placement' to the URL or open this http://127.0.0.1:5000/placement to adjust and permanently change the placement of your ships
- Press R to change the orientation of your placements
- Click on the "Send Game" button to finish configuration and return back to the game (message pop-up will display)

#### Changing Difficulty:
- Add **'/difficulty:algorithm'** to the URL, with algorithm being the type of algorithm that the AI is going to use
- All the types of algorithms are:
	- **'/difficulty:normal'** - Sets the difficulty to *normal* mode
	- **'/difficulty:hunt&target'** - Sets the difficulty to *hunt&target* mode
	- **'/difficulty:parity'** - Sets the difficulty to *parity* mode

## License
Copyright 2023

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
