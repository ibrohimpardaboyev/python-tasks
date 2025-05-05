import random
import pickle

class Healthy:
    def can_act(self):
        return True

class Poisoned:
    def can_act(self):
        return True

class Dead:
    def can_act(self):
        return False

class Entity:
    def __init__(self, name, hp, attack_power, defense):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

class Player(Entity):
    def __init__(self, name):
        super().__init__(name, 100, 10, 5)
        self.inventory = []
        self.state = Healthy()
        self.quests = []

    def attack(self, enemy):
        if not self.state.can_act():
            log(f"{self.name} cannot attack (state: {self.state.__class__.__name__})")
            return
        damage = max(self.attack_power - enemy.defense, 1)
        enemy.hp -= damage
        log(f"{self.name} attacks {enemy.name} for {damage} damage")

    def defend(self):
        if not self.state.can_act():
            log(f"{self.name} cannot defend (state: {self.state.__class__.__name__})")
            return
        self.defense += 2
        log(f"{self.name} is defending (Defense now {self.defense})")

    def use_item(self, item):
        if item in self.inventory:
            item.use(self)
            self.inventory.remove(item)
            log(f"{self.name} uses {item.name}")

class Enemy(Entity):
    def decide_action(self, player):
        if self.hp < 20:
            log(f"{self.name} retreats!")
        else:
            self.attack(player)

    def attack(self, player):
        damage = max(self.attack_power - player.defense, 1)
        player.hp -= damage
        log(f"{self.name} attacks {player.name} for {damage} damage")

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, player):
        self.effect(player)

class Quest:
    def __init__(self, type_):
        self.type = type_
        self.completed = False

    @staticmethod
    def generate():
        types = ["Find Item", "Kill Monster", "Explore Zone"]
        return Quest(random.choice(types))

class World:
    def __init__(self):
        self.zones = ["Forest", "Cave", "Village"]

    def explore(self):
        zone = random.choice(self.zones)
        log(f"Explored {zone}")
        return zone


def log(message):
    with open("log.txt", "a") as f:
        f.write(message + "\n")
    print(message)

def save_game(player, filename="save.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(player, f)

def load_game(filename="save.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)
