xo_matrix = list("_________")
game_status = "X"
coordinates = ""
coordinates_index = 0
winner = ""


def print_screen():
    print("---------")
    print("|", xo_matrix[0], xo_matrix[1], xo_matrix[2], "|")
    print("|", xo_matrix[3], xo_matrix[4], xo_matrix[5], "|")
    print("|", xo_matrix[6], xo_matrix[7], xo_matrix[8], "|")
    print("---------")


def take_and_check_input():
    global coordinates
    global coordinates_index

    input_is_valid = False
    while not input_is_valid:
        coordinates = input("Enter the coordinates: ")
        coordinates_list = coordinates.split()
        if len(coordinates_list) != 2:
            print("Invalid input! Try again.")
        elif not coordinates_list[0].isnumeric() or not coordinates_list[1].isnumeric():
            print("You should enter numbers!")
        else:
            coordinate1 = int(coordinates_list[0])
            coordinate2 = int(coordinates_list[1])
            if coordinate1 < 1 or coordinate1 > 3 or coordinate2 < 1 or coordinate2 > 3:
                print("Coordinates should be from 1 to 3!")
            else:
                coordinates_index = ((coordinate1 - 1) * 3) + (coordinate2 - 1)
                if xo_matrix[coordinates_index] != "_":
                    print("This cell is occupied! Choose another one!")
                else:
                    input_is_valid = True


def execute_move():
    global xo_matrix
    global game_status

    if game_status == "X":
        xo_matrix[coordinates_index] = "X"
        game_status = "O"
    elif game_status == "O":
        xo_matrix[coordinates_index] = "O"
        game_status = "X"


def check_game_status():
    global game_status
    global winner

    indexes_of_threes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    spaces_left = 0
    for i in xo_matrix:
        if i == "_":
            spaces_left += 1
    three_x = False
    three_o = False
    for i in indexes_of_threes:
        number_of_x = 0
        number_of_o = 0
        for j in i:
            if xo_matrix[j] == "X":
                number_of_x += 1
            elif xo_matrix[j] == "O":
                number_of_o += 1
        if number_of_x == 3:
            three_x = True
        if number_of_o == 3:
            three_o = True
    if three_x and three_o:
        print_screen()
        print("Impossible")
        game_status = "over"
    elif three_x:
        print_screen()
        print("X wins")
        game_status = "over"
    elif three_o:
        print_screen()
        print("O wins")
        game_status = "over"
    elif spaces_left == 0:
        print_screen()
        print("Draw")
        game_status = "over"


# Main Game Logic
while game_status != "over":
    print_screen()
    take_and_check_input()
    execute_move()
    check_game_status()

