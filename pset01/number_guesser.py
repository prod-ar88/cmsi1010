# The code below shows a number guessing game where the user has to guess a number from 1 to 1000.

import random

def number_guesser():
    while True:
        number = random.randint(1, 1000) # The number to guess
        attempts = 0 # Count of attempts
        while True:
            guess = input("Guess a number between 1 and 1000 (type 'bye' or 'exit' to quit the game): ").strip().lower() # Allows user to quit the game. Plus the user can write bye or exit in any way they want such as full caps or mixed caps.
            if guess.lower() in ['bye', 'exit']:
                print("Goodbye! Hope to see you soon!") # Goodbye message.
                return
            if not guess.isdigit():
                print("Enter a valid number please!") # User needs to imput a valid number.
                continue
            guess = int(guess)
            if guess < 1 or guess > 1000:
                print("Please guess a number within the range of 1 to 1000.") # Makes sure the user inputs a number within the range.
                continue
            attempts += 1
            if guess < number:
                print("Too low!") # Lets the user know their guess is too low.
            elif guess > number:
                print("Too high!") # Lets the user know their guess is too high.
            else:
                print(f"Congratulations! You guessed the number! Attempts you made: {attempts}") # Congratulates the user and tells them how many attempts they made.
                break

number_guesser()