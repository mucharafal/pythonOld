from random import randint
import sys

def read_file(file_name):
    """Return list of words from file. Format of file- one word in line without whitespaces (except of new line sign)."""
    words = []
    with open(file_name, 'r') as file:
        read_word = file.readline()
        while read_word != '':
            if read_word.isalpha():
                words.append(read_word)
            read_word = file.readline()
    return words

def list_of_words(file_name = None):
    """Return list of words. If file_name is not specified return default list."""
    words = []
    if file_name:
        words = read_file(file_name)
    else:
        words = ["Ala", "ma", "kota"]
    return words

def show_word(word, guessed_letters):
    """Print only this letters of word, which are in guessed_letters list. If letter is not in guessed_letters is replaced by '_'."""
    word_to_print = ""
    for letter in word:
        word_to_print = word_to_print + (letter if letter in guessed_letters else "_")
    print(word_to_print)

def get_letter():
    """Return letter inserted by user."""
    correct_letter = False
    while not correct_letter:
        letter = input("Your letter: ")
        correct_letter = letter.isalpha() and len(letter) == 1
        if not correct_letter:
            print("It's not letter")
    return letter

def guessed(word, tried_letters):
    """Return true if all letters from word are in tried_letters"""
    is_guessed = True
    for letter in word:
        if letter not in tried_letters:
            is_guessed = False
    return is_guessed

def game(file_name = None):
    list_of_words_var = list_of_words(file_name)
    if len(list_of_words_var) == 0:
        print("None correct words in file")
        return
    else: 
        word = list_of_words_var[randint(0, len(list_of_words_var) - 1)].lower()    #choosing word

    incorrect_tries = 0
    tried_letters = []
    while incorrect_tries < 3 and not guessed(word, tried_letters):
        show_word(word, tried_letters)
        letter = get_letter().lower()
        while letter in tried_letters:
            letter = get_letter()
        
        if letter not in word:
            incorrect_tries = incorrect_tries + 1
        
        tried_letters.append(letter)

    if guessed(word, tried_letters):
        show_word(word, tried_letters)
        print("Congratulations, you win")
    else:
        print("Sorry, you lose.")

    if_again = input("Would you like to try again? N/Y ")
    if if_again in ['Y', 'y', "yes", "Yes"]:
        game()
        
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Incorrect arguments")
    elif len(sys.argv) < 2:
        game()
    else:
        game(sys.argv[1])