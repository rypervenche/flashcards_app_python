import sqlite3
import random

connection = sqlite3.connect("/tmp/test.db")

cursor = connection.cursor()


class Card:
    def __init__(self, card_id, deck_id, front, back):
        self.id = id
        self.deck_id = deck_id
        self.front = front
        self.back = back


def create_db():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            front TEXT NOT NULL UNIQUE,
            back TEXT NOT NULL,
            FOREIGN KEY(deck_id) REFERENCES decks(id)
        );"""
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
        "INSERT INTO decks (name) VALUES (?)", [deck_name]
    )

    cursor.execute("SELECT id FROM decks WHERE name = (?)", [deck_name])
    return cursor.fetchone()[0]


def update_db(deck_id, front, back):
    cursor.execute(
        """INSERT INTO cards (deck_id, front, back) VALUES (?, ?, ?)""", (deck_id, front, back))
    connection.commit()


def get_cards(deck_id):
    cards = dict()
    for row in cursor.execute(f"SELECT cards.id, decks.name, front, back FROM cards INNER JOIN decks ON cards.deck_id = decks.id WHERE deck_id = (?)", [deck_id]):
        card = f"{row[0]}, {row[1]}, {row[2]}, {row[3]}"
        cards[row[2]] = card
    return cards


def main():
    create_db()

    chosen_deck = "test"
    deck_id = get_deck_id(chosen_deck)

    update_db(deck_id, "Доброе утро", "Good morning")
    update_db(deck_id, "Добрый день", "Good afternoon")
    update_db(deck_id, "Добрый вечер", "Good evening")

    cards = get_cards(deck_id)

    for card in cards:
        print(card)
        print(cards.get(card))


main()

connection.commit()

connection.close()
