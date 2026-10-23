import random

youDict = {"s": 1, "w": -1, "g": 0}
reverseDict = {1: "snake", -1: "water", 0: "gun"}

while True:
    computer = random.choice([-1, 0, 1])
    youstr = input("Enter your choice: ")
    you = youDict[youstr]

    if computer == you:
        print("It's a draw!")
    else:
        # Computer chose Water (-1)
        if computer == -1 and you == 1:
            print("You win!")  # Snake drinks Water
        elif computer == -1 and you == 0:
            print("You lose!") # Water drowns Gun

        # Computer chose Gun (0)
        elif computer == 0 and you == 1:
            print("You lose!") # Gun shoots Snake
        elif computer == 0 and you == -1:
            print("You win!")  # Water drowns Gun

        # Computer chose Snake (1)
        elif computer == 1 and you == -1:
            print("You lose!") # Snake drinks Water
        elif computer == 1 and you == 0:
            print("You win!")  # Gun shoots Snake