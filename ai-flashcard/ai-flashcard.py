import random
import csv
import json
from datetime import datetime

class Card:
    def init(self, question, answer, difficulty=1, success_rate=0):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.success_rate = success_rate

    def update_success_rate(self, rate):
        self.success_rate = rate

class Deck:
    def init(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_hardest_cards(self):
        return sorted(self.cards, key=lambda card: card.success_rate)[:3]

    def get_top_learned_topics(self):
        return sorted(self.cards, key=lambda card: card.success_rate, reverse=True)[:3]

class User:
    def init(self, name):
        self.name = name
        self.sessions = []

    def start_session(self, deck):
        session = Session(self, deck)
        self.sessions.append(session)
        return session

class Session:
    def init(self, user, deck):
        self.user = user
        self.deck = deck
        self.log = []
        self.start_time = datetime.now()

    def log_answer(self, card, is_correct):
        self.log.append({
            'card': card.question,
            'correct': is_correct,
            'timestamp': datetime.now()
        })
        card.update_success_rate(card.success_rate + (1 if is_correct else -1))

    def run_quiz(self):
        random.shuffle(self.deck.cards)
        for card in self.deck.cards:
            print(f"Question: {card.question}")
            answer = input("Your answer: ")
            is_correct = answer.lower() == card.answer.lower()
            self.log_answer(card, is_correct)
            print(f"Answer: {card.answer}")
            print(f"Correct: {is_correct}")
            print("-" * 30)
        self.end_session()

    def end_session(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.save_results(duration)
        print(f"Session ended. Duration: {duration}")
        print("Hardest Cards: ", self.deck.get_hardest_cards())
        print("Top Learned Topics: ", self.deck.get_top_learned_topics())

    def save_results(self, duration):
        session_data = {
            'user': self.user.name,
            'deck': self.deck.name,
            'duration': str(duration),
            'log': self.log
        }

        with open(f"{self.user.name}_session_results.json", "w") as json_file:
            json.dump(session_data, json_file, indent=4)
