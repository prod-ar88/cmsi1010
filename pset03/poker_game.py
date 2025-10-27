# Import necessary functions from cards.py
from cards import deal, poker_classification


def main():
    # Words to quit
    QUIT = {"bye", "exit"}

    while True:
        user = input("Enter the number of players (2-10): ").strip().lower()
        if user in QUIT:
            print("Goodbye!")
            break

        # Converts input to integer and displays error if invalid
        try:
            num_players = int(user)
        except ValueError:
            print("Please enter a number between 2 and 10, or 'bye' to quit.")
            continue

        # Checks range of players
        if num_players < 2 or num_players > 10:
            print("Number of players must be between 2 and 10.")
            continue

        # Deal hands with 5 cards each for player and handle possible errors
        try:
            hands = deal(num_players, 5)
        except Exception as e:
            print("Error dealing cards:", e)
            continue

        # Print each hand and its poker classification
        for hand in hands:
            cards_str = " ".join(str(card) for card in hand)
            classification = poker_classification(hand)
            print(f"{cards_str} is a {classification}")

        print()  # Blank line before next prompt for readability


if __name__ == "__main__":
    main()
