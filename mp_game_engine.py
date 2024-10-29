"""Multi-player components with AI for the game

This module goes towards the more advanced parts of the game, implementing
multi-player components into battleships such as an Ai opponent that challenges
the player in the game. Moreover, this module also allows for multi-player
development tests on the terminal to test the more advanced functionality of
the game.

Attributes
----------
players : (dict{str : (list[list]), dict{str : int}})
    This module_level stores the names for the player and the Ai bot, as
    well as the board and the battleships for each player
"""


import random
from components import initialise_board, create_battleships, place_battleships, display_board
from game_engine import attack, cli_coordinates_input
from battleships_ai import hunt_and_target_ai, parity_ai

players = {}

def generate_attack(algorithm = '', ship_detection = None, ai_hitlog = None, board_size = None):
    """Randomly generates an attack for the AI
    
    Args:
        algorithm (str): The selected difficulty of the Ai
        ship_detection (bool, bool, tuple(int, int), list[tuple]): A packed array that contains:
            ship_detected (bool): Determines whether the Ai is tracking one of the player's ships
            shiphit (bool): Determines whether the Ai has hit one of the player's ships
            lastco_ords (tuple(int, int)): The last co_ord that the Ai has shot
            stackco_ords (list[tuple]): A stack of coordinates that the Ai is going to shoot next
        ai_hitlog (list[tuple(int, int)]): A log of all the coordinates that the Ai has hit 
            on the player's board
        board_size (int): The size of the player's board

    Returns:
        hunt_and_target_ai (ship_detection, ai_hitlog, board_size): A function that generates 
            specified coordinates that is determined by whether the Ai has hit a player's ship,
            otherwise it will generate a random coordinate
        parity_ai (ship_detection, ai_hitlog, board_size): A function that generates specified
            coordinates that is determined by whether the Ai has hit a player's ship, otherwise it
            will generate a random coordinate based on the checkerboard method
        coordinates (tuple(int, int)): The coordinates of the attack that is randomly generated
    """

    if algorithm == 'simple':
        # Checks if the Ai is using a simple algorithm
        coordinates = (random.randrange(0, board_size), random.randrange(0, board_size))
        # Generates a random coordinate
        return tuple(coordinates)

    if algorithm == 'hunt&target':
        # Checks if the Ai is using a hunt&target algorithm
        return hunt_and_target_ai(ship_detection, ai_hitlog, board_size)

    if algorithm == 'parity':
        # Checks if the Ai is using a parity algorithm
        return parity_ai(ship_detection, ai_hitlog, board_size)

    coordinates = (random.randrange(0, 10), random.randrange(0, 10))
    # Default board size with random coordinates
    return tuple(coordinates)

def ai_opponent_game_loop():
    """Loops the game for the AI opponent until the game finishes
    
    Args:
        No arguments
    Returns:
        Nothing is returned
    """

    print('Welcome to battleships')
    player_board = initialise_board(10)
    # Initialises the player's board
    player_ships = create_battleships('battleships.txt')
    # Creates the player's ships
    player_board = place_battleships(player_board, player_ships, 'custom')
    players['Player'] = (player_board, player_ships)
    # Stores the player's data into the dictionary of players

    ai_board = initialise_board(10)
    # Initialises the AI's board
    ai_ships = create_battleships('battleships.txt')
    # Creates the AI's ships
    ai_board = place_battleships(ai_board, ai_ships, 'random')
    players['AI Bot'] = (ai_board, ai_ships)
    # stores the AI's data into the dictionary of players

    player_turn = True
    # Use to determine whether it is the player's turn or if it's the AI' s turn
    game_finished = False
    while game_finished is False:
        display_board(players['Player'][0])
        # Displays the player's board
        print('\n\n')
        display_board(players['AI Bot'][0])
        # Displays the AI's board
        if player_turn:
            co_ords = cli_coordinates_input()
            hit_register = attack(co_ords, (players['AI Bot'])[0],
                                  (players['AI Bot'])[1])
            # Initiates an attack on the AI board

            if hit_register:
                print('Hit')
            else:
                print('Miss')

            if all(ships == 0 for ships in players['AI Bot'][1].values()):
                # Game ends when all the AI ships have been sunk
                game_finished = True
                print(f'Game Over, {list(players.keys())[0]} WINS!!!') #Display player name
            player_turn = False
            # Ends the player's turn

        else:
            co_ords = generate_attack('simple', None, None, board_size= 10)
            # Generates a random coordinate for the AI
            hit_register = attack(co_ords, players['Player'][0],
                                  players['Player'][1])
            # Initiates an attack on the player's board
            print(co_ords)
            if hit_register:
                print('Hit')
            else:
                print('Miss')

            if all(ships == 0 for ships in players['Player'][1].values()):
                # Game ends when all the player's ships have been sunk
                game_finished = True
                print(f'Game Over, {list(players.keys())[0]} LOSES!!!')
            player_turn = True
            # Ends the AI's turn

if __name__ == '__main__':
    ai_opponent_game_loop()
                