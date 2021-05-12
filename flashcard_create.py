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


    if create_study_edit_exit.lower() == "s":
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


    if create_study_edit_exit.lower() == "x":
        return None

create_flashcards(take_input())

connection.commit()

connection.close()
