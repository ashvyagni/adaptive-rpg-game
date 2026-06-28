# ⚔️ Adaptive RPG

> A modern desktop RPG built in **Python**, featuring adaptive enemy AI, turn-based combat, character progression, multiple classes, inventories, shops, leveling, and a polished desktop GUI.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-Qt-success)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## 📖 Overview

Adaptive RPG started as a simple terminal-based battle system and gradually evolved into a complete desktop RPG.

The project focuses on writing clean, modular Python code while implementing real game systems such as combat, progression, AI behavior, inventory management, saving/loading profiles, and a modern graphical interface.

Unlike many beginner RPGs, enemies don't simply attack every turn—they analyze how the player fights and adapt their strategy over time.

---

# ✨ Features

## ⚔️ Turn-Based Combat

* Interactive turn-based battles
* Randomized damage rolls
* Critical hit system
* Defense mechanic
* Healing abilities
* Mana system
* Adaptive enemy behavior

---

## 🧠 Adaptive AI

Enemies observe your fighting style.

They learn from your actions and gradually change their strategy.

Examples include:

* Becoming aggressive if you heal frequently
* Increasing defense if you constantly attack
* Changing priorities depending on your playstyle
* Scaling intelligently as the game progresses

No two battles feel exactly the same.

---

## 👤 Character Profiles

Create and manage multiple save profiles.

Each profile stores:

* Player Name
* Character Class
* Level
* Experience
* Gold
* Inventory
* Equipment
* Statistics
* Progress

---

# 🛡 Character Classes

Choose from multiple unique classes.

### 🗡 Knight

* High Health
* High Defense
* Balanced Damage

---

### 🔮 Mage

* High Mana
* Powerful Magic
* Fast Mana Regeneration

---

### ⚔ Duelist

* High Critical Chance
* High Damage
* Agile Playstyle

---

### 🛡 Tank

* Massive Health Pool
* Extremely High Defense
* Lower Damage

---

### 🏹 Ranger

* Balanced Stats
* High Accuracy
* Improved Dodge

---

# 📈 Progression

Gain experience after every battle.

Leveling up rewards stat points that can be invested into:

* ❤️ Max Health
* ⚔ Attack
* 🛡 Defense
* 🔷 Mana
* 💥 Critical Chance
* 🔥 Critical Damage
* ♻ Mana Regeneration

---

# 👹 Enemy Variety

Battle a growing roster of enemies.

Examples include:

* Goblin
* Skeleton
* Orc
* Bandit
* Knight
* Mage
* Slime
* Spider
* Dragon
* Necromancer

Each enemy has unique stats and behavior.

---

# 👑 Boss Battles

Epic boss encounters featuring:

* Multiple phases
* Stronger AI
* Unique abilities
* Increased difficulty
* Special rewards

---

# 🎒 Inventory System

Manage collected items through an inventory system.

Categories include:

* Weapons
* Armor
* Consumables
* Accessories
* Quest Items

---

# 🛍 Shop System

Spend earned gold to purchase upgrades.

Available items include:

* Weapons
* Armor
* Health Potions
* Mana Potions
* Accessories

Sell unused equipment to earn additional gold.

---

# 💰 Economy

Earn Gold by:

* Winning battles
* Completing quests
* Defeating bosses

Spend gold wisely to improve your build.

---

# 🎯 Equipment

Equip stronger gear to customize your build.

Equipment directly modifies player stats.

Examples:

* Swords
* Axes
* Staffs
* Bows
* Helmets
* Chestplates
* Rings
* Amulets

---

# ❤️ Health & Mana

Features include:

* Animated Health Bars
* Animated Mana Bars
* Passive Mana Regeneration
* Healing Abilities
* Resource Management

---

# 🎨 Modern GUI

Built with **PySide6 (Qt)**.

Features include:

* Modern desktop interface
* Smooth animations
* Interactive buttons
* Floating combat text
* Dynamic health bars
* Professional layout
* Responsive windows
* Dark fantasy inspired styling

---

# 💾 Save System

Supports:

* Multiple Profiles
* Save & Load
* Auto Save
* Persistent Progress

---

# 📂 Project Structure

```text
adaptive-rpg/
│
├── assets/
├── audio/
├── effects/
├── engine/
├── entities/
├── inventory/
├── save/
├── shop/
├── ui/
├── main.py
└── README.md
```

---

# 🛠 Technologies Used

* Python
* PySide6 (Qt)
* Object-Oriented Programming
* JSON
* Modular Architecture

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/adaptive-rpg.git
```

Navigate into the project:

```bash
cd adaptive-rpg
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python main.py
```

---

# 🎯 Future Improvements

* Multiplayer Battles
* Online Profiles
* Procedural Dungeons
* Skill Trees
* Crafting System
* Dialogue System
* Story Mode
* World Exploration
* Controller Support
* Steam Integration

---

# 📚 What I Learned

This project was built as a way to strengthen my understanding of:

* Object-Oriented Programming
* Python Architecture
* GUI Development
* Game Loops
* State Management
* AI Design
* Save Systems
* Modular Project Structure
* Software Engineering Principles

---

# 🤝 Contributing

Contributions, suggestions, and improvements are always welcome.

Feel free to fork the repository, submit issues, or open pull requests.

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ If you enjoyed this project

Consider giving the repository a ⭐ on GitHub—it helps others discover the project and supports future development.
