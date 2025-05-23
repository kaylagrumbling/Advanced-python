import random
 # Simple RPG Battle Game
# This is a simple text-based RPG battle game where the player can choose a character class and fight against an Evil Wizard.
class Character:
    def __init__(self, name, max_health, attack_range):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.attack_range = attack_range
        self.ability_cooldowns = {}

    def attack(self, target):
        damage = random.randint(*self.attack_range)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def heal(self, amount):
        if self.health == self.max_health:
            print(f"{self.name} is already at maximum health!")
            return
        self.health = min(self.max_health, self.health + amount)
        print(f"{self.name} heals for {amount} HP! (Current HP: {self.health}/{self.max_health})")

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def show_stats(self):
        print(f"{self.name} | HP: {self.health}/{self.max_health}")

# --- Character Classes ---

class Warrior(Character):
    def __init__(self):
        super().__init__("Warrior", 100, (15, 25))
        self.berserk_active = False

    def ability_1(self, target):
        # Berserk: Double damage next attack
        self.berserk_active = True
        print("Warrior uses Berserk! Next attack will deal double damage.")

    def ability_2(self, target):
        # Shield Block: Blocks next attack
        self.ability_cooldowns['shield_block'] = 1
        print("Warrior uses Shield Block! Blocks the next attack.")

    def attack(self, target):
        damage = random.randint(*self.attack_range)
        if self.berserk_active:
            damage *= 2
            print("Berserk activated! Double damage!")
            self.berserk_active = False
        print(f"Warrior attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, amount):
        if self.ability_cooldowns.get('shield_block', 0) > 0:
            print("Shield Block activated! No damage taken.")
            self.ability_cooldowns['shield_block'] = 0
        else:
            super().take_damage(amount)

class Mage(Character):
    def __init__(self):
        super().__init__("Mage", 80, (20, 30))
        self.fireball_ready = True

    def ability_1(self, target):
        # Fireball: High damage attack
        if self.fireball_ready:
            damage = random.randint(35, 50)
            print(f"Mage casts Fireball on {target.name} for {damage} damage!")
            target.take_damage(damage)
            self.fireball_ready = False
        else:
            print("Fireball is recharging!")

    def ability_2(self, target):
        # Mana Shield: Heals self
        heal_amount = 25
        print("Mage uses Mana Shield to heal!")
        self.heal(heal_amount)

    def end_turn(self):
        self.fireball_ready = True

class Archer(Character):
    def __init__(self):
        super().__init__("Archer", 90, (12, 22))
        self.evade_active = False

    def ability_1(self, target):
        # Quick Shot: Double arrow attack
        print("Archer uses Quick Shot! Two arrows fired!")
        for _ in range(2):
            damage = random.randint(8, 14)
            print(f"  Arrow hits {target.name} for {damage} damage!")
            target.take_damage(damage)

    def ability_2(self, target):
        # Evade: Evades next attack
        self.evade_active = True
        print("Archer prepares to evade the next attack!")

    def take_damage(self, amount):
        if self.evade_active:
            print("Archer evades the attack! No damage taken.")
            self.evade_active = False
        else:
            super().take_damage(amount)

class Paladin(Character):
    def __init__(self):
        super().__init__("Paladin", 110, (10, 20))
        self.shield_active = False

    def ability_1(self, target):
        # Holy Strike: Bonus damage
        damage = random.randint(25, 35)
        print(f"Paladin uses Holy Strike on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def ability_2(self, target):
        # Divine Shield: Blocks next attack
        self.shield_active = True
        print("Paladin uses Divine Shield! Blocks the next attack.")

    def take_damage(self, amount):
        if self.shield_active:
            print("Divine Shield activated! No damage taken.")
            self.shield_active = False
        else:
            super().take_damage(amount)

# --- Evil Wizard ---

class EvilWizard(Character):
    def __init__(self):
        super().__init__("Evil Wizard", 120, (18, 28))

    def regenerate(self):
        regen = random.randint(8, 18)
        self.heal(regen)
        print(f"Evil Wizard regenerates {regen} HP!")

    def evil_attack(self, target):
        # Randomly choose between normal attack or a special attack
        if random.random() < 0.3:
            # Special attack: Dark Blast
            damage = random.randint(30, 40)
            print(f"Evil Wizard uses Dark Blast for {damage} damage!")
            target.take_damage(damage)
        else:
            self.attack(target)

# --- Game Logic ---

def choose_character():
    print("Choose your character:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Paladin")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        return Warrior()
    elif choice == '2':
        return Mage()
    elif choice == '3':
        return Archer()
    elif choice == '4':
        return Paladin()
    else:
        print("Invalid choice, defaulting to Warrior.")
        return Warrior()

def player_turn(player, enemy):
    print("\nYour turn! What will you do?")
    print("1. Attack")
    print("2. Heal")
    print("3. Use Ability 1")
    print("4. Use Ability 2")
    print("5. View Stats")
    action = input("Choose an action: ")
    if action == '1':
        player.attack(enemy)
    elif action == '2':
        player.heal(20)
    elif action == '3':
        player.ability_1(enemy)
    elif action == '4':
        player.ability_2(enemy)
    elif action == '5':
        player.show_stats()
        enemy.show_stats()
        player_turn(player, enemy)  # Let player choose again
    else:
        print("Invalid action. Try again.")
        player_turn(player, enemy)

def main():
    print("=== Welcome to the Battle Arena! ===")
    player = choose_character()
    wizard = EvilWizard()

    turn = 1
    while player.is_alive() and wizard.is_alive():
        print(f"\n--- Turn {turn} ---")
        player.show_stats()
        wizard.show_stats()

        player_turn(player, wizard)

        # End-of-turn effects for some classes
        if isinstance(player, Mage):
            player.end_turn()

        if not wizard.is_alive():
            print("\nCongratulations! You have defeated the Evil Wizard!")
            break

        # Evil Wizard's turn
        print("\nEvil Wizard's turn!")
        wizard.regenerate()
        wizard.evil_attack(player)
        if not player.is_alive():
            print("\nYou have been defeated by the Evil Wizard. Game Over.")
            break
        turn += 1

if __name__ == "__main__":
    main()
