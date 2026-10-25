
import random

n = random.randint(1, 100)
a = -1
guesses = 0

while a != n:
    a = int(input("Guess the number: "))
    guesses += 1

    if a < n:
        print("Higher number please!")
    elif a > n:
        print("Lower number please!")

print(f"You guessed the number {n} correctly in {guesses} attempts.")
