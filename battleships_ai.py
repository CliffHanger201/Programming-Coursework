"""The library of battleship AI for attack coordinates

This module expands on strengthening the Ai to make it harder
for the player to overcome the challenge and as it employs more
strategies and tactics to increase the change of the Ai winning
the game.
"""


import random

def hunt_and_target_ai(ship_detection, ai_hitlog, board_size):
    """Advanced version of the battleships Ai
    
    Description:
        The 'Hunt and Target Ai' utilises a more sophisticated algorithm where it targets a ship 
        when it knows it has found its target. It does this by initially shooting a random 
        coordinate on the player's board. Once it has found a ship, it will then mark each 
        adjacent or lateral coordinate next to the attack coordinate.

    Args:
        ship_detection (bool, bool, tuple(int, int), list[tuple]): A packed array that contains:
            ship_detected (bool): Determines whether the Ai is tracking one of the player's ships
            shiphit (bool): Determines whether the Ai has hit one of the player's ships
            lastco_ords (tuple(int, int)): The last co_ord that the Ai has shot
            stackco_ords (list[tuple]): A stack of coordinates that the Ai is going to shoot next
        ai_hitlog (list[tuple(int, int)]): A log of all the coordinates that the Ai has hit 
            on the player's board
        board_size (list[list]): The player's board that contains the player's ships

    Returns:
        tuple(int, int): The coordinate for the Ai's next attack 
    """
    ship_detected, hit_register, lastco_ord, stackco_ords = ship_detection
    if ship_detected:
        # Checks to see if the Ai has detected a ship

        x, y = lastco_ord
        x, y = int(x), int(y)
        # Gets the x and y from the last coordinate

        if hit_register:
        # Checks if the Ai had hit a ship
            for xcount in range(-1, 2, 1):
            # Selects each adjacent x coordinate
                co_ord = (x + xcount, y)
                if co_ord not in stackco_ords and co_ord not in ai_hitlog:
                # Checks if the coordinate has not already been used and is unique
                    stackco_ords.append(co_ord)
                    # Adds the coordinate to the stack

            for ycount in range(-1, 2, 1):
            # Selects each adjacent y coordinate
                co_ord = (x, y + ycount)
                # Repeats the function again
                if co_ord not in stackco_ords and co_ord not in ai_hitlog:
                    stackco_ords.append(co_ord)

        if len(stackco_ords) > 0:
        # Checks if the stack is not empty
            shotco_ord = stackco_ords[-1]
            # Gets the last item in the stack and sets it as the new coordinate
            del stackco_ords[-1]
            # Removes the last item in the stack
            return shotco_ord, stackco_ords

    x = random.randrange(0, board_size)
    y = random.randrange(0, board_size)
     # Randomly generates a coordinate
    return (x, y), stackco_ords

def parity_ai(ship_detection, ai_hitlog, board_size):
    """An even harder Ai that incorporates the hunt and target Ai
    
    Description:
        Similar to the 'Hunt and Target Ai', the Parity Ai envisions the board as checkerboard.
        This is because the smallest ship that exists in the battleships game takes up two 
        squares, therefore instead of 100 possible locations to choose, there is only 
        50 random locations the Ai can choose from.

    Args:
        ship_detection (bool, bool, tuple(int, int), list[tuple]): A packed array that contains:
            ship_detected (bool): Determines whether the Ai is tracking one of the player's ships
            shiphit (bool): Determines whether the Ai has hit one of the player's ships
            lastco_ords (tuple(int, int)): The last co_ord that the Ai has shot
            stackco_ords (list[tuple]): A stack of coordinates that the Ai is going to shoot next
        ai_hitlog (list[tuple(int, int)]): A log of all the coordinates that the Ai has hit 
            on the player's board
        board_size (list[list]): The player's board that contains the player's ships

    Returns:
        tuple(int, int): The coordinate for the Ai's next attack 
    """

    ship_detected, hit_register, lastco_ord, stackco_ords = ship_detection
    if ship_detected:
        # Checks to see if the Ai has detected a ship

        x, y = lastco_ord
        x, y = int(x), int(y)
        # Gets the x and y from the last coordinate

        if hit_register:
        # Checks if the Ai had hit a ship
            for xcount in range(-1, 2, 1):
            # Selects each adjacent x coordinate
                co_ord = (x + xcount, y)
                if co_ord not in stackco_ords and co_ord not in ai_hitlog:
                # Checks if the coordinate has not already been used and is unique
                    stackco_ords.append(co_ord)
                    # Adds the coordinate to the stack

            for ycount in range(-1, 2, 1):
            # Selects each adjacent y coordinate
                co_ord = (x, y + ycount)
                # Repeats the function again
                if co_ord not in stackco_ords and co_ord not in ai_hitlog:
                    stackco_ords.append(co_ord)

        if len(stackco_ords) > 0:
        # Checks if the stack is not empty
            shotco_ord = stackco_ords[-1]
            # Gets the last item in the stack and sets it as the new coordinate
            del stackco_ords[-1]
            # Removes the last item in the stack
            return shotco_ord, stackco_ords

    valid_shot = False
    while valid_shot is False:
        # Repeats until it has found a suitable coordinate to shoot

        x = random.randrange(0, board_size)
        y = random.randrange(0, board_size)
        # Generates a random coordinate

        if x + (y * 10) > 9:
            # Determines whether the Ai is shooting a 'black square'
            if (x + (y * 10)) % 2 == 1 and y % 2 == 0:
                return (x, y), stackco_ords
            if (x + (y * 10)) % 2 == 0 and y % 2 == 1:
                return(x, y), stackco_ords
        if x % 2 == 1:
            return (x, y), stackco_ords
