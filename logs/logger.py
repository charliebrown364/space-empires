class Logger():
    def __init__(self, filename='log.txt'):
        self.filename = filename

    def clear_log(self):
        with open(self.filename, 'w') as file:
            file.writelines([''])

    def write(self, string=None):
        with open(self.filename, 'a') as file:
            file.writelines([string])

logger = Logger('/home/runner/space-empires/logs/silly-log.txt')
logger.write('stuff')

"""

END OF TURN 1 COMBAT PHASE

BEGINNING OF TURN 2 MOVEMENT PHASE

	Player 1 Scout 1: (4, 2) -> (4, 3)
	Player 1 Scout 2: (4, 2) -> (4, 3)
	Player 1 Scout 3: (4, 2) -> (4, 3)
	Player 2 Scout 1: (4, 6) -> (4, 5)
	Player 2 Scout 2: (4, 6) -> (4, 5)
	Player 2 Scout 3: (4, 6) -> (4, 5)

END OF TURN 2 MOVEMENT PHASE

BEGINNING OF TURN 2 COMBAT PHASE

END OF TURN 2 COMBAT PHASE

BEGINNING OF TURN 3 MOVEMENT PHASE

	Player 1 Scout 1: (4, 3) -> (4, 4)
	Player 1 Scout 2: (4, 3) -> (4, 4)
	Player 1 Scout 3: (4, 3) -> (4, 4)
	Player 2 Scout 1: (4, 5) -> (4, 4)
	Player 2 Scout 2: (4, 5) -> (4, 4)
	Player 2 Scout 3: (4, 5) -> (4, 4)

END OF TURN 3 MOVEMENT PHASE

BEGINNING OF TURN 3 COMBAT PHASE

	Combat at (4, 4)

		Player 2 Scout 1 was destroyed
		Player 1 Scout 3 was destroyed
		Player 1 Scout 1 was destroyed
		Player 2 Scout 3 was destroyed
		Player 1 Scout 2 was destroyed

END OF TURN 3 COMBAT PHASE

BEGINNING OF TURN 4 MOVEMENT PHASE

	Player 2 Scout 2: (4, 4) -> (4, 3)

END OF TURN 4 MOVEMENT PHASE

BEGINNING OF TURN 4 COMBAT PHASE

END OF TURN 4 COMBAT PHASE

BEGINNING OF TURN 5 MOVEMENT PHASE

	Player 2 Scout 2: (4, 3) -> (4, 2)

END OF TURN 5 MOVEMENT PHASE

BEGINNING OF TURN 5 COMBAT PHASE

END OF TURN 5 COMBAT PHASE

BEGINNING OF TURN 6 MOVEMENT PHASE

	Player 2 Scout 2: (4, 2) -> (4, 1)

END OF TURN 6 MOVEMENT PHASE

BEGINNING OF TURN 6 COMBAT PHASE

END OF TURN 6 COMBAT PHASE

WINNER: PLAYER 2

"""