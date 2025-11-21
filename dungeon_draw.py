import random
import sys


# Define Constants for Cards and Decks
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
JESTER_SUIT = "Jester" # To be implemented into a boss fight

RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠",
    JESTER_SUIT: "🃏"
}

# Define the Card Class
class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    @property
    def value(self) -> int:
        return RANK_VALUES.get(self.rank, 0)

    @property
    def symbol(self) -> str:
        return SUIT_SYMBOLS.get(self.suit, "?")

    def __str__(self) -> str:
        return f"{self.rank}{self.symbol}"
    
    # Create the ASCII representation of the card
    def to_ascii_lines(self):
        inside_width = 9
        top = "┌" + "─" * inside_width + "┐"
        bottom = "└" + "─" * inside_width + "┘"

        rank = self.rank
        rank_top = f"│{rank:<2}" + " " * (inside_width - 2) + "│"
        rank_bottom = "│" + " " * (inside_width - 2) + f"{rank:>2}│"
        blank = "│" + " " * inside_width + "│"
        suit_line = "│" + self.symbol.center(inside_width) + "│"

        return [
            top,
            rank_top,
            blank,
            suit_line,
            blank,
            rank_bottom,
            bottom,
        ]


# Define the Deck Class to hold a set of cards
class Deck:
    def __init__(self):
        # Initialises a standard 52 card deck
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        # Add Two Jester Boss Cards
        self.cards.append(Card('J', JESTER_SUIT))
        self.cards.append(Card('J', JESTER_SUIT))
        random.shuffle(self.cards) # .Shuffle used to randomise the deck (its just convenient)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop(0)

    def remaining(self) -> int:
        return len(self.cards)


# Gameplay Logic

class DungeonDrawGame:
    def __init__(self):
        # Initialise Game State and Stats
        self.deck = Deck()
        self.max_hp = 20
        self.hp = self.max_hp
        self.gold = 0
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.armor = 0

        # Over Time Effects
        self.poison_turns = 0
        self.poison_damage_per_turn = 0
        self.regen_turns = 0
        self.regen_amount_per_turn = 0

        # Items
        self.totem_charges = 0       
        self.escape_rope_charges = 0 

        # Jester Boss State
        self.in_jester_fight = False
        self.jester_turns_left = 0
        self.jester_correct = 0

        # Draw First Card (Make sure it's not a Jester)
        first = self.deck.draw()
        while first is not None and first.suit == JESTER_SUIT:
            self.deck.cards.append(first)
            random.shuffle(self.deck.cards)
            first = self.deck.draw()
        self.current_card = first

    # Helper Methods

    def take_damage(self, amount: int, source: str = ""):
        if amount <= 0:
            return
        self.hp -= amount
        if self.hp <= 0 and self.totem_charges > 0:
            self.totem_charges -= 1
            self.hp = self.max_hp // 2
            print("\n*** The Totem Shatters, pulling you back from the very brink of death! ***")
            print(f"You are restored to {self.hp} HP.\n")

        if self.hp < 0:
            self.hp = 0

    def apply_over_time_effects(self):
        # Poison Ticks First
        if self.poison_turns > 0 and self.poison_damage_per_turn > 0 and self.hp > 0:
            dmg = self.poison_damage_per_turn
            print(f"Poison courses through your veins for {dmg} damage!")
            self.take_damage(dmg, source="poison")
            self.poison_turns -= 1
            if self.poison_turns == 0:
                self.poison_damage_per_turn = 0
                print("The poison finally fades.")

        # Then Regen Ticks
        if self.regen_turns > 0 and self.regen_amount_per_turn > 0 and self.hp > 0:
            heal = self.regen_amount_per_turn
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + heal)
            actual = self.hp - old_hp
            print(f"Regenerative magic fixes your wounds. You heal {actual} HP.")
            self.regen_turns -= 1
            if self.regen_turns == 0:
                self.regen_amount_per_turn = 0
                print("Your regenerative blessing fades.")

    # UI Display Methods

    def display_title(self):
        print("=" * 40)
        print("      WELCOME TO DUNGEON DRAW      ")
        print("=" * 40)

    def display_hud(self):
        print("-" * 40)
        hearts = f"{self.hp}/{self.max_hp}"
        print(
            f"HP: {hearts:<7}  Gold: {self.gold:<4}  "
            f"Streak: {self.streak:<2} (Best: {self.best_streak})"
        )
        print(
            f"Armor: {self.armor:<2} "
            f"Cards left: {self.deck.remaining():<3}  "
            f"Totem: {self.totem_charges}  Escape Rope: {self.escape_rope_charges}"
        )
        print("-" * 40)

    def display_card(self, card: Card, title: str = None):
        if title:
            print(title)
        for line in card.to_ascii_lines():
            print(line)
        print()

    def display_two_cards(self, left: Card, right: Card,
                          left_title="Current room:", right_title="Next room:"):
        left_lines = left.to_ascii_lines()
        right_lines = right.to_ascii_lines()

        print(left_title)
        print(right_title.rjust(len(right_title) + 18))
        print()

        for l, r in zip(left_lines, right_lines):
            print(l + "   " + r)
        print()

    def display_jester_face(self):
        art = [
    "         /\\  \\",
    "        /  \\/ \\",
    "   ___  \\   O /  ___",
    "  /    \\ \\   / /    \\",
    " /   __ -    -  __   \\",
    "/___/ | <>   <> | \\___\\",
    "O  ___|    ^    |___  O",
    " /     \\  -^-  /    \\",
    "/   /\\  \\_____/ /\\   \\",
    "\\_ / /          \\ \\_ /",
    "O   /   /\\   /\\  \\  O",
    "     \\ /  \\ /  \\ /",
    "      O    O    O"
        ]
        for line in art:
            print(line)
        print()

    # Core Game Logic

    def check_guess(self, guess: str, current: Card, next_card: Card) -> str:
        if next_card.value == current.value:
            return 'equal'
        if next_card.value > current.value and guess == 'h':
            return 'correct'
        if next_card.value < current.value and guess == 'l':
            return 'correct'
        return 'incorrect'

    # Suit Behaviour with Variants

    def handle_spades_enemy(self, correct: bool, value: int):
        enemy_type = random.choice(["goblin", "slime", "warlock"])

        if enemy_type == "goblin":
            print("Enemy Room (Goblin): A sneaky goblin rushes you!")
            if correct:
                damage = max(0, value // 3 - self.armor)
                loot = value // 2
                self.take_damage(damage)
                self.gold += loot
                print(f"You stab first! You take {damage} damage and loot {loot} gold.")
            else:
                damage = max(1, value - self.armor)
                self.take_damage(damage)
                print(f"The goblin slashes wildly! You take {damage} damage.")

        elif enemy_type == "slime":
            print("Enemy Room (Slime): A dripping slime oozes toward you.")
            # Immediate Damage is Small But Poisons
            if correct:
                damage = max(0, value // 4 - self.armor)
                self.take_damage(damage)
                # Light Poison
                extra_turns = 2
                poison_strength = max(1, value // 6)
            else:
                damage = max(1, value // 3 - self.armor)
                self.take_damage(damage)
                # Heavy Poison
                extra_turns = 3
                poison_strength = max(1, value // 4)

            # Stack Poison
            if self.poison_turns == 0:
                self.poison_turns = extra_turns
                self.poison_damage_per_turn = poison_strength
            else:
                self.poison_turns += extra_turns
                self.poison_damage_per_turn = max(self.poison_damage_per_turn,
                                                  poison_strength)

            print(f"The slime's toxins melt into your wounds; you are poisoned "
                  f"({self.poison_damage_per_turn} dmg for {self.poison_turns} turns).")

        elif enemy_type == "warlock":
            print("Enemy Room (Warlock): A corrupt warlock mutters a curse.")
            if correct:
                # Reduced curse if you guessed right
                damage = max(3, (value // 2) + (self.hp // 20) - self.armor)
            else:
                damage = max(5, value + (self.hp // 10) - self.armor)
            self.take_damage(damage)
            print(f"Dark magic drains your lifespan for {damage} damage.")

    def handle_hearts_heal(self, correct: bool, value: int):
        heal_type = random.choice(["pure", "regen", "blessing"])

        if heal_type == "pure":
            print("Rest Room (Pure Healing): A calm fountain restores you.")
            if correct:
                heal = value
            else:
                heal = max(1, value // 3)
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + heal)
            actual = self.hp - old_hp
            print(f"You heal {actual} HP.")

        elif heal_type == "regen":
            print("Rest Room (Regeneration): A green aura wraps around you.")
            if correct:
                turns = 3
                per_turn = max(1, value // 4)
            else:
                turns = 2
                per_turn = max(1, value // 6)

            if self.regen_turns == 0:
                self.regen_turns = turns
                self.regen_amount_per_turn = per_turn
            else:
                self.regen_turns += turns
                self.regen_amount_per_turn = max(self.regen_amount_per_turn, per_turn)

            print(f"You feel your body putting itself back together over time "
                  f"({self.regen_amount_per_turn} HP for {self.regen_turns} turns).")

        elif heal_type == "blessing":
            print("Rest Room (Blessing of Fortune): A radiant altar hums with power.")
            if random.random() < 0.5:
                # big immediate heal
                heal = value * (2 if correct else 1)
                old_hp = self.hp
                self.hp = min(self.max_hp, self.hp + heal)
                actual = self.hp - old_hp
                print(f"You receive a surge of holy light, healing {actual} HP.")
            else:
                # max HP boost
                boost = 3 if correct else 1
                self.max_hp += boost
                self.hp += boost  # small top-up too
                print(f"Your body is permanently strengthened! Max HP +{boost}.")

    def handle_clubs_utility(self, correct: bool, value: int):
        if correct:
            # You Safely Explore the Room and Find an Item
            utility_type = random.choice(["totem", "escape", "stone"])
            if utility_type == "totem":
                if self.totem_charges == 0:
                    self.totem_charges = 1
                    print("Equipment Room: You find a Totem of Rebirth.")
                    print("If you die, the totem will save you once.")
                else:
                    # Already Have One: Gain Armor Instead
                    self.armor += 1
                    print("You find another eerie totem, but its magic is unstable.")
                    print("Instead, you reinforce your armor. Armor +1.")
            elif utility_type == "escape":
                self.escape_rope_charges += 1
                print("Equipment Room: You find an Escape Rope.")
                print("You can automatically skip the next hostile room once.")
            elif utility_type == "stone":
                self.armor += 1
                print("Equipment Room: A Sharpening Stone lets you upgrade your gear.")
                print("Your armor increases by 1.")
        else:
            # Trap Outcome
            damage = max(1, value // 2)
            self.take_damage(damage)
            if self.armor > 0 and random.random() < 0.5:
                self.armor -= 1
                print("Equipment Room (Trap): Gears and blades launch from the walls!")
                print(f"You take {damage} damage and lose 1 armor.")
            else:
                print("Equipment Room (Trap): Hidden spikes shoot up from the floor!")
                print(f"You take {damage} damage.")

    def room_effect(self, result: str, card: Card):
        # Jester Cards are Handled Elsewhere
        if card.suit == JESTER_SUIT:
            return

        suit = card.suit
        value = card.value

        # Base Result Messaging
        if result == 'equal':
            self.score += 1
            print("You navigate carefully through the room, but nothing major happens.")
            return

        if result == 'correct':
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            self.score += 10 + value // 2
            print("Your senses were right; you've successfully navigated the room!")
            correct = True
        else:
            self.streak = 0
            self.score = max(0, self.score - 5)
            print("You misjudged the room's danger and suffered the consequences!")
            correct = False

        # Suit Specific Logic
        if suit == "Spades":
            self.handle_spades_enemy(correct, value)

        elif suit == "Hearts":
            self.handle_hearts_heal(correct, value)

        elif suit == "Diamonds":
            if correct:
                gold_gain = value * 2
                self.gold += gold_gain
                print("Treasure Room: You find a chest filled to the brim with gold!")
                print(f"You gain {gold_gain} gold.")
            else:
                damage = max(1, value // 2)
                gold_gain = value // 2
                self.take_damage(damage)
                self.gold += gold_gain
                print("Treasure Room: A trap triggers as you open the chest!")
                print(f"You take {damage} damage and only get {gold_gain} gold.")

        elif suit == "Clubs":
            self.handle_clubs_utility(correct, value)

    # Jester Boss Logic

    def start_jester_fight(self):
        self.in_jester_fight = True
        self.jester_turns_left = 5
        self.jester_correct = 0

        print("\n" + "=" * 40)
        print("🃏  THE JESTER APPEARS!  🃏")
        print("=" * 40)
        self.display_jester_face()
        print("The dungeon twists into a chaotic carnival.")
        print("For the next 5 draws, you must predict at least 3 correctly.")
        print("Succeed, and you outwit the Jester. Fail, and he drains your life and gold.")
        print()

        previous_card = self.current_card

        while (
            self.jester_turns_left > 0
            and self.hp > 0
            and self.deck.remaining() > 0
        ):
            self.apply_over_time_effects()
            if self.hp <= 0:
                break

            self.display_hud()
            self.display_card(previous_card, title="Jester's current card:")

            guess = None
            while True:
                raw = input("Jester draw: Higher (H) or Lower (L)? (H/L): ").strip().lower()
                if raw in ('h', 'l'):
                    guess = raw
                    break
                print("Invalid input. Please enter H or L.")

            next_card = self.deck.draw()
            if next_card is None:
                print("The Jester's carnival collapses suddenly the deck is empty!")
                break

            print()
            self.display_two_cards(
                previous_card, next_card,
                left_title="Current card:",
                right_title="Jester's draw:"
            )

            result = self.check_guess(guess, previous_card, next_card)
            print(f"You guessed: {'Higher' if guess == 'h' else 'Lower'}")
            print(f"Jester drew: {next_card.rank}{next_card.symbol}")

            if result == 'correct':
                self.jester_correct += 1
                print("You read his games correctly. The Jester snarls.")
            elif result == 'incorrect':
                print("Your prediction fails. The Jester laughs at your misfortune.")
            else:
                print("Equal value the Jester tilts his head, amused but unimpressed.")

            self.jester_turns_left -= 1
            previous_card = next_card

            if self.jester_turns_left > 0 and self.hp > 0:
                print()
                input("Press Enter for the next Jester draw...")
                print()

        self.current_card = previous_card
        self.end_jester_fight()

    def end_jester_fight(self):
        print("\n" + "-" * 40)
        print("The Jester's game comes to an end...")
        print(f"Correct predictions in his carnival: {self.jester_correct}/5")

        if self.jester_correct >= 3:
            bonus_gold = 30
            bonus_score = 20
            bonus_heal = 5
            self.gold += bonus_gold
            self.score += bonus_score
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + bonus_heal)
            healed = self.hp - old_hp

            print("You outplay the Jester! He claps slowly, then vanishes in smoke.")
            print(f"You gain {bonus_gold} gold, {bonus_score} score, and heal {healed} HP.")
        else:
            hp_loss = 15
            gold_loss = 20
            self.take_damage(hp_loss)
            self.gold = max(0, self.gold - gold_loss)

            print("The Jester cackles wildly as your luck runs dry.")
            print(f"He steals {gold_loss} of your gold and rips away {hp_loss} HP!")

        self.in_jester_fight = False
        print("-" * 40 + "\n")

    # Main Gameplay Loop

    def play(self):
        self.display_title()
        print("You descend into the dungeon, ready to face its challenges.")
        print("Predict whether the card in the next room is HIGHER or LOWER in power than the current one!")
        print("H = Higher; L = Lower; Q = Quit")
        print()

        while self.hp > 0 and self.deck.remaining() > 0:
            # Over Time Effects at the Start of Turn
            self.apply_over_time_effects()
            if self.hp <= 0:
                break

            self.display_hud()
            self.display_card(self.current_card, title="Current Room:")

            # Take in the Player's Guess
            guess = None
            while True:
                raw = input(
                    "Will the next room's card be Higher (H) or Lower (L)? (H/L/Q): "
                ).strip().lower()
                if raw in ['h', 'l', 'q']:
                    guess = raw
                    break
                print("Invalid input. Please enter H, L, or Q.")

            if guess == 'q':
                print("You choose to leave the dungeon early.")
                break

            next_card = self.deck.draw()
            if next_card is None:
                print("The dungeon collapses behind you as there are no more rooms left!")
                break

            # Escape Rope Logic: Skip 1 Hostile Room
            if self.escape_rope_charges > 0 and next_card.suit in ("Spades", "Clubs"):
                print()
                self.display_two_cards(self.current_card, next_card,
                                       left_title="Current Room:",
                                       right_title="Next Room (skipped):")
                print("Your Escape Rope activates! You flee this hostile room unscathed.")
                self.escape_rope_charges -= 1
                # You Move into the Next Room Safely
                self.current_card = next_card
                print()
                input("Press Enter to continue...")
                print()
                continue

            # Jester Boss Trigger
            if next_card.suit == JESTER_SUIT:
                print()
                print("You draw a strange card...")
                self.display_card(next_card, title="Jester Card:")
                self.start_jester_fight()
                if self.hp <= 0:
                    break
                continue

            result = self.check_guess(guess, self.current_card, next_card)

            print()
            self.display_two_cards(self.current_card, next_card)
            print(f"You guessed: {'Higher' if guess == 'h' else 'Lower'}")
            print(f"The next room was: {next_card.rank} ({next_card.value})")

            self.room_effect(result, next_card)

            if self.hp <= 0:
                print()
                print("You have succumbed to the dangers of the dungeon... it claims yet another soul.")
                break

            self.current_card = next_card
            print()
            input("Press Enter to continue to the next room!")
            print()

        # End of Game Summary
        print("=" * 40)
        print("          DUNGEON RUN SUMMARY          ")
        print("=" * 40)
        print(f"Final HP: {self.hp}/{self.max_hp}")
        print(f"Gold Collected: {self.gold}")
        print(f"Final Score: {self.score}")
        print(f"Best Streak: {self.best_streak}")
        if self.hp > 0 and self.deck.remaining() == 0:
            print("You've conquered the dungeon deck! Well done adventurer!")
        elif self.hp <= 0:
            print("Your journey ends here... but the dungeon awaits your return.")
        else:
            print("You turned back before uncovering all its secrets. Until next time...")
        print("=" * 40)


def main():
    while True:
        game = DungeonDrawGame()
        game.play()
        choice = input("Play Again? (y/n): ").strip().lower()
        if choice != 'y':
            print("Thanks For Playing Dungeon Draw!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
