import random
import math

# Declaring global variables for the game
stock_pieces = []
computer_pieces = []
player_pieces = []
domino_snake = []
game_status = ""
player_input = 0


# Defining main functions

# Generating a full set of dominoes
def generate_domino_set():
    all_dominoes = []
    for i in range(7):
        for j in range(i, 7):
            all_dominoes.append([i, j])
    return all_dominoes


# Distributing the pieces and setting starting piece and player
def begin_game():
    global stock_pieces
    global computer_pieces
    global player_pieces
    global domino_snake
    global game_status

    game_status = "beginning"
    shuffle_is_valid = False
    while not shuffle_is_valid:

        starting_domino = [0, 0]
        stock_pieces = generate_domino_set()
        # Distributing pieces from stock pieces between player and computer
        for i in range(7):
            player_piece = stock_pieces.pop(random.randint(0, 27 - (2 * i)))
            computer_piece = stock_pieces.pop(random.randint(0, 26 - (2 * i)))

            player_pieces.append(player_piece)
            computer_pieces.append(computer_piece)

            if player_piece[0] == player_piece[1] and player_piece[0] >= starting_domino[0]:
                starting_domino = player_piece
                game_status = "computer"
            if computer_piece[0] == computer_piece[1] and computer_piece[0] >= starting_domino[0]:
                starting_domino = computer_piece
                game_status = "player"

        if game_status == "computer":
            domino_snake.append(starting_domino)
            player_pieces.remove(starting_domino)
            shuffle_is_valid = True
        elif game_status == "player":
            domino_snake.append(starting_domino)
            computer_pieces.remove(starting_domino)
            shuffle_is_valid = True


def print_screen():
    print("======================================================================")
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()
    if len(domino_snake) > 6:
        print(f"{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}{domino_snake[-1]}")
    else:
        print("".join(str(i) for i in domino_snake))
    print()
    print("Your pieces:")
    for i in range(len(player_pieces)):
        print(f"{i + 1}:{player_pieces[i]}")
    print()
    if game_status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif game_status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif game_status == "player won":
        print("Status: The game is over. You won!")
    elif game_status == "computer won":
        print("Status: The game is over. The computer won!")
    elif game_status == "draw":
        print("Status: The game is over. It's a draw!")


def take_player_input():
    global player_input

    input_is_valid = False
    if game_status == "computer":
        player_input = input()
    elif game_status == "player":
        while not input_is_valid:
            player_input = input()
            try:
                player_input = int(player_input)
            except ValueError:
                print("Invalid input. Please try again.")
            else:
                if abs(player_input) > len(player_pieces):
                    print("Invalid input. Please try again.")
                elif player_input != 0:
                    move_index = abs(player_input) - 1
                    played_first_number = player_pieces[move_index][0]
                    played_second_number = player_pieces[move_index][1]
                    snake_first_number = domino_snake[0][0]
                    snake_last_number = domino_snake[-1][-1]

                    if player_input < 0 and (played_first_number != snake_first_number and played_second_number != snake_first_number):
                        print("Illegal move. Please try again.")
                    elif player_input > 0 and (played_first_number != snake_last_number and played_second_number != snake_last_number):
                        print("Illegal move. Please try again.")
                    else:
                        input_is_valid = True

                else:
                    input_is_valid = True


def make_player_move():
    global game_status

    if player_input == 0:
        player_pieces.append(stock_pieces.pop(random.randint(0, len(stock_pieces) - 1)))
    else:
        move_index = abs(player_input) - 1
        played_first_number = player_pieces[move_index][0]
        played_second_number = player_pieces[move_index][1]
        snake_first_number = domino_snake[0][0]
        snake_last_number = domino_snake[-1][-1]
        if player_input < 0:
            if played_second_number != snake_first_number:
                domino_snake.insert(0, [played_second_number, played_first_number])
                player_pieces.pop(move_index)
            else:
                domino_snake.insert(0, player_pieces.pop(move_index))
        elif player_input > 0:
            if played_first_number != snake_last_number:
                domino_snake.append([played_second_number, played_first_number])
                player_pieces.pop(move_index)
            else:
                domino_snake.append(player_pieces.pop(move_index))

    game_status = "computer"


def make_computer_move():
    global game_status

    def count_numbers_scores():
        scores_dictionary = {}
        for i in range(7):
            count = 0

            for k in computer_pieces:
                if k[0] == i:
                    count += 1
                if k[1] == i:
                    count += 1

            for m in domino_snake:
                if m[0] == i:
                    count += 1
                if m[1] == i:
                    count += 1

            scores_dictionary[i] = count
        return scores_dictionary

    def check_if_legal_move(computer_move):

        if computer_move != 0:
            move_index = abs(computer_move) - 1
            played_first_number = computer_pieces[move_index][0]
            played_second_number = computer_pieces[move_index][1]
            snake_first_number = domino_snake[0][0]
            snake_last_number = domino_snake[-1][-1]

            if computer_move < 0 and (
                    played_first_number != snake_first_number and played_second_number != snake_first_number):
                return False
            elif computer_move > 0 and (
                    played_first_number != snake_last_number and played_second_number != snake_last_number):
                return False
            else:
                return True

        else:
            return True

    numbers_scores = count_numbers_scores()
    domino_scores = {}
    for i in range(len(computer_pieces)):
        domino_score = numbers_scores[computer_pieces[i][0]] + numbers_scores[computer_pieces[i][1]]
        domino_scores[i] = domino_score

    move_value = 0
    found_move = False
    illegal_move_indexes = []
    while not found_move:

        max_value = -math.inf
        max_index = 0

        for key, value in domino_scores.items():
            if key in illegal_move_indexes:
                continue
            elif value > max_value:
                max_value = value
                max_index = key

        if check_if_legal_move(max_index + 1):
            move_value = max_index + 1
            found_move = True
        elif check_if_legal_move(-(max_index + 1)):
            move_value = -(max_index + 1)
            found_move = True
        else:
            illegal_move_indexes.append(max_index)
            if len(illegal_move_indexes) == len(domino_scores):
                move_value = 0
                found_move = True

    if move_value == 0:
        computer_pieces.append(stock_pieces.pop(random.randint(0, len(stock_pieces) - 1)))
    else:
        move_index = abs(move_value) - 1
        played_first_number = computer_pieces[move_index][0]
        played_second_number = computer_pieces[move_index][1]
        snake_first_number = domino_snake[0][0]
        snake_last_number = domino_snake[-1][-1]
        if move_value < 0:
            if played_second_number != snake_first_number:
                domino_snake.insert(0, [played_second_number, played_first_number])
                computer_pieces.pop(move_index)
            else:
                domino_snake.insert(0, computer_pieces.pop(move_index))
        elif move_value > 0:
            if played_first_number != snake_last_number:
                domino_snake.append([played_second_number, played_first_number])
                computer_pieces.pop(move_index)
            else:
                domino_snake.append(computer_pieces.pop(move_index))

    game_status = "player"


def check_game_status():
    global game_status

    if len(player_pieces) == 0:
        game_status = "player won"
    elif len(computer_pieces) == 0:
        game_status = "computer won"
    else:
        if domino_snake[0][0] == domino_snake[-1][-1]:
            count = 0
            for i in range(len(domino_snake)):
                if domino_snake[i][0] == domino_snake[0][0]:
                    count += 1
                if domino_snake[i][1] == domino_snake[0][0]:
                    count += 1
            if count == 8:
                game_status = "draw"


# Main game loop
begin_game()
while game_status in ["player", "computer"]:
    print_screen()
    take_player_input()

    if game_status == "player":
        make_player_move()
    elif game_status == "computer":
        make_computer_move()

    check_game_status()

    if game_status in ["player won", "computer won", "draw"]:
        print_screen()

