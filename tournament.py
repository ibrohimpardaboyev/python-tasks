from abc import ABC, abstractmethod
from itertools import combinations
import random
import json

class TournamentStrategy(ABC):
    @abstractmethod
    def schedule_matches(self, players):
        pass
    
    @abstractmethod
    def determine_winner(self, matches):
        pass

class RoundRobinStrategy(TournamentStrategy):
    def schedule_matches(self, players):
        self.matches = list(combinations(players, 2))
        return self.matches
    
    def determine_winner(self, match_results):
        standings = {}
        
        for result in match_results:
            p1, score_str, p2 = result.split()
            p1_score, p2_score = map(int, score_str.split(':'))
            
            standings[p1] = standings.get(p1, 0) + (1 if p1_score > p2_score else 0)
            standings[p2] = standings.get(p2, 0) + (1 if p2_score > p1_score else 0)
        
        return max(standings, key=standings.get)

class KnockoutStrategy(TournamentStrategy):
    def schedule_matches(self, players):
        random.shuffle(players)
        self.matches = [tuple(players[i:i+2]) for i in range(0, len(players), 2)]
        return self.matches
    
    def determine_winner(self, match_results):
        current_players = []
        
        for result in match_results:
            p1, score_str, p2 = result.split()
            p1_score, p2_score = map(int, score_str.split(':'))
            current_players.append(p1 if p1_score > p2_score else p2)
        
        while len(current_players) > 1:
            next_round = []
            for i in range(0, len(current_players), 2):
                if i+1 < len(current_players):
                    winner = current_players[i] if random.random() > 0.5 else current_players[i+1]
                    next_round.append(winner)
                else:
                    next_round.append(current_players[i])
            current_players = next_round
        
        return current_players[0]

class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.total_score = 0

class Tournament:
    def __init__(self, players):
        self.players = players
        self.matches = []
        self.results = []
        
        print("Select Tournament Format:1 Robin 2 Knockout")
        choice = input("Enter choice (1/2): ")
        
        self.strategy = RoundRobinStrategy() if choice == "1" else KnockoutStrategy()
        self.matches = self.strategy.schedule_matches([p.name for p in self.players])
    
    def play_matches(self):
        for match in self.matches:
            result = input(f"Enter result for {match[0]} vs {match[1]} (format: score1:score2): ")
            p1_score, p2_score = map(int, result.split(":"))
            
            self.results.append(f"{match[0]} {p1_score}:{p2_score} {match[1]}")
            for player in self.players:
                if player.name == match[0]:
                    player.total_score += p1_score
                    if p1_score > p2_score:
                        player.wins += 1
                elif player.name == match[1]:
                    player.total_score += p2_score
                    if p2_score > p1_score:
                        player.wins += 1
    def save_to_json(self):
        saveable_dic = {}
        sorted_players = sorted(self.players, key=lambda x: (x.wins, x.total_score), reverse=True)
        for i, player in enumerate(sorted_players, 1):
            saveable_dic[player.name] = {"rank": i, "wins": player.wins, "score": player.total_score}
        # print(saveable_dic)
        with open("tournament_table.json","w") as file:
            json.dump(saveable_dic,file)
    def show_standings(self):
        sorted_players = sorted(self.players, key=lambda x: (x.wins, x.total_score), reverse=True)
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.name} - Wins: {player.wins}, Total Score: {player.total_score}")
    
    def declare_winner(self):
        winner = self.strategy.determine_winner(self.results)
        print(f"Winner of the tournament: {winner}")

players = []
print("Enter player names (type 'done' to finish):")
while True:
    name = input("Player name: ").strip()
    if name.lower() == 'done':
        break
    if name:
        players.append(Player(name)) 
    if len(players) < 2:
        print("Not enough players to start a tournament!")
tournament = Tournament(players)
tournament.play_matches()
tournament.show_standings()
tournament.declare_winner()
tournament.save_to_json()