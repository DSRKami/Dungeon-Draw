### Overview



**Dungeon Draw** is a CLI-based, dungeon crawler card game built around the **Higher** or **Lower** card game. Each card drawn represents a room in the dungeon, and the player predicts whether the next room's card will be higher or lower in value. Different suits trigger different room types, each with their own behaviour and effects.



The goal is to survive till the end of the suit, score as much points as possible, collect gold, and conquer the dungeon.



##### How to Play

1. You start with **20HP**, no armour, and a random room (card).
2. On each turn, you guess whether the next card will be **Higher (H)** or **Lower (L)** in rank.
3. The next card is revealed: if you predicted correctly, you gain some score and the room helps you, but if you guessed wrong, then the room punishes you.
4. You continue until: **your HP drops to 0,** you **run out of cards (escape the dungeon)**, or you quit early **Q**.



Card Values: 2 < 3 < … < J < Q < J < A (A = highest)



##### Room Types

Each suit represents a different kind of room in the dungeon.



♠ Spades – Enemy Rooms



Spades trigger combat encounters. There are three enemy types chosen at random:



* Goblin: Simple, flat-damage enemy. Hits harder if you guessed wrong.
* Slime: Applies poison over time, dealing damage across several turns. Worse poison if your guess was wrong.
* Warlock: Curses you. Damage scales with your current HP, so they’re more dangerous when you’re healthy.



♥ Hearts – Healing Rooms



You find ways to recover here, but not all healing works the same:



* Pure Heal: Straight HP restore.
* Regeneration: Grants healing over several turns.
* Blessing of Fortune: Can give either a big burst heal or a permanent Max HP increase.



♦ Diamonds – Treasure Rooms



Simple risk vs reward. Correct guess is a big gold gain, but a wrong guess trippers a trap, while still getting some gold.



♣ Clubs – Utility / Traps



Useful tools or painful traps depending on your guess:



* Totem of Rebirth: A one-time revive if you drop below 0 HP.
* Escape Rope: Lets you skip the next hostile room (Spades or Clubs).
* Sharpening Stone: Grants permanent armour.



Wrong guess triggers a trap: can cause HP loss or armour break.



##### Jester Boss Encounter

Two special Jester cards are hidden in the deck. Drawing one triggers a mini-boss fight.



**How the fight works:**

* You must make 5 consecutive predictions (H/L).
* Get 3 or more correct: you defeat the Jester.
* Fail and he heavily punishes your HP and gold.



It acts as a break from the normal loop and adds high-stakes tension.



##### Stats \& Effects

**Poison**: Damage every turn until it expires

**Regeneration**: Small heal each turn

**Armor**: Reduces incoming damage

**Streak**: Consecutive correct guesses; increases score and tracked for “best streak”

**Gold**: Gained from enemies and treasure; just a score-like resource for now



##### Design Choices \& Why hey Were Made

I wanted something more interesting than a straight forward Higher/Lower game, so I tried to combine that basic mechanic with some **roguelike** elements. Here's the reasoning behind the major choices:



**Keeping Higher/Lower as the Foundation**

The assignment requires a card game 'such as Higher/Lower', so I kept that structure and built a dungeon crawler theme on top to give it more of an identity.



**Adding Enemies, Healing Types, Utility Items**

I wanted a basic amount of strategy and gameplay variations, so I added different suits (hearts: healing, diamonds: treasure, etc.) so that the game was less predictable. A basic balance of enemies, treasure, healing and utility items seemed like a good balance to me, but in retrospect I should push for more variety in player difficulty.



**Poison and Regen Over Time Effects**

I wanted to create small decisions and tensions across multiple turns, instead of each turn being isolated. It would be good to expand upon these more.



**Totem and Escape Rope**

These were added to give the player tools to recover from luck swings, especially as higher/lower is inherently random. But I need to add elements to balance the difficulty back away from the player's direction.



**The Jester Boss Fight**

I wanted a 'unique twist', and the Jester encounter adds a dramatic break in the regular pacing of the game. It also gives a decent sense of progression and narrative, while also feeling more 'high-stakes'. 



##### Potential Ideas \& Future Improvements



**Shops**

It would be good to give gold an actual purpose within gameplay other than being a glorified second score tracker. Thinks like full heals, temporary buffs, or more one time consumables would be interesting.



**Difficulty Modes**

I should add a difficulty selector at the beginning of the game, that would likely do things like scaling healing damage, scaling enemy damage, poison severity, but perhaps boosting score and gold gain.



**More Bosses**

Bosses for specific cards could be interesting idea.



**Expand the Events that can happen to the Player**

I could expand the events the player can encounter based on the card they get, or just based on random chance.



**Graphical Version**

A simple Pygame variant could turn the game into something much more visual.

