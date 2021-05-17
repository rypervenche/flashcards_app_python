import sqlite3
import random

connection = sqlite3.connect("/home/yaboiwierdal/Flashcards Python Project/pythonFlashcards.db")

cursor = connection.cursor()



class Card:
    def __init__(self, card_id, deck_id, front, back):
        self.id = id
        self.deck_id = deck_id
        self.front = front
        self.back = back



def create_db():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            mandarin TEXT NOT NULL UNIQUE,
            english TEXT NOT NULL,
            FOREIGN KEY(deck_id) REFERENCES decks(id)
        )"""
    )   
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )"""
    )
    connection.commit()


def get_deck_id(deck_name):
    cursor.execute(
        f"INSERT OR IGNORE INTO decks (name) VALUES ({deck_name})"
    )


def update_db(deck_id, front, back):
    cursor.execute(
        f"INSERT INTO cards (deck_id, front, back) VALUES ('{deck_id}', '{front}', '{back}')"
    )
    connection.commit()


def get_cards(deck_id):
    cards = dict()
    for row in cursor.execute(f"""SELECT notes.id, decks.name, mandarin, english FROM notes INNER JOIN decks ON notes.deck_id = decks.id WHERE deck_id = {deck_id}""")
        card = Card(row[0], row[1], row[2], row[3])
        cards[row[2]] = card
    return cards


def main():
    create_db()

    update_db(1, "Доброе утро", "Good morning")
    update_db(1, "Добрый день", "Good afternoon")
    update_db(1, "Добрый вечер", "Good evening")

    cards = get_cards(1)

    for card in cards:
        print(f"#{card}")


main()

connection.commit()

connection.close()
