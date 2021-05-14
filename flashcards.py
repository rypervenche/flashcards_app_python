import sqlite3
import random

connection = sqlite3.connect("/home/yaboiwierdal/Flashcards Python Project/pythonFlashcards.db")

cursor = connection.cursor()


def mode_select():
    choice = input("Would you like to create a new deck, study a current deck, edit a deck,  or exit the program (create/study/edit/exit)? ")
    if choice.lower() == "create":
        create_flashcards()
    elif choice.lower() == "study":
        study_flashcards()
    elif choice.lower() == "edit":
        editing()
    elif choice.lower() == "exit":
        save_and_exit()


def create_flashcards():
    deck_name = input("What do you want to name your new deck? ")
    check_duplicate = cursor.execute(f"SELECT Deck FROM flashcards WHERE Deck='{deck_name}'").fetchone()
    if check_duplicate is not None:
        taken_alert = input("That deck name is taken. Would you like to try another name (y/n)? ")
        if taken_alert.lower() == "y":
            create_flashcards()
        else:
            mode_select()
    else:
        creating = True
        while creating == True:
            card_front = input("What do you want on the front of this card? ")
            card_back = input("What do you want on the back of this card? ")
            confirmation = input(f"You are adding the following card to '{deck_name}':\n Front: {card_front}\n Back: {card_back}\nAre you sure you want to make this addition (y/n)")
            if confirmation == "y":
                cursor.execute(f"""INSERT INTO flashcards VALUES ("{deck_name}", "{card_front}", "{card_back}");""")
                connection.commit()
                continue_creating = input("Your addition has been saved. Would you like to add another card (y/n)?")
            else:
                continue_creating = input("Would you like to try again (y/n)?")
            creating = False if continue_creating == "n" else True
        mode_select()


def study_flashcards():
    counter = 1
    cursor.execute("SELECT DISTINCT Deck FROM flashcards;")
    decks_tuple = cursor.fetchall()
    for distinct_deck_row in decks_tuple:
        print(f" {counter}. {distinct_deck_row[0]}")
        counter += 1
    deck_choice = int(input("Which deck would you like to study? "))
    deck_choice = decks_tuple[deck_choice - 1][0]
    cursor.execute(f"SELECT Front, Back FROM flashcards WHERE Deck='{deck_choice}'")
    flashcard_info_tuple = cursor.fetchall()
    studying = True
    while studying == True:
        random.shuffle(flashcard_info_tuple)
        for card_info_list in flashcard_info_tuple:
            print(card_info_list[0])
            guess = input("Input your guess: ")
            print("Correct!") if guess.lower() == card_info_list[1].lower() else print("Incorrect.")

            # Add try again feature

        continue_studying = input("You have finished studying this deck. Would you like to study it again (y/n)? ")
        if continue_studying == "n":
            continue_studying = input("Would you like to study another deck or exit the studying program (study/exit)? ")
            studying = False if continue_studying == "study" else mode_select()


def edit_select():
    edit_method = input("Would you like to add cards, delete cards, change cards, delete the whole deck, or exit (add/delete/change/delete deck/exit)? ")
    return edit_method


def list_decks():
    cursor.execute("SELECT DISTINCT Deck FROM flashcards;")
    decks = cursor.fetchall()
    for counter, deck_name in enumerate(decks):
        print(f" {counter + 1}. {deck_name[0]}")
    return decks


def list_cards():
    decks = list_decks()  
    deck_to_edit = int(input("Which deck would you like to edit?\n"))
    deck_choice = decks[deck_to_edit - 1][0]
    cursor.execute(f"SELECT Front, Back FROM flashcards WHERE Deck='{deck_choice}'")
    front_and_back = cursor.fetchall()
    for counter, card in enumerate(front_and_back):
        print(f"Card #{counter + 1}: \n Front: {card[0]}\n Back: {card[1]}")
    return front_and_back, deck_choice


def editing():
    print("This")
    edit_method = edit_select()
    front_and_back, deck_choice = list_cards()
    editing = True
    while editing == True:
        if edit_method.lower() == "add":
            card_front = input("What do you want on the front of this card? ")
            card_back = input("What do you want on the back of this card? ")
            confirmation = input(f"You are adding the following card to '{deck_choice}':\n Front: {card_front}\n Back: {card_back}\nAre you sure you want to make this addition (y/n)? ")
            sql_command = f"""INSERT INTO flashcards VALUES ("{deck_choice}", "{card_front}", "{card_back}");"""
            continue_confirmation = "Your addition has been saved. Would you like to add another card (y/n)? "

        elif edit_method.lower() == "delete":
            card_to_delete = int(input("What number card would you like to delete? "))
            confirmation = input(f"You are deleting the following card from '{deck_choice}':\n Front: {front_and_back[card_to_delete - 1][0]}\n Back: {front_and_back[card_to_delete - 1][1]}\nAre you sure you want to make these changes (y/n)? ")
            sql_command = f"""DELETE FROM flashcards WHERE Front="{front_and_back[card_to_delete - 1][0]}" AND Back="{front_and_back[card_to_delete - 1][1]}";"""
            continue_confirmation = "Your deletion has been saved. Would you like to delete another card (y/n)? "

        elif edit_method.lower() == "change":
            card_to_change = int(input("What number card would you like to change? "))
            card_front = input("What do you want on the front of the card?\n")
            card_back = input("What doo you want on the back of the card?\n")
            confirmation = input(f"You are requesting update this card in {deck_choice} to:\n Front: {card_front}\n Back: {card_back}\nAre you sure you want to make these changes (y/n)? ")
            sql_command = f"""UPDATE flashcards SET Front="{front_and_back[card_to_change- 1][0]}", Back="{front_and_back[card_to_change - 1][1]}" WHERE Front="{front_and_back[card_to_change- 1][0]}" AND Back="{front_and_back[card_to_change - 1][1]}";"""
            continue_confirmation = "Your change has been saved. Would you like to change another card in this deck (y/n)? "

        elif edit_method.lower() == "delete deck":
            decks = list_decks()
            deck_to_edit = int(input("Which deck would you like to delete?\n"))
            deck_choice = decks[deck_to_edit - 1][0]
            confirmation = input(f"Are you sure you want to delete '{deck_choice}' (y/n)? ")
            sql_command = f"""DELETE FROM flashcards WHERE Front="{front_and_back[card_to_delete - 1][0]}" AND Back="{front_and_back[card_to_delete - 1][1]}";"""
            continue_confirmation = "Your deletion has been saved. Would you like to delete another deck? "


        if confirmation == "y":
            cursor.execute(sql_command)
            connection.commit()
            continue_editing = input(continue_confirmation)
        else: 
            continue_editing = input("Would you like to try again (y/n)? ")
        editing = False if continue_editing == "n" else True
    mode_select()


def save_and_exit():
    return False


mode_select()

connection.commit()

connection.close()
