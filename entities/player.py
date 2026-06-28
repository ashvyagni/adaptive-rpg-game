from dataclasses import dataclass, field
from typing import Callable, Optional, List, Dict, Any
from enum import Enum
import json
import os


class StatusEffect(Enum):
    POISON = "poison"
    BURN = "burn"
    FREEZE = "freeze"
    STUN = "stun"


@dataclass
class ActiveEffect:
    effect: StatusEffect
    duration: int
    potency: int = 1
    source: str = ""


class Player:
    CLASS_DATA = {}
    
    def __init__(
        self,
        name: str,
        character_class: str = "knight",
        profile_id: str = "",
        maxhealth: int = 100,
        attack: int = 10,
        defense: int = 5,
        mana: int = 50,
        accuracy: int = 90,
        speed: int = 10,
        crit_chance: int = 5,
        level: int = 1,
        xp: int = 0,
        gold: int = 0,
        mana_regen: int = 3,
    ):
        self.name = name
        self.character_class = character_class
        self.profile_id = profile_id
        self.created_at = ""
        
        self.level = level
        self.xp = xp
        self.xp_to_next = 100
        self.gold = gold
        
        self.maxhealth = maxhealth
        self.health = maxhealth
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.maxmana = mana
        self.accuracy = accuracy
        self.speed = speed
        self.crit_chance = crit_chance
        self.mana_regen = mana_regen
        
        self.stat_points = 0
        
        self.base_maxhealth = maxhealth
        self.base_attack = attack
        self.base_defense = defense
        self.base_mana = mana
        self.base_accuracy = accuracy
        self.base_speed = speed
        self.base_crit_chance = crit_chance
        self.base_mana_regen = mana_regen
        
        self.defending = False
        self.status_effects: List[ActiveEffect] = []
        
        self.inventory: List[Dict] = []
        self.equipment: Dict[str, Optional[str]] = {
            "main_hand": None, "chest": None, "ring": None, "amulet": None, "boots": None
        }
        self.skills: List[str] = []
        
        self.completed_battles = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.total_healed = 0
        self.critical_hits = 0
        self.enemies_defeated: Dict[str, int] = {}
        self.achievements: List[str] = []
        self.quests_completed: List[str] = []
        self.playtime_seconds = 0
        
        self.on_health_changed: Optional[Callable[[int, int], None]] = None
        self.on_mana_changed: Optional[Callable[[int, int], None]] = None
        self.on_damage_taken: Optional[Callable[[int, bool, bool], None]] = None
        self.on_heal: Optional[Callable[[int], None]] = None
        self.on_crit: Optional[Callable[[int], None]] = None
        self.on_defend: Optional[Callable[[], None]] = None
        self.on_status_applied: Optional[Callable[[StatusEffect, int], None]] = None
        self.on_status_removed: Optional[Callable[[StatusEffect], None]] = None
        self.on_level_up: Optional[Callable[[int], None]] = None
        self.on_death: Optional[Callable[[], None]] = None
        self.on_gold_changed: Optional[Callable[[int], None]] = None
        self.on_stat_changed: Optional[Callable[[str, int], None]] = None
        self.on_mana_regen: Optional[Callable[[int], None]] = None
        self.on_equipment_changed: Optional[Callable[[], None]] = None
    
    @classmethod
    def load_class_data(cls):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'classes.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                cls.CLASS_DATA = json.load(f)
    
    @classmethod
    def create_from_class(cls, name: str, character_class: str, profile_id: str = "") -> 'Player':
        if not cls.CLASS_DATA:
            cls.load_class_data()
        
        class_data = cls.CLASS_DATA.get(character_class, cls.CLASS_DATA.get('knight', {}))
        stats = class_data.get('primary_stats', {})
        
        return cls(
            name=name,
            character_class=character_class,
            profile_id=profile_id,
            maxhealth=stats.get('maxhealth', 100),
            attack=stats.get('attack', 10),
            defense=stats.get('defense', 5),
            mana=stats.get('mana', 50),
            accuracy=stats.get('accuracy', 90),
            speed=stats.get('speed', 10),
            crit_chance=stats.get('crit_chance', 5),
            level=1,
            xp=0,
            gold=100,
            mana_regen=class_data.get('mana_regen', 3),
        )
    
    def take_damage(self, amount: int, is_crit: bool = False, is_miss: bool = False):
        if is_miss:
            if self.on_damage_taken:
                self.on_damage_taken(0, False, True)
            return
        
        actual_damage = max(0, amount)
        self.health = max(0, self.health - actual_damage)
        self.total_damage_taken += actual_damage
        
        if self.on_health_changed:
            self.on_health_changed(self.health, self.maxhealth)
        if self.on_damage_taken:
            self.on_damage_taken(actual_damage, is_crit, False)
        
        if self.health <= 0 and self.on_death:
            self.on_death()
    
    def heal(self, amount: int):
        if self.health >= self.maxhealth:
            return
        old_health = self.health
        self.health = min(self.maxhealth, self.health + amount)
        healed = self.health - old_health
        if healed > 0:
            self.total_healed += healed
            if self.on_health_changed:
                self.on_health_changed(self.health, self.maxhealth)
            if self.on_heal:
                self.on_heal(healed)
    
    def restore_mana(self, amount: int):
        old_mana = self.mana
        self.mana = min(self.maxmana, self.mana + amount)
        regenerated = self.mana - old_mana
        if regenerated > 0 and self.on_mana_changed:
            self.on_mana_changed(self.mana, self.maxmana)
            if self.on_mana_regen:
                self.on_mana_regen(regenerated)
    
    def regenerate_mana(self):
        self.restore_mana(self.mana_regen)
    
    def spend_mana(self, cost: int) -> bool:
        if self.mana >= cost:
            self.mana -= cost
            if self.on_mana_changed:
                self.on_mana_changed(self.mana, self.maxmana)
            return True
        return False
    
    def add_gold(self, amount: int):
        self.gold += amount
        if self.on_gold_changed:
            self.on_gold_changed(self.gold)
    
    def spend_gold(self, amount: int) -> bool:
        if self.gold >= amount:
            self.gold -= amount
            if self.on_gold_changed:
                self.on_gold_changed(self.gold)
            return True
        return False
    
    def set_defending(self, defending: bool):
        self.defending = defending
        if defending and self.on_defend:
            self.on_defend()
    
    def apply_crit(self, damage: int):
        if self.on_crit:
            self.on_crit(damage)
    
    def add_status(self, effect: StatusEffect, duration: int, potency: int = 1):
        for active in self.status_effects:
            if active.effect == effect:
                active.duration = max(active.duration, duration)
                active.potency = max(active.potency, potency)
                return
        self.status_effects.append(ActiveEffect(effect, duration, potency))
        if self.on_status_applied:
            self.on_status_applied(effect, duration)
    
    def remove_status(self, effect: StatusEffect):
        self.status_effects = [e for e in self.status_effects if e.effect != effect]
        if self.on_status_removed:
            self.on_status_removed(effect)
    
    def process_status_effects(self):
        for active in self.status_effects[:]:
            if active.effect == StatusEffect.POISON:
                self.take_damage(active.potency * 3)
            elif active.effect == StatusEffect.BURN:
                self.take_damage(active.potency * 4)
            active.duration -= 1
            if active.duration <= 0:
                self.remove_status(active.effect)
    
    def gain_xp(self, amount: int):
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.stat_points += 5
        
        growth = self.CLASS_DATA.get(self.character_class, {}).get('stat_growth', {})
        self.maxhealth += growth.get('maxhealth', 10)
        self.health = self.maxhealth
        self.attack += growth.get('attack', 2)
        self.defense += growth.get('defense', 1)
        self.maxmana += growth.get('mana', 10)
        self.mana = self.maxmana
        self.accuracy += growth.get('accuracy', 1)
        self.speed += growth.get('speed', 1)
        self.crit_chance += growth.get('crit_chance', 0)
        
        self.base_maxhealth = self.maxhealth
        self.base_attack = self.attack
        self.base_defense = self.defense
        self.base_mana = self.maxmana
        self.base_accuracy = self.accuracy
        self.base_speed = self.speed
        self.base_crit_chance = self.crit_chance
        
        if self.on_health_changed:
            self.on_health_changed(self.health, self.maxhealth)
        if self.on_mana_changed:
            self.on_mana_changed(self.mana, self.maxmana)
        if self.on_stat_changed:
            for stat in ['maxhealth', 'attack', 'defense', 'maxmana', 'accuracy', 'speed', 'crit_chance']:
                self.on_stat_changed(stat, getattr(self, stat))
        if self.on_level_up:
            self.on_level_up(self.level)
    
    def allocate_stat(self, stat: str) -> bool:
        if self.stat_points <= 0:
            return False
        
        growth = self.CLASS_DATA.get(self.character_class, {}).get('stat_growth', {})
        
        if stat == "maxhealth":
            self.maxhealth += growth.get('maxhealth', 10) + 5
            self.health = self.maxhealth
        elif stat == "attack":
            self.attack += growth.get('attack', 2) + 2
        elif stat == "defense":
            self.defense += growth.get('defense', 1) + 2
        elif stat == "mana":
            self.maxmana += growth.get('mana', 10) + 5
            self.mana = self.maxmana
        elif stat == "crit_chance":
            self.crit_chance += growth.get('crit_chance', 1) + 1
        elif stat == "mana_regen":
            self.mana_regen += 1
        else:
            return False
        
        self.stat_points -= 1
        
        if self.on_stat_changed:
            self.on_stat_changed(stat, getattr(self, stat))
        if self.on_health_changed and stat in ["maxhealth", "health"]:
            self.on_health_changed(self.health, self.maxhealth)
        if self.on_mana_changed and stat in ["mana", "maxmana"]:
            self.on_mana_changed(self.mana, self.maxmana)
        
        return True
    
    def get_effective_stats(self) -> Dict[str, int]:
        stats = {
            "maxhealth": self.maxhealth,
            "attack": self.attack,
            "defense": self.defense,
            "maxmana": self.maxmana,
            "accuracy": self.accuracy,
            "speed": self.speed,
            "crit_chance": self.crit_chance,
            "mana_regen": self.mana_regen,
        }
        
        for slot, item_id in self.equipment.items():
            if item_id:
                item = self.get_item(item_id)
                if item and 'base_stats' in item:
                    for stat, value in item['base_stats'].items():
                        if stat in stats:
                            stats[stat] += value
        
        return stats
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        items_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'items.json')
        if os.path.exists(items_path):
            with open(items_path, 'r') as f:
                all_items = json.load(f)
                for category in all_items.values():
                    if isinstance(category, dict) and item_id in category:
                        return category[item_id]
        return None
    
    def equip_item(self, item_id: str) -> bool:
        item = self.get_item(item_id)
        if not item:
            return False
        
        slot = item.get('slot', '')
        if slot not in self.equipment:
            return False
        
        level_req = item.get('level_req', 1)
        if self.level < level_req:
            return False
        
        if self.equipment[slot]:
            self.unequip_item(slot)
        
        self.equipment[slot] = item_id
        if item_id in self.inventory:
            self.inventory.remove(item_id)
        
        if self.on_equipment_changed:
            self.on_equipment_changed()
        return True
    
    def unequip_item(self, slot: str) -> Optional[str]:
        item_id = self.equipment.get(slot)
        if item_id:
            self.inventory.append(item_id)
            self.equipment[slot] = None
            if self.on_equipment_changed:
                self.on_equipment_changed()
        return item_id
    
    def add_to_inventory(self, item_id: str, quantity: int = 1):
        item = self.get_item(item_id)
        if not item:
            return
        
        if item.get('stackable', False):
            for inv_item in self.inventory:
                if isinstance(inv_item, dict) and inv_item.get('id') == item_id:
                    inv_item['quantity'] = min(inv_item.get('quantity', 1) + quantity, item.get('max_stack', 99))
                    return
            self.inventory.append({'id': item_id, 'quantity': quantity})
        else:
            for _ in range(quantity):
                self.inventory.append(item_id)
    
    def remove_from_inventory(self, item_id: str, quantity: int = 1) -> bool:
        for i, inv_item in enumerate(self.inventory):
            if isinstance(inv_item, dict) and inv_item.get('id') == item_id:
                inv_item['quantity'] -= quantity
                if inv_item['quantity'] <= 0:
                    self.inventory.pop(i)
                return True
            elif inv_item == item_id:
                self.inventory.pop(i)
                quantity -= 1
                if quantity <= 0:
                    return True
        return False
    
    def use_consumable(self, item_id: str) -> bool:
        item = self.get_item(item_id)
        if not item or item.get('type') != 'consumable':
            return False
        
        effects = item.get('effects', {})
        if 'heal' in effects:
            self.heal(effects['heal'])
        if 'restore_mana' in effects:
            self.restore_mana(effects['restore_mana'])
        if 'cure' in effects:
            for effect in effects['cure']:
                if isinstance(effect, str):
                    self.remove_status(StatusEffect(effect))
        if 'cure_all' in effects:
            self.status_effects.clear()
        if 'revive' in effects:
            if self.health <= 0:
                self.health = self.maxhealth * effects.get('heal_percent', 50) // 100
                if self.on_health_changed:
                    self.on_health_changed(self.health, self.maxhealth)
        
        self.remove_from_inventory(item_id, 1)
        return True
    
    def record_battle_result(self, won: bool, enemy_type: str, damage_dealt: int, damage_taken: int):
        self.completed_battles += 1
        self.total_damage_dealt += damage_dealt
        self.total_damage_taken += damage_taken
        if won:
            self.enemies_defeated[enemy_type] = self.enemies_defeated.get(enemy_type, 0) + 1
    
    def unlock_achievement(self, achievement_id: str):
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def get_stats_dict(self) -> Dict[str, Any]:
        effective = self.get_effective_stats()
        return {
            "name": self.name,
            "class": self.character_class,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "gold": self.gold,
            "hp": self.health,
            "max_hp": effective["maxhealth"],
            "mana": self.mana,
            "max_mana": effective["maxmana"],
            "attack": effective["attack"],
            "defense": effective["defense"],
            "accuracy": effective["accuracy"],
            "speed": effective["speed"],
            "crit_chance": effective["crit_chance"],
            "mana_regen": effective["mana_regen"],
            "stat_points": self.stat_points,
        }

Player.load_class_data()