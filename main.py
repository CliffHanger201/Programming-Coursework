"""Renders the flask environment for the Battleships game

This module implements the battleships game onto a webpage interface
using the flask environment. This module can do this by rendering
pre-made html templates to display the boards for the player and Ai
bot as well a html template for placing the ships that collects and
stores the data into a json file for other battleship games.

Furthermore, this module processes the attack for both the player
and the Ai, which logs it and responds to it with the appropiate message.
As an extension, this module also allows for the change in Ai difficulty
from the URL.

Attributes
----------
player_board : list[list]
    The player's board in the battleships game
player_ships : dict{str : int}
    The player's ships and its' remaining hitpoints in the game
player_hitog : list[tuple]
    Log of all the coordinates that the player has shot in this game
ai_board : list[list]
    The Ai's board in the battleships game
ai_ships : dict{str : int}
    The Ai's ships and it's remaining hitpoints in the game
ai_hitlog : list[tuple]
    Log of all the coordinates that the Ai has shot in this game
AI_ALGORITHM : str
    The type of algorithm used by the Ai against the player
lastco_ord : tuple(int, int)
    The last coordinate that the Ai has shot
stackco_ords : list[tuple]
    Stack of coordinates that the Ai is going to shoot next
SHIP_DETECTED : bool
    Determines whether the Ai is tracking a ship after hitting one or not
SHIPHIT : bool
    Validation for when the Ai has hit a ship or not
"""


import json
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from components import initialise_board, create_battleships, place_battleships
from game_engine import attack
from mp_game_engine import generate_attack

player_board = []
player_ships = {}
player_hitlog = []
ai_board = []
ai_ships = {}
ai_hitlog = []
AI_ALGORITHM = 'parity'
lastco_ord = ()
stackco_ords = []
SHIP_DETECTED = False
SHIPHIT = False

app = Flask(__name__)

logging.basicConfig(filename='flask.log', level=logging.DEBUG)
# Logs each event that occurs in the runtime of flask

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """Handles the GET requests and POST requests for the ship placement interface
    
    Description:
        "GET": Renders the placement template onto the placement interface using Flask
        "POST": Collects the coordinates and orientations of the ships that were placed down on the
            template and stores them in the 'placement.json' file
    Args:
        No arguments
    Returns:
        render_template(): Function that renders the placement template for the placement interface
        jsonify(): Function that displays a message on the flask interface
    Responses:
        "GET" 200: The placement template has successfully rendered onto flask
        "POST" 200: The json data for the placement of the ships on the placement interface has been
            successfully stored, returning user back to the main template

    """

    if request.method == 'GET':
        # Receives the GET request when the URL is put in
        logging.info('Rendering placement template...')
        ships = create_battleships('battleships.txt')
        logging.info('SUCCESS! Placement template has been rendered')
        return render_template('placement.html', ships=ships, board_size = 10)
        # Renders the html for the ship placement html

    if request.method == 'POST':
        # Receives the POST request when the 'send game' button is pressed
        logging.info('Storing data into placement.json file')
        data = request.get_json()
        # Gets the json data for all the player's ships on the placement template
        # This includes: coordinates and orientation

        with open('placement.json', 'w', encoding= 'utf-8') as file:
        # Opens the 'placement.json file for overwriting
            json.dump(data, file, indent=4)
            # 'dumps' the data into the placement file by overwriting it
        file.close()
        # Closes the file
        logging.info('SUCCESS! Data stored into placement.json file')
        return jsonify({'message' : 'Received'}), 200
        # Returns a message displaying that the data has been received

@app.route('/', methods=['GET'])
def root():
    """The root foundation of the flask environment for the game
    
    Description:
        "GET": Renders and displays the main template on the root interface, where the
            player will get to the game, as well as creating the player's board
            and the Ai's board
    Args:
        No arguments
    Returns:
        render_template(): A function that renders the main base template for the battleships game
    Responses:
        200: The main battleships template for flask has been successfully rendered
    """

    if request.method == 'GET':
        global player_board, player_ships, ai_board, ai_ships, AI_ALGORITHM

        logging.info("Creating the player board and the player's ships")
        player_board = initialise_board(10)
        player_ships = create_battleships('battleships.txt')
        # Initialises the player's board and creates the player's battleships

        logging.info("Creating the Ai board and the Ai's ships")
        ai_board = initialise_board(10)
        ai_ships = create_battleships('battleships.txt')
        # Initialises the Ai's board and creates the Ai's battleships

        global player_hitlog, ai_hitlog, lastco_ord, stackco_ords, SHIP_DETECTED, SHIPHIT

        player_hitlog = []
        ai_hitlog = []
        lastco_ord = ()
        stackco_ords = []
        SHIP_DETECTED = False
        SHIPHIT = False

        with open('placement.json', encoding = "utf-8") as file:
        # Opens the 'placement.json' file to read from ('r' is automatic)
            config_file = json.load(file)
            # Loads the data from the config file
            for ship_type, ship_pos in config_file.items():
                for ship, value in player_ships.items():
                    x, y, orient = ship_pos
                    x = int(x)
                    y = int(y)
                    # Places the ships onto the player's board
                    if (orient == 'v' and ship_type == ship):
                        for count in range(int(value)):
                            player_board[y + count][x] = ship
                    elif (orient == 'h' and ship_type == ship):
                        for count in range(int(value)):
                            player_board[y][x + count] = ship
            file.close()
            logging.info('SUCCESS! Player board has been created')
        ai_board = place_battleships(ai_board, ai_ships, 'random')
        logging.info('SUCCESS! Ai board has been created')
        return render_template('main.html', player_board=player_board)
        # Renders the main template onto Flask
    return None

@app.route('/attack', methods=['GET'])
def process_attack():
    """Processes the player's attack and the AI's attack
    
    Description:
        "GET": Retrieves the coordinates of the attack from the position of the player's mouse 
            and generates the Ai's attack; continues until either the player or the Ai
            win the game
    Args:
        No arguments
    Returns:
        jsonify(): Function that displays a message on the flask interface
    Raises:
        TypeError: The function breaks and does not return a valid coordinate to the attack
            function
    Responses:
        200:
            Description: The attack has been successfully registered
        500: 
            Description: The function for did not return a valid response as the function
                returned None, this is because the player clicked on a coordinate
                that was already hit
    """

    if request.method == 'GET':
        global player_hitlog, ai_hitlog, lastco_ord, SHIP_DETECTED, stackco_ords, SHIPHIT

        logging.debug('Retrieving coordinates...')
        x = request.args.get('x')
        y = request.args.get('y')
        # Retrieves the x and y coordinates from the player's mouse on the root interface
        coords = (x, y)
        # Stores the x and y coordinates into a tuple
        logging.debug('Coordinates received!')

        ship_detection = [SHIP_DETECTED, SHIPHIT, lastco_ord, stackco_ords]
        # Packs the ship_detection variables
        logging.debug('Generating Ai coordinates...')
        if AI_ALGORITHM == 'simple' or SHIP_DETECTED is False:
        # Checks if the Ai uses a simple algorithm or whether the ai is not tracking a ship
            ai_coords = generate_attack('simple', ship_detection,
                                        ai_hitlog, board_size=10)
        else:
            ai_coords, stackco_ords = generate_attack(AI_ALGORITHM, ship_detection,
                                                    ai_hitlog, board_size=10)

        while ai_coords in ai_hitlog:
        # Repeats the function until the algorithm generates a new and unique coordinate
        # that has not been shot

            if AI_ALGORITHM == 'simple' or SHIP_DETECTED is False:
                ai_coords = generate_attack('simple', ship_detection,
                                            ai_hitlog, board_size=10)
            else:
                ai_coords, stackco_ords = generate_attack(AI_ALGORITHM, ship_detection,
                                                        ai_hitlog, board_size=10)

        logging.debug('Ai coordinates successfuly generated!')
        if stackco_ords == []:
        # Checks if there are no more coordinates in the stack and therefore
        # no longer tracking
            SHIP_DETECTED = False

        if coords not in player_hitlog:
        # Checks if the player's chosen coordinate is not in the player's hitlog
            hit_register = attack(coords, ai_board, ai_ships)
            # Initiates the attack on the Ai's board
            if hit_register:
                logging.debug('Player has hit an Ai ship')
            else:
                logging.debug('Player misses')
            player_hitlog.append(coords)
            # Adds the coordinate to the player's hitlog
            logging.debug('Coordinates have been added to players hitlog')

            ai_hit_register = attack(ai_coords, player_board, player_ships)
            # Initiates the attack on the player's board
            ai_hitlog.append(ai_coords)
            #Adds the coordinate to the Ai's hitlog
            logging.debug('Ai coordinates have been added to the Ai hitlog')

            if ai_hit_register:
                # Checks if the ai has hit one the player's ships
                lastco_ord = ai_coords
                SHIP_DETECTED = True
                SHIPHIT = True
                logging.debug('Ai has hit a player ship')
            else:
                SHIPHIT = False
                logging.debug('Ai bot misses')

            if all(ships == 0 for ships in ai_ships.values()):
            # Checks if all the ai's ships have been sunk
                logging.debug('Player has won the game')
                return jsonify({'hit': hit_register,
                                'AI_Turn': ai_coords,
                                'finished': 'Game Over, Player Wins!'})

            if all(ships == 0 for ships in player_ships.values()):
            # Checks if all the player's ships have been sunk
                logging.debug('Ai Bot has won the game')
                return jsonify({'hit': hit_register,
                                'AI_Turn': ai_coords,
                                'finished': 'Game Over, Player Loses!'})

            return jsonify({'hit': hit_register,
                            'AI_Turn': ai_coords})

        logging.error('Repeated coordinate has been shot again')
        raise TypeError('Player clicked on a square that is already hit')


@app.route('/difficulty:normal')
def normal_difficulty():
    """Changes the Ai back to normal difficulty
    
    Description:
        Calls the ai algorithm and resets it back to using the simple algorithm
        at normal difficulty
    Args:
        No arguments
    Returns:
        redirect(url_for('root')): Brings the user back to the main template of the game
    """

    global AI_ALGORITHM
    AI_ALGORITHM = 'simple'
    logging.info('Difficulty has been switched to normal')
    return redirect(url_for('root'))

@app.route('/difficulty:hunt&target')
def huntdifficulty():
    """Changes the Ai difficulty to hunt & target mode difficulty
    
    Description:
        Calls the Ai algorithm and changes the difficulty of the Ai to hunt & target difficulty
    Args:
        No arguments
    Returns:
        redirect(url_for('root')): Brings the user back to the main template of the game
    """

    global AI_ALGORITHM
    logging.info('Difficulty has been switched to hunt & target difficulty')
    AI_ALGORITHM = 'hunt&target'
    return redirect(url_for('root'))

@app.route('/difficulty:parity')
def paritydifficulty():
    """Changes the Ai difficult to parity mode difficulty
    
    Description:
        Calls the Ai algorithm and changes the difficulty of the Ai to parity difficulty
    Args:
        No arguments
    Returns:
        redirect(url_for('root')): Brings the user back to the main template of the game
    """

    global AI_ALGORITHM
    AI_ALGORITHM = "parity"
    logging.info('Difficulty has been switched to parity difficulty')
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run()
