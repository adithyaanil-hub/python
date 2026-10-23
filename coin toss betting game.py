# coin toss betting game
# guess heads/tails
# bet points on each round
# correct guess increases points
# wrong guesses loses points

import random
point = 100
while point > 0:
    a = input("choose head or tail:")
    b = int(input("enter bet:"))
    coin = ["head", "tail"]
    result = random.choice(coin)
    print("coin:", result)
    if a == result:
        point = point+b
        print("win")
    else:
        point = point-b
        print("lost")
    print("point:", point)
