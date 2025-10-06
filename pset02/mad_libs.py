import random
import re
import string
import sys

# An awesome template including awesome sentences. Plus it includes ":words" that will get replaced later on.
TEMPLATES = [
    {"text": "The :color :action :animal over the :adjective :plant.", "author": "Alexis"},
    {"text": "A crazy :noun was :verb the tree at :time.", "author": "Alexis"},
    {"text": "Remember when :place had :animal and it was always :emotion?",
     "author": "Alexis"},
    {"text": "The best game I've ever played was :game and it was so :adjective.",
     "author": "Alexis"},
    {"text": "That :noun used to look so :adjective right?", "author": "Alexis"},
    {"text": "The :profession wanted me to use :item while I was :verb.",
     "author": "Alexis"},
    {"text": "When it's :time_of_day, the sky looked so :adjective.",
     "author": "Alexis"},
    {"text": "During the :season, I would only eat :food and only eat :number times a day.",
     "author": "Alexis"},
    {"text": "The :adjective :vehicle :verb through the street!", "author": "Alexis"},
    {"text": "Our meeting at :place starts at :time_of_day so don't be late.",
     "author": "Alexis"},
]

# Yes answers are in English (and slang English), French, Spanish, Italian,
# Portuguese, German/Dutch, and Romanian.
YES_ANSWERS = {"yes", "yeah", "ye", "yea", "yup", "y", "for sure",
               "i'm down", "sure", "okay", "ok", "oui", "si", "sí", "sim", "ja", "da"}


# Find all :words in the template
def get_words_needed(template):
    return re.findall(r":(\w+)", template)


# Allows user input for their weird
def get_user_word(word_type):
    while True:
        user_word = input(f"Enter a {word_type}: ").strip()
        if 1 <= len(user_word) <= 30:
            return user_word
        print("Please enter a word between 1 and 30 characters.")


# Actual code to set the game up
def play_mad_libs():
    while True:
        # Chooses random template from the list
        template = random.choice(TEMPLATES)
        text = template["text"]
        author = template["author"]
        # Finds placeholder words that have ":"
        words_needed = get_words_needed(text)
        user_words = {}
        # Asks user for words
        for word in words_needed:
            user_words[word] = get_user_word(word)
        # Replaces placeholder words and uses user's words
        result = text
        for word, user_input in user_words.items():
            result = result.replace(f":{word}", user_input)
        # Code below prints the completed sentence with author included.
        print("\n" + result)
        print(f"\n(Template by {author})\n")
        while True:
            # Asks if user wants to play again
            again = input("Do you want to play again? ").strip().lower()
            if again in YES_ANSWERS:
                break  # Play again
            # "No" responses include same languages from yes responses
            elif again in {"no", "n", "não", "nein", "nee", "non", "nu", }:
                print("Thanks for playing!")
                return  # Ends game
            else:
                print("Please answer with yes or no.")
                # Stops the user from inputting pesky, unnecessary words


if __name__ == "__main__":
    play_mad_libs()
