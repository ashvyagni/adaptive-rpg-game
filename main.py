from entities.player import Player
from entities.enemy import Enemy
from engine.battle import Battle
name = input("Enter your character's name: "),

player = Player(
    name = name,
    maxhealth = 100,
    attack = 10,
    defense = 5,
    mana = 50
)

enemy = Enemy(
    name = "Goblin",
    maxhealth = 50,
    attack = 8,
    defense = 3,
    mana = 30
)

battle = Battle(player, enemy)

battle.start()
