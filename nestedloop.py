# nested
# pattern printing

# for i in range(1, 6):
#     for j in range(1, i+1):
#         print("*", end="")
#     print()

# reverse
# for i in range(6, 0, -1):
#     for j in range(1, i+1):
#         print("*", end="")
#     print()

# for i in range(1,6):
#    for j in range(6-i):
#      print(" ",end="")
#    for k in range(1,i+1):
#       print("* ",end="")
#    print()

# chessboard pattern

# for i in range(1,9):
#     for j in range(1,9):
#         if((i+j) % 2 == 0):
#           print("W ",end="")
#         else:
#           print("B ",end="")
#     print()


for i in range(1, 6):
    for j in range(6-i):
        print("A P P L E ", end="")
    for k in range(1, i+1):
        print()
