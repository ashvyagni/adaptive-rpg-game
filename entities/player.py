class Player:
    def __init__(self, name, maxhealth, attack, defense, mana):
        self.name = name
        self.maxhealth = maxhealth
        self.health = maxhealth
        self.attack = attack
        self.defense = defense
        self.mana = mana

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxhealth:
            self.health = self.maxhealth

    def is_alive(self):
        return self.health > 0