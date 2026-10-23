# random

import random


# randint
# choice

# print(random.randint(1,10))

# fruits=("apple","mango","orange","pineapple","grapes")
# print(random.choice(fruits))

# coin toss

# a=("head","tail")
# print(random.choice(a))

# rock paper scissor
# choice = ("rock", "paper", "scissor")
# player = input("Enter rock,paper,scissor:")
# computer = random.choice(choice)

# print(f"computer chose: {computer}")
# print(f"player chose: {player}")
# if computer == player:
#     print("its a tie")
# elif player == "rock":
#     if computer == "scissor":
#         print("player wins")
#     else:
#         print("Computer wins")

# elif player == "paper":
#     if computer == "rock":
#         print("player wins")
#     else:
#         print("Computer wins")

# elif player == "scissor":
#     if computer == "paper":
#         print("player wins")
#     else:
#         print("Computer wins")


# wrong choice u have 5 options left
# guess:avesham
# choose
# letter 1
# guess 2


# create snake and ladder game
# 2 player game

import random
player1 = 0
player2 = 0

snakes = {
    99: 54,
    70: 55,
    52: 42,
    25: 2
}

ladders = {
    4: 25,
    13: 46,
    33: 49,
    50: 69
}
while player1 < 100 and player2 < 100:
    input("player1 -press enter to roll:")
    dice = random.randint(1,6)
    print("player 1 rolled:,dice")
    if player1 == 0:
        if dice == 1 or dice == 6:
            player1 = 1
            print("player1 started!")
        else:
            print("player1 need 1 or 6 to start")




