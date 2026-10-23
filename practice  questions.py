# a=10
# b=20
# print(a+b)
# print(a-b)
# print(a*b)
# print(a/b)

# a = 15
# b = 6
# print(a / b)
# print(a // b)
# print(a % b)

# a = 12
# b = 5

# a = a + b
# b = a - b
# a = a - b

# a = a * 2
# b = b + 10

# print(a)
# print(b)


# print(2 + 3 * 4)
# print((2 + 3) * 4)

# swap 2 numbers using third variable
# a = 25
# b = 40
# c=a
# a=b
# b=c
# print(a)
# print(b)

# swapping 2 numbers without third variable
# a=10
# b=20
# a=a+b
# b=a-b
# a=a-b
# b=a-b
# print(a)
# print(b)

# for i in range(1, 6):
#     for j in range(1, i + 1):
#         print(j, end="")
#     print()

# for i in range(1, 6):
#     for j in range(1, i+1):
#         print("* ", end="")
#     print()


# for i in range(6, 0, -1):
#     for j in range(1, i+1):
#         print("* ", end="")
#     print()

# for i in range(1,6):
#     for j in range(6-i):
#         print(" ",end="")
#     for k in range(1,i+1):
#             print("* ",end="")
#     print()

# for i in range(5, 0, -1):
#     for j in range(i):
#         print("*", end="")
#     print()


import random

movies = ["avesham", "thattathin marayathu", "anandham", "premam", "drishyam"]
word = random.choice(movies)

display = ""
for letter in word:
    if letter == " ":
        display = display + " "
    else:
        display = display + "-"

count = 5

while count > 0 and "-" in display:
    print(display)
    guess = input("Choose a letter: ").lower()

    if guess in word:
        print("Correct choice!")
        new = ""

        for i in range(len(word)):
            if word[i] == guess:
                new = new + guess
            else:
                new = new + display[i]

        display = new

    else:
        count = count - 1
        print("Wrong choice, you have", count, "options left")

if "-" not in display:
    print("You win!")
    print("Movie:", word)
else:
    print("You lose!")
    print("Movie was:", word)