"""The main backbone components for the game

This module is designed to be the main backend of the battleships game, providing the
fundamental mechanics of the game, such as developing the board, creating the 
battleships from a text file and placing the created ships on the boards using a
variety of algorithms.
"""


import random
import json

def initialise_board(size):
    """Initialises the board for the player
    
    Args:
        No arguments
    Returns:
        board (list[list]): Returns the whole board for the player, 
            where each individual node is empty
    """

    board_size = size
    board = [[None for x in range(board_size)] for y in range(board_size)]
    # Creating the board by setting it as a 10 by 10 list of lists
    return board

def create_battleships(filename = "battleships.txt"):
    """Creates the battleships for the player
    
    Args:
        No arguments
    Returns:
        battleships (dict): Returns the battleships from the text file, 
            where the names of the ships as the key and the size of the ships as the values.
    """

    with open(filename, 'r', encoding='utf-8') as file:
    # Reads all the lines in the "battleships.txt" file
        battleships = {}
        for line in file:
            # Individually reads each line in the file
            line = line.split(':')
            # Split each line of the file by the ':'
            key, val = line[0], int(line[1])
            battleships[key] = val
            # Appending the 'battleships' dictionary by adding the key and value of each line
    return battleships

def place_battleships(board = None, ships = None, algorithm = ''):
    """Placing ships on to the board

    Args:
        board (list[list]): The player's board used for the game
        battleships (dict[str:int]): The player's ships that are going to be placed on the board
        algorithm (str): The style of ship placement that is used to increase 
            the complexity of the game
    Returns:
        simple_placement(): A function that returns the player's board with the player's ships
            placed along the first few rows on the board
        random_placement(): A function that returns the player's board with the player's ships
            placed in random coordinates on the board
        custom_placement(): A function that returns the player's board wtih the player's ships
            placed in set coordinates based on the coordinates received from the 'placement.json'
            file
    """

    if algorithm == 'simple':
        return simple_placement(board, ships)
    if algorithm == 'random':
        return random_placement(board, ships)
    if algorithm == 'custom':
        return custom_placement(board, ships)
    return board

def simple_placement(board, battleships):
    """Places the ships on the board horizontally on the first few rows
    
    Args:
        board (list[list]): The player's board used for the game
        battleships (dict[str:int]): The player's ships that are going to be placed on the board
    Returns:
        board (list[list]): The player's board with the player's ships placed on the first few rows
            on the board
    """

    y = 0
    # Starts at the very top row
    for ships, value in battleships.items():
    # Splits the dictionary between the ship name and length of ship
        for x in range(int(value)):
            board[y][x] = ships
            # Assigns the slot at the coordinate on the board to the ship
        y += 1
        # Increments after each ship
    return board

def random_placement(board, battleships):
    """Places the ships randomly on the board in random orientations and random paths

    Args:
        board (list[list]): The player's board used for the game
        battleships (dict[str:int]): The player's ships that are going to be placed on the board
    Returns:
        board (list[list]): The player's board with the player's ships placed on random
            coordinates with random orientations across the board
    """

    for ships, value in battleships.items():
        valid_placement = False
        # Used to determine whether if the placement of the ship is valid or not
        while valid_placement is False:
        # Repeats if the placement of the ship is not valid
            x = random.randrange(0,10)
            y = random.randrange(0,10)
            # Randomly generates the x and y coordinates for the ship
            vert_orient = random.getrandbits(1)
            # Randomly generates the orientation for the ship (Vertical or Horizontal)
            placement = random.getrandbits(1)
            # Randomly determines the placement method;
            # Vertical: Up or Down
            # Horizontal: Left or Right

            ship_placement = x, y, vert_orient, placement
            value = int(value)
            if vert_orient:
            # Checks if the ship uses vertical orientation

                # If statement to check whether the placement of the ship is within
                # the periphery of the board and the placement is valid
                if (y + value < 10 and valid_board_placement(board, value, ship_placement)
                    and placement):
                    valid_placement = True
                    for count in range(value):
                        board[y + count][x] = ships
                if (y - value > -1 and valid_board_placement(board, value, ship_placement)
                    and not placement):
                    valid_placement = True
                    for count in range(value):
                        board[y - count][x] = ships
            else:
                # Selection statement when the ship uses horizontal instead of vertical orientation
                if (x + value < 10 and valid_board_placement(board, value, ship_placement)
                    and placement):
                    valid_placement = True
                    for count in range(value):
                        board[y][x + count] = ships
                if (x - value > -1 and valid_board_placement(board, value, ship_placement)
                    and not placement):
                    valid_placement = True
                    for count in range(value):
                        board[y][x - count] = ships
    return board

def custom_placement(board, battleships):
    """Places the ships on the board based on the values given by the json file
    
    Args:
        board (list[list]): The player's board used for the game
        battleships (dict[str:int]): The player's ships that are going to be placed on the board
    Returns:
        board (list[list]): The player's board with the player's ships placed in set coordinates
            and orientation given by the 'placement.json' file
    """

    with open('placement.json', encoding = "utf-8") as file:
        # Reads the 'placement.json' file
        config_file = json.load(file)
        # Loads the json data
        for ship_type, ship_pos in config_file.items():
        # Splits the json between the type of ship and the position of the ship
            valid_placement = False
            while valid_placement is False:
                for ship, value in battleships.items():
                    x, y, orient = ship_pos
                    # Gets the x, y and orient values from the json file
                    x = int(x)
                    y = int(y)
                    placement = random.getrandbits(1)
                    # Randomly determines the placement method;
                    # Vertical: Up or Down
                    # Horizontal: Left or Right

                    # Checks the orientation, placement, whether the ships match
                    # and if the ship is within the periphery of the board with
                    # valid placement
                    if (orient == 'v' and (y - int(value) < 0 or placement) and
                        ship_type == ship and
                        valid_board_placement(board, value, [x, y, orient, True])):
                        valid_placement = True
                        for count in range(int(value)):
                            board[y + count][x] = ship
                    elif (orient == 'v' and (y + int(value) > 10 or not placement) and
                          ship_type == ship and
                          valid_board_placement(board, value, [x, y, orient, False])):
                        valid_placement = True
                        for count in range(int(value)):
                            board[y - count][x] = ship
                    elif (orient == 'h' and (x - int(value) < 0 or placement) and
                          ship_type == ship and
                          valid_board_placement(board, value, [x, y, orient, True])):
                        valid_placement = True
                        for count in range(int(value)):
                            board[y][x + count] = ship
                    elif (orient == 'h' and (x + int(value) > 10 or not placement) and
                          ship_type == ship and
                          valid_board_placement(board, value, [x, y, orient, False])):
                        valid_placement = True
                        for count in range(int(value)):
                            board[y][x - count] = ship
    return board

def valid_board_placement(board, ship_size, ship_placement):
    """Checks and validates whether the placement of the ship does not collide with any other ship 
        or the border of the board
    
    Args:
        board (list[list]): The player's board
        ship_size (int): The length of the ship that is being placed
        ship_placement ([int, int, (int/str), bool]): An array that holds the x and y coordinates, 
            the orientation and the placement method of the ship

    Returns:
        bool: True if all the coordinates that the ship will cover are empty slots that do not
            contain another ship. False if all the coordinates that the ship will cover clashes 
            or overlaps another ship or the ship goes beyond the border of the player's board 
    """

    x, y, orient, placement = ship_placement
    # Extracts the coordinates, orientation and the placement method from the array
    for count in range(ship_size):
    # Checks if the ship collides with another ship or the placement goes beyond the border
        if y + ship_size < 10 and (orient in {'v', 1}) and placement:
            if board[y + count][x] is not None:
                return False
        elif y - ship_size > -1 and (orient in {'v', 1}) and not placement:
            if board[y - count][x] is not None:
                return False
        elif x + ship_size < 10 and (orient in {'h', 0}) and placement:
            if board[y][x + count] is not None:
                return False
        elif x - ship_size > -1 and (orient in {'h', 0}) and not placement:
            if board[y - count][x - count] is not None:
                return False
    return True

def display_board(board):
    """Displays the board on the terminal
    
    Args:
        board (list[list]): The player's board that contains the player's ships
    Returns:
        Returns nothing
    """

    for y in range(len(board)):
        # Reads each row of the board
        for x in range(len(board[y])):
            #Reads each column for each row on the board

            # Prints each slot on the board
            print(f'[{board[y][x]}]', end='')
        print()
