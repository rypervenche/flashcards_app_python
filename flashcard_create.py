import sqlite3

connection = sqlite3.connect("/home/yaboiwierdal/Flashcards Python Project/pythonFlashcards.db")

cursor = connection.cursor()

def take_input():
    create_study_edit_exit = input("Would you like to create a new deck, study a current deck, edit a deck, or save and exit the program? (c/s/e/x)\n")
    return create_study_edit_exit

def create_flashcards(create_study_edit_exit):
    if create_study_edit_exit.lower() == "c":
        name_new_deck = input("What do you want to name your new deck?\n")
        check_same_name = cursor.execute(f"SELECT Deck FROM flashcards WHERE Deck='{name_new_deck}'").fetchone()
        if check_same_name is not None:
            name_taken_alert = input("That deck name is taken. Would you like to try another name? (y/n)\n")
            if name_taken_alert == "y":
                create_flashcards(create_study_edit_exit)
            else:
                print("See you next time :)")
        else:
            add_another_card = True 
            while add_another_card == True:
                card_front = input("What do you want on the front of your card?\n")
                card_back = input("What do you want on the back of your card?\n")
                sql_command = f"""INSERT INTO flashcards VALUES ("{name_new_deck}", "{card_front}", "{card_back}");"""
                cursor.execute(sql_command)
                continue_adding = input("Would you like to add another card to the deck? (y/n)")
                if continue_adding == "n":
                    add_another_card = False
            create_flashcards(take_input())


    elif create_study_edit_exit.lower() == "s":
        counter = 1
        cursor.execute("SELECT DISTINCT Deck FROM flashcards;")
        fetched_data = cursor.fetchall()
        for item in fetched_data:
            print(f"{counter}. {item[0]}")
            counter += 1
        deck_to_study = int(input("Which deck would you like to study?\n"))
        print(fetched_data[deck_to_study - 1][0])
        cursor.execute(f"SELECT Front, Back FROM flashcards WHERE Deck='{fetched_data[deck_to_study - 1][0]}'")
        fetched_data = cursor.fetchall()
        want_to_study = True
        while want_to_study == True:
            for item in fetched_data:
                print("\n" + item[0])
                guess = input("Input your guess.\n")
                print("\n" + item[1])
                if guess.lower() == item[1].lower():
                    print("Correct! Good job!\n")
                else:
                    print("You fucking suck at this.\n")
            keep_studying = input("You have finished studying this deck, would you like to study it again? (y/n)\n")
            if keep_studying.lower() == "n":
                want_to_study = False
                print(want_to_study)
        create_flashcards(take_input())


    elif create_study_edit_exit.lower() == "e":
        counter = 1
        cursor.execute("SELECT DISTINCT Deck FROM flashcards;")
        fetched_data = cursor.fetchall()
        for item in fetched_data:
            print(f"{counter}. {item[0]}")
            counter += 1
        deck_to_edit = int(input("Which deck would you like to edit?\n"))
        deck_to_edit = fetched_data[deck_to_edit - 1][0]
        print(deck_to_edit)
        cursor.execute(f"SELECT Front, Back FROM flashcards WHERE Deck='{deck_to_edit}'")
        fetched_data = cursor.fetchall()
        counter = 1
        for item in fetched_data:
            print(f"Card #{counter}: \n Front: {item[0]}\n Back: {item[1]}")
            counter += 1
        print("\n")
        want_to_edit = True
        while want_to_edit == True:
            how_edit = input("Would you like to add cards, delete cards, change cards, delete the whole deck, or exit? (a/d/c/w/e)\n")
            if how_edit == "a":
                card_front = input("What do you want on the front of your card?\n")
                card_back = input("What do you want on the back of your card?\n")
                sql_command = f"""INSERT INTO flashcards VALUES ("{deck_to_edit}", "{card_front}", "{card_back}");"""
                cursor.execute(sql_command)
                print("Card changed")

            elif how_edit == "d":
                card_to_delete = int(input("What number card would you like to delete?\n"))
                sql_command = f"""DELETE FROM flashcards WHERE Front="{fetched_data[card_to_delete - 1][0]}" AND Back="{fetched_data[card_to_delete - 1][1]}";"""
                cursor.execute(sql_command)
                print(fetched_data[card_to_delete - 1][0])
                print(fetched_data[card_to_delete - 1][1])

            elif how_edit == "c":
                card_to_edit = int(input("What number card would you like to edit"))
                card_front = input("What do you want on the front of the card?\n")
                card_back = input("What doo you want on the back of the card?\n")
                sql_command = f"""UPDATE flashcards SET Front="{card_front}", Back="{card_back}" WHERE Front="{fetched_data[card_to_edit - 1][0]}" AND Back="{fetched_data[card_to_edit - 1][0]}";"""
                print("Card updated successfully.")
            
            elif how_edit == "w":
                delete_certainty = input("Are you sure you want to delete this deck? (y/n)\n")
                if delete_certainty == "y":
                    sql_command = f"""DELETE FROM flashcards WHERE Deck="{deck_to_edit}";"""
                    cursor.execute(sql_command)
                else:
                    return False

            elif how_edit == "e":
                return False

            want_to_edit = input("Would you like to continue editing? (y/n)\n")
            if want_to_edit == "n":
                want_to_edit = False
        create_flashcards(take_input)


    elif create_study_edit_exit.lower() == "x":
        return None

create_flashcards(take_input())

connection.commit()

connection.close()
