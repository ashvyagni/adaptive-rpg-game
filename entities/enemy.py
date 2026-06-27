class Enemy:
    def __init__(self, name, maxhealth, attack, defense, mana):
        self.name = name
        self.maxhealth = maxhealth
        self.health = maxhealth
        self.attack = attack
        self.defense = defense
        self.mana = mana

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} takes {damage} damage and has {self.health} health left.")
            
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxhealth:
            self.health = self.maxhealth
        print(f"{self.name} heals for {amount} and has {self.health} health now.")

    def basic_attack(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")
        target.take_damage(self.attack)
        
    def is_alive(self):
        return self.health > 0
    