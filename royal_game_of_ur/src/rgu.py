import numpy as np


class RGU(object):

    def __init__(self):

        self.player = 0
        self.num_dice = 4
        self.num_stones = 4

        # 2 race tracks, indices 5 through 12 overlap
        self.track_length = 16
        self.track = [[], []]
        self.track[0] = np.zeros(self.track_length, dtype=np.int8)
        self.track[1] = np.zeros(self.track_length, dtype=np.int8)
        self.track = np.array(self.track)
        self.vulnerable_idx = [5, 6, 7, 9, 10, 11, 12]
        self.reroll_idx = [4, 8, 14]

        # 2d array for drawing the board
        self.board = np.zeros((3, 8), dtype=np.int8)

        # self.board_values = np.array(list(range(24)))
        # self.board_values = np.reshape(self.board_values, (3,8))
        self.board_values = np.asarray(
            [
                [
                    [0.9, 0.6, 0.4, 0.8, 0.1, 1.0, 0.7, 0.8],
                    [0.2, 0.7, 0.0, 1.0, 1.0, 0.6, 0.2, 0.7],
                    [0.2, 0.5, 0.9, 0.9, 0.0, 0.3, 0.4, 0.5],
                ],
                [
                    [0.9, 0.6, 0.5, 0.8, 0.2, 0.9, 0.7, 0.8],
                    [0.2, 0.7, 0.0, 1.0, 1.0, 0.6, 0.2, 0.7],
                    [0.2, 0.3, 0.8, 0.8, 0.0, 0.2, 0.4, 0.4],
                ],
            ]
        )

        self.translate = np.zeros((3, 8), dtype=np.int8)
        self.translate[0] = [4, 3, 2, 1, 0, 15, 14, 13]
        self.translate[1] = [i for i in range(5, 13)]
        self.translate[2] = [4, 3, 2, 1, 0, 15, 14, 13]

    def print(self):
        # Print the current status of the board to the screen.
        print(self.board)

    def roll_dice(self):
        # The 4 dice have a 50-50 chance to return either 1 or 0.
        # The total is the result, between 0 and 4.
        # note: 0 is possible
        return sum(np.random.randint(2, size=self.num_dice))

    def new_game(self):
        # creates a new game and clears the board.

        for i, _ in enumerate(self.track):
            self.track[i] = np.zeros(self.track_length, dtype=np.int8)
            self.track[i][0] = self.num_stones

        self.track_to_board()

    def get_possible_moves(self, r):
        # Returns a list of indices of stones that are able to move
        # the number of squares specified.
        # Params: r: number of spaces to move.

        # get all squares with stones on them
        possible = np.nonzero(self.track[self.player])[0]

        # remove the squares that will overshoot
        possible = possible[possible < self.track_length - r]
        resulting = [i + r for i in possible]
        overlapping = [i - r for i in possible if i in resulting]

        possible = [i for i in possible if i not in overlapping]

        # filter immune center square
        if self.track[(self.player + 1) % 2][8] > 0 and 8 - r in possible:
            possible.remove(8 - r)

        return possible

    def track_to_board(self):
        # Fills self.board with the current state of both tracks.

        # Top row:
        for i, v in enumerate(self.translate[0]):
            self.board[0][i] = self.track[0][v]

        # Middle row
        for i, v in enumerate(self.translate[1]):
            self.board[1][i] = self.track[0][v] - self.track[1][v]

        # Bottom row
        for i, v in enumerate(self.translate[2]):
            self.board[2][i] = -self.track[1][v]

    def change_player(self):
        # rotates the value of self.player between 0 and 1
        self.player = (self.player + 1) % 2

    def do_move(self, s, r):
        # Moves a stone on the track and updates the board.
        # Returns the index of the new location of the moved stone, so a check
        # can be made for a reroll on 1 of the 5 reroll squares.
        # Params: s: index of the stone to move
        #         r: number of squares to move.
        self.track[self.player][s] -= 1
        self.track[self.player][s + r] += 1

        # remove opponent's stone
        if (
            s + r in self.vulnerable_idx
            and self.track[(self.player + 1) % 2][s + r] != 0
        ):
            self.track[(self.player + 1) % 2][s + r] = 0
            self.track[(self.player + 1) % 2][0] += 1

        self.track_to_board()

        return s + r

    def check_winner(self):
        # return the index of the winner, False otherwise
        for idx, track in enumerate(self.track):
            if track[-1] == self.num_stones:
                return idx
        return -1

    def get_move(self, roll):
        # Allows the user to select a stone to move
        # Returns the index of the stone to move.
        # Returns -3 if there are no possible moves
        # Manually abort by entering -2
        # Params: roll: the number of squares the stone is to move.
        possible_moves = self.get_possible_moves(roll)
        if possible_moves == []:
            print("There are no moves possible, switching player.")
            return -3
        chosen = False
        while not chosen:
            stone = int(input("Select a stone to move: {} :".format(possible_moves)))
            if stone in possible_moves:
                return stone
            elif stone == -2:
                return stone
            else:
                print("Invalid choice, must be in {}.".format(possible_moves))
        # TODO: type checking of input
        return stone

    def get_roll(self):
        print("\nPlayer {}.".format(self.player))
        input("Press <enter> to roll the dice.")
        roll = self.roll_dice()
        print("You have rolled {}.".format(roll))
        return roll

    def play_turn(self, roll):
        stone = self.get_move(roll)
        moved = self.do_move(stone, roll)
        if moved not in self.reroll_idx:
            self.change_player()

    def play(self):
        won = False
        while not won:
            self.print()
            roll = self.get_roll()
            if roll == 0:
                print("You rolled 0, no move possible, switching player.")
                self.change_player()
                continue

            stone = self.get_move(roll)
            moved = self.do_move(stone, roll)

            if self.check_winner() == self.player:
                won = True

            if moved not in self.reroll_idx:
                self.change_player()
            else:
                print("You landed on a reroll square and get another turn.")

    def play_automated(self):
        won = False
        while not won:
            # self.print()
            roll = self.roll_dice()
            if roll == 0:
                # print("You rolled 0, no move possible, switching player.")
                self.change_player()
                continue

            stone = self.get_best_move(roll)[0]
            if stone < 0:
                self.change_player()
                continue
            moved = self.do_move(stone, roll)
            winner = self.check_winner()

            if winner == self.player:
                won = True

            if moved not in self.reroll_idx:
                self.change_player()

        # self.print()
        return winner

    def evaluate_move(self, stone, roll):
        # copy state
        # track
        # board
        temp_track = self.track.copy()

        # do move
        self.do_move(stone, roll)

        # evaluate
        rating = self.rate_board()
        # return state

        self.track = temp_track
        self.track_to_board()

        return rating

    def evaluate_possible_moves(self, roll):
        evaluate = []
        possible = self.get_possible_moves(roll)
        for i in possible:
            evaluate.append((i, self.evaluate_move(i, roll)))

        return evaluate

    def get_best_move(self, roll):
        # TODO: zelfde waarde keuze oplossen
        # min bij player 1

        p = self.evaluate_possible_moves(roll)
        if self.player == 0:
            return max(p, key=lambda i: i[1], default=(-1, -1))
        else:
            return min(p, key=lambda i: i[1], default=(-1, -1))

    def rate_board(self):
        if self.player == 0:
            order = [0, 1, 2]
        else:
            order = [2, 1, 0]
        rating = 0
        for a, b in zip(self.board_values[self.player][order], self.board):
            for v, b in zip(a, b):
                rating += v * b
        return rating


if __name__ == "__main__":
    game = RGU()
    game.new_game()
    game.play()
