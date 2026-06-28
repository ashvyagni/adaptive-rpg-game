# Project Brain - Adaptive RPG Battle Game

## Current State Analysis

### Existing Backend (Preserve All Mechanics)
- **entities/player.py** - Player class with HP, attack, defense, mana, take_damage, heal, is_alive
- **entities/enemy.py** - Enemy class with HP, attack, defense, mana, take_damage, heal, basic_attack, is_alive
- **engine/battle.py** - Battle engine with:
  - Turn-based combat
  - Randomized damage (±4 variance)
  - Critical hits (15% chance, 2x damage)
  - Healing (20 HP, costs 25 mana)
  - Defense (reduces next damage by 50%, costs 15 mana)
  - Adaptive AI: tracks attack/heal/defend counts, adjusts strategy
  - Enemy adapts: heals often → stronger attacks; defends often → heavy attacks

### Current Issues Fixed
- Fixed indentation in battle.py

## Implementation Progress

### ✅ COMPLETED - Phase 1: Core Architecture & Data Models
- [x] **Enhanced Player class** - Added type hints, callbacks/signals, new stats (accuracy, speed, crit_chance, level, xp, mana_regen, gold), stat allocation system, equipment system, inventory system, status effects, achievement tracking
- [x] **Enhanced Enemy class** - Added type hints, callbacks/signals, new stats, 14 enemy types loaded from JSON, boss phases with stat bonuses, multiple AI personalities (aggressive, defensive, tactical, caster, predator, summoner, boss)
- [x] **Data files created**:
  - `data/classes.json` - 5 character classes (Knight, Mage, Duelist, Tank, Ranger) with unique stats, growth rates, mana regen
  - `data/items.json` - Complete item system with 6 rarity tiers (Common→Mythic), weapons, armor, accessories, consumables
  - `data/enemies.json` - 14 enemies with full stats, AI profiles, skills, loot tables, boss phases, dialogue
- [x] **Status effects system** - Poison, Burn, Freeze, Stun with duration/potency tracking
- [x] **Mana regeneration** - Per-turn mana regen based on class
- [x] **Gold economy** - Gold rewards, spending, shop integration

### ✅ COMPLETED - Phase 2: UI Framework (PySide6)
- [x] **Main Window** - QStackedWidget navigation between screens
- [x] **Custom Widgets**:
  - `CharacterStatsPanel` - Player/Enemy panels with animated HP/Mana/XP bars, portraits
  - `CombatLog` - Color-coded messages with icons, auto-scroll
  - `FloatingText` - Animated damage/heal/crit numbers with fade/slide
  - `ActionButton` - Styled buttons with hover/press states
  - `ProfileCard` - Profile selection cards with delete option
  - `ClassCard` - Class selection cards with stat previews
- [x] **Styling** - Dark fantasy theme (`ui/styles.py`), blue/purple accents, rounded corners, gradients, shadows

### ✅ COMPLETED - Phase 3: Battle Screen Implementation
- [x] **Enemy Panel (Top)** - Portrait, name, animated HP bar, phase indicator
- [x] **Battle Arena (Center)** - Floating damage numbers, screen shake, hit flashes
- [x] **Player Panel (Bottom)** - Portrait, name, HP/Mana/XP bars, stats
- [x] **Action Panel (Right)** - Attack/Heal/Defend buttons with costs
- [x] **Combat Log** - Color-coded messages with timestamps

### ✅ COMPLETED - Phase 4: Animation & Effects System
- [x] **Animated HP/Mana/XP bars** - QPropertyAnimation smooth interpolation
- [x] **Floating damage numbers** - Slide up + fade out, crit glow, miss indicator
- [x] **Screen shake** - On critical hits
- [x] **Flash effects** - Red flash on damage, green on heal, blue on defend
- [x] **AI message display** - Temporary yellow banner for enemy adaptation messages

### ✅ COMPLETED - Phase 5: AI Enhancement
- [x] **Enhanced AI personalities** - 7 distinct profiles with unique decision logic
- [x] **Pattern detection** - Tracks heal/attack/defend frequencies
- [x] **Dynamic adaptation** - Adjusts attack power, defense based on player behavior
- [x] **Boss phases** - 3-phase bosses with stat bonuses and new skills
- [x] **Visual AI feedback** - Messages like "Enemy notices healing pattern!", "Enemy adapts to defense!"

### ✅ COMPLETED - Phase 6: Polish & Features
- [x] **Save System** - JSON-based profile management (`save/save_manager.py`)
  - Create/load/delete/rename profiles
  - Auto-save on battle end
  - Save versioning for future compatibility
  - Export/import save data
- [x] **Profile Selection Screen** - List profiles with level, gold, battles won, playtime
- [x] **Class Selection Screen** - 5 classes with stat previews and descriptions
- [x] **Level Up Screen** - Stat point allocation with +/− buttons, reset, confirm/cancel
- [x] **Inventory Screen** - Tabbed (Consumables/Weapons/Armor/Accessories), use/equip/unequip/sell
- [x] **Shop Screen** - Buy/Sell tabs, level-filtered items, rarity-sorted, gold display
- [x] **Settings Screen** - Audio/Video/Gameplay/Data tabs, sliders, checkboxes, reset/export
- [x] **Equipment System** - 5 slots (weapon, chest, ring, amulet, boots), stat bonuses
- [x] **Gold Economy** - Battle rewards, shop purchases, selling items
- [x] **Achievement System** - Framework for tracking achievements
- [x] **Quest Framework** - Daily quests, battle objectives

## File Structure (Actual)
```
adaptive-game/
├── main.py                      # Entry point with MainWindow
├── brain.md                     # This file
├── config.json                  # User settings (auto-created)
├── data/
│   ├── classes.json             # 5 character classes
│   ├── items.json               # Complete item database
│   └── enemies.json             # 14 enemy types
├── entities/
│   ├── __init__.py
│   ├── player.py                # Enhanced Player with callbacks, equipment, inventory
│   └── enemy.py                 # Enhanced Enemy with AI profiles, boss phases
├── engine/
│   ├── __init__.py
│   └── battle.py                # Refactored Battle with signal/slot architecture
├── save/
│   ├── __init__.py
│   └── save_manager.py          # Profile management, JSON persistence
├── ui/
│   ├── __init__.py
│   ├── styles.py                # QSS dark fantasy theme
│   ├── screens.py               # ALL screens: Battle, ProfileSelect, ClassSelect, Inventory, Shop, Settings, LevelUp
│   └── widgets.py               # CharacterStatsPanel, CombatLog, FloatingText, ActionButton, ProfileCard, ClassCard, StartScreen, GameOverScreen
└── saves/                       # Profile JSON files (auto-created)
```

## Key Design Decisions

1. **Signal/Slot Architecture** - Battle engine emits signals, UI connects to them (decoupled)
2. **State Machine** - Battle states: PLAYER_TURN, ENEMY_TURN, ANIMATING, GAME_OVER
3. **Data-Driven** - Enemies, equipment, skills, classes from JSON files
4. **Extensible** - Plugin architecture for new enemies, effects, mechanics
5. **Async Animations** - Non-blocking animations using QTimer/QPropertyAnimation
6. **Profile-Based** - Multiple save slots, class-locked progression

## Remaining Tasks (Optional Polish)

### Audio System
- [ ] Audio manager class (`audio/audio_manager.py`)
- [ ] Sound effect placeholders (attack, heal, crit, levelup, victory, defeat, click, hover)
- [ ] Background music support
- [ ] Volume controls integration

### Visual Polish
- [ ] Particle effects system (`effects/particles.py`) - heal sparkles, crit explosions
- [ ] Better enemy portraits (replace generated circles with actual art)
- [ ] Status effect icons on character panels
- [ ] Battle background art per enemy type
- [ ] Transition animations between screens

### Gameplay Depth
- [ ] Skill/Ability system - Active skills with cooldowns, mana costs
- [ ] Status effect visual indicators on HP bars
- [ ] Enemy intent display (preview next attack)
- [ ] Difficulty settings
- [ ] New Game+ mode
- [ ] More enemy varieties
- [ ] Unique boss mechanics per boss

### Quality of Life
- [ ] Keyboard shortcuts (1/2/3 for actions)
- [ ] Tooltips on items/stats
- [ ] Battle speed slider
- [ ] Auto-battle option
- [ ] Detailed stats screen
- [ ] Battle history/log viewer

## Verification Commands

```bash
# Quick test launch
cd "/Users/flamexmystix/Documents/Sidequests/basic projects to make the github green/adaptive-game"
python3 -c "
import sys
from PySide6.QtWidgets import QApplication
app = QApplication(sys.argv)
from main import MainWindow
w = MainWindow()
w.show()
from PySide6.QtCore import QTimer
QTimer.singleShot(1000, app.quit)
app.exec()
print('SUCCESS')
"
```

## Architecture Notes for Future Expansion

- **Adding new enemies**: Add to `data/enemies.json`, no code changes needed
- **Adding new items**: Add to `data/items.json`, automatically appears in shop/inventory
- **Adding new classes**: Add to `data/classes.json`, automatically appears in class select
- **New status effects**: Extend `StatusEffect` enum in player/enemy, add processing logic
- **New screens**: Add to `ui/screens.py`, register in MainWindow stacked widget
- **Save versioning**: Increment `SAVE_VERSION` in save_manager, add migration logic