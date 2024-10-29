"""Module that manages the mechanics of the game

This module manages the simple mechanics of the game such as the simple attack
function on another player's board by receiving the coordinates from the player's
input. This also allows single-player development tests on the terminal to test
the functionality of the game.
"""



from ast import literal_eval
from components import create_battleships, initialise_board, place_battleships, display_board

def attack(coordinates, board, battleships):
    """Initiates an attack on the coordinates on the enemies board
    
    Args:
        coordinates (tuple(int, int)): The coordinates of the attack on the enemy's board
        board (list[list]): The enemy's board that contains the enemy's ships
        battleships (dict[str : int]): The enemy's ships and their remaining slots
    Returns:
        bool: True if the coordinates hits an enemy ship. False if the coordinates does not hit 
            an enemy ship and instead misses the shot
    """

    x, y = coordinates
    # Get the x and y coordinates from the tuple
    x = int(x)
    y = int(y)
    if board[y][x] is not None:
        # Checks if the coordinate on the board is not empty
        # Returns true if a ship has been hit
        battleships[board[y][x]] = battleships.get(board[y][x]) - 1
        board[y][x] = None
        return True
    # Returns false if the attack has shot an empty slot and missed a ship
    return False

def cli_coordinates_input():
    """Gets the coordinates that the user inputs or presses
    
    Args:
        No arguments
    Returns:
        coordinates (tuple(int, int)): The coordinates of the attack that is generated 
            from the user's input
    """

    loc = input('Enter the coordinates of your shot: ').split(',')
    # Gets the location from the user's input and splits the string
    coordinates = tuple(literal_eval(i) for i in loc)
    # Checks if the values in the 'loc' variable are integers and then stores them in the tuple
    return coordinates

def simple_game_loop():
    """Loops the game until the game for the player until the game is finished
    
    Args:
        No arguments
    Returns:
        Nothing is returned
    """

    print('Welcome to battleships')
    board = initialise_board(10)
    # Initialises the board
    battleships = create_battleships('battleships.txt')
    # Creates the battleships
    board = place_battleships(board, battleships, 'custom')
    # Places the battleships onto the board via custom placement

    game_finished = False
    # Used for repeating the game until it is finished

    while game_finished is False:
    # Repeats if the game is not finished
        display_board(board)
        co_ords = cli_coordinates_input()
        # Gets the coordinates from the player's input
        hit_register = attack(co_ords, board, battleships)
        # Checks if the coordinates hits a ship

        if hit_register:
        # Checks whether the player has hit a ship
            print('Hit')
        else:
            print('Miss')

        if all(ships == 0 for ships in battleships.values()):
        # Checks if all the positions of the ships have been shot down
            game_finished = True

    print('Game Over')
    # Prints the game over text

if __name__ == '__main__':
    simple_game_loop()
