from dataclasses import dataclass
from typing import Callable, Optional, List, Dict, Any
from enum import Enum
import random
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


class Enemy:
    ENEMY_DATA = {}
    
    def __init__(self, enemy_type: str = "goblin", level: int = 1):
        if not Enemy.ENEMY_DATA:
            Enemy.load_enemy_data()
        
        template = Enemy.ENEMY_DATA.get(enemy_type, Enemy.ENEMY_DATA.get("goblin", {})).copy()
        
        self.enemy_type = enemy_type
        self.name = template.get("name", "Unknown")
        self.description = template.get("description", "")
        self.portrait = template.get("portrait", enemy_type)
        self.dialogue = template.get("dialogue", {})
        
        base_stats = template.get("base_stats", {})
        self.base_maxhealth = base_stats.get("maxhealth", 50)
        self.base_attack = base_stats.get("attack", 8)
        self.base_defense = base_stats.get("defense", 3)
        self.base_mana = base_stats.get("mana", 30)
        self.base_accuracy = base_stats.get("accuracy", 85)
        self.base_speed = base_stats.get("speed", 10)
        self.base_crit_chance = base_stats.get("crit_chance", 5)
        
        self.level = template.get("level", level)
        self.xp_reward = template.get("xp_reward", 25)
        self.gold_reward = template.get("gold_reward", 10)
        self.ai_profile = template.get("ai_profile", "aggressive")
        self.skills = template.get("skills", ["basic_attack"])
        self.loot_table = template.get("loot_table", [])
        self.phases = template.get("phases", [])
        self.current_phase = 0
        
        self._apply_level_scaling(level)
        
        self.maxhealth = self.base_maxhealth
        self.health = self.maxhealth
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.mana = self.base_mana
        self.maxmana = self.base_mana
        self.accuracy = self.base_accuracy
        self.speed = self.base_speed
        self.crit_chance = self.base_crit_chance
        
        self.status_effects: List[ActiveEffect] = []
        
        self.on_health_changed: Optional[Callable[[int, int], None]] = None
        self.on_mana_changed: Optional[Callable[[int, int], None]] = None
        self.on_damage_taken: Optional[Callable[[int, bool, bool], None]] = None
        self.on_heal: Optional[Callable[[int], None]] = None
        self.on_crit: Optional[Callable[[int], None]] = None
        self.on_status_applied: Optional[Callable[[StatusEffect, int], None]] = None
        self.on_status_removed: Optional[Callable[[StatusEffect], None]] = None
        self.on_death: Optional[Callable[[], None]] = None
        self.on_phase_change: Optional[Callable[[str], None]] = None
        self.on_ai_message: Optional[Callable[[str], None]] = None
    
    @classmethod
    def load_enemy_data(cls):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'enemies.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)
                cls.ENEMY_DATA = data.get('enemies', {})
    
    def _apply_level_scaling(self, level: int):
        if level > 1:
            multiplier = 1 + (level - 1) * 0.15
            self.base_maxhealth = int(self.base_maxhealth * multiplier)
            self.base_attack = int(self.base_attack * multiplier)
            self.base_defense = int(self.base_defense * multiplier)
            self.base_mana = int(self.base_mana * multiplier)
            self.xp_reward = int(self.xp_reward * multiplier)
            self.gold_reward = int(self.gold_reward * multiplier)
    
    def take_damage(self, amount: int, is_crit: bool = False, is_miss: bool = False):
        if is_miss:
            if self.on_damage_taken:
                self.on_damage_taken(0, False, True)
            return
        
        actual_damage = max(0, amount)
        self.health = max(0, self.health - actual_damage)
        
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
            if self.on_health_changed:
                self.on_health_changed(self.health, self.maxhealth)
            if self.on_heal:
                self.on_heal(healed)
    
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
    
    def check_phase_change(self):
        if not self.phases:
            return
        hp_ratio = self.health / self.maxhealth
        for i, phase in enumerate(self.phases):
            if hp_ratio <= phase["threshold"] and i > self.current_phase:
                self.current_phase = i
                if "attack_bonus" in phase:
                    self.attack = self.base_attack + phase["attack_bonus"]
                if "crit_bonus" in phase:
                    self.crit_chance = self.base_crit_chance + phase["crit_bonus"]
                if "defense_bonus" in phase:
                    self.defense = self.base_defense + phase["defense_bonus"]
                if "speed_bonus" in phase:
                    self.speed = self.base_speed + phase["speed_bonus"]
                if "mana_bonus" in phase:
                    self.maxmana = self.base_mana + phase["mana_bonus"]
                if self.on_phase_change:
                    self.on_phase_change(phase["name"])
                if self.on_ai_message and "dialogue" in phase:
                    self.on_ai_message(phase.get("dialogue", f"Enemy enters {phase['name']}!"))
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def get_stats_dict(self) -> Dict[str, Any]:
        phase_name = ""
        if self.phases and self.current_phase < len(self.phases):
            phase_name = self.phases[self.current_phase]["name"]
        return {
            "name": self.name,
            "type": self.enemy_type,
            "hp": self.health,
            "max_hp": self.maxhealth,
            "mana": self.mana,
            "max_mana": self.maxmana,
            "attack": self.attack,
            "defense": self.defense,
            "accuracy": self.accuracy,
            "speed": self.speed,
            "crit_chance": self.crit_chance,
            "level": self.level,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "phase": phase_name,
            "ai_profile": self.ai_profile,
        }
    
    @classmethod
    def create_random(cls, player_level: int = 1):
        available = []
        for etype, data in cls.ENEMY_DATA.items():
            enemy_level = data.get("level", 1)
            if enemy_level <= player_level + 2:
                available.append(etype)
        if not available:
            available = ["goblin"]
        return cls(random.choice(available), level=player_level)
    
    @classmethod
    def create_boss(cls, boss_type: str, player_level: int = 1):
        return cls(boss_type, level=max(player_level, cls.ENEMY_DATA.get(boss_type, {}).get("level", 1)))

Enemy.load_enemy_data()