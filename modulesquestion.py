# number guessing name
# computer generates a random number
# player gets 5-7 attempts
# give hints: too high/too low
# track score
# print("The number was:", computer)

# import random
# computer = random.randint(1, 10)
# score = 0
# for i in range(5):
#     user = int(input("Guess the num (1-10): "))
#     if computer == user:
#         print("win")
#         score = 5-i
#         break
#     elif user > computer:
#         print("Too high")
#     else:
#         print("Too low")
# else:
#     print("lost")
# print("score:", score)


# racing game
# player and computer race
# each round normally moves the players forward
# first to reach 50 points wins
# add speed/boost  options

import random
player = 0
computer = 0
while player < 50 and computer < 50:
    choice = input("Normal or Boost? ")
    if choice == "Boost":
        player += random.randint(5, 10)
    else:
        player += random.randint(1, 5)

    computer += random.randint(1, 5)
    print("Player:", player)
    print("Computer:", computer)
if player >= 50:
    print("Player wins!")
else:
    print("Computer wins!")


# coin toss betting game
# guess heads/tails
# bet points on each round
# correct guess increases points
# wrong guesses loses points


# import random
# point = 100
# while point > 0:
#     a = input("choose head or tail:")
#     b = int(input("enter bet:"))
#     coin = ["head", "tail"]
#     result = random.choice(coin)
#     print("coin:", result)
#     if a == result:
#         point = point+b
#         print("win")
#     else:
#         point = point-b
#         print("lost")
#     print("point:", point)
