class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
    def player_attack(self):
        damage = self.player.attack - self.enemy.defense
        if damage < 0:
            damage = 0
        print(f"{self.player.name} attacks {self.enemy.name} for {damage} damage!")
        self.enemy.take_damage(damage)
    def enemy_attack(self):
        damage = self.enemy.attack - self.player.defense
        if damage < 0:
            damage = 0
        print(f"{self.enemy.name} attacks {self.player.name} for {damage} damage!")
        self.player.take_damage(damage)
    def is_over(self):
        if not self.player.is_alive():
            print(f"{self.player.name} has been defeated! Game Over.")
            return True
        elif not self.enemy.is_alive():
            print(f"{self.enemy.name} has been defeated! You win!")
            return True
        return False
    def start(self):
        print(f"A wild {self.enemy.name} appears!")
        while not self.is_over():
            action = input("Choose an action: (1) Attack (2) Heal: ")
            if action == "1":
                self.player_attack()
            elif action == "2":
                heal_amount = 20
                self.player.heal(heal_amount)
                print(f"{self.player.name} heals for {heal_amount} and has {self.player.health} health now.")
            else:
                print("Invalid action. Please choose again.")
                continue
            if not self.is_over():
                self.enemy_attack()
                