import json
import os
from typing import Callable, Optional, List, Dict, Any
from enum import Enum
import random

from entities.player import Player
from entities.enemy import Enemy


class BattleState(Enum):
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    ANIMATING = "animating"
    PLAYER_WON = "player_won"
    ENEMY_WON = "enemy_won"
    WAITING_ACTION = "waiting_action"


class BattleResult(Enum):
    PLAYER_WIN = "player_win"
    ENEMY_WIN = "enemy_win"
    ONGOING = "ongoing"


class Battle:
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.state = BattleState.WAITING_ACTION
        self.player.defending = False
        self.player_attack_count = 0
        self.player_heal_count = 0
        self.player_defend_count = 0
        
        self.damage_dealt_this_battle = 0
        self.damage_taken_this_battle = 0
        
        self.on_state_change: Optional[Callable[[BattleState], None]] = None
        self.on_log_message: Optional[Callable[[str, str], None]] = None
        self.on_player_attack: Optional[Callable[[int, bool, bool], None]] = None
        self.on_enemy_attack: Optional[Callable[[int, bool, bool], None]] = None
        self.on_player_heal: Optional[Callable[[int], None]] = None
        self.on_player_defend: Optional[Callable[[], None]] = None
        self.on_enemy_ai_message: Optional[Callable[[str], None]] = None
        self.on_battle_end: Optional[Callable[[BattleResult], None]] = None
        self.on_turn_change: Optional[Callable[[bool], None]] = None
        self.on_mana_regen: Optional[Callable[[int], None]] = None
        
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        self.player.on_health_changed = self._on_player_health_changed
        self.player.on_mana_changed = self._on_player_mana_changed
        self.player.on_damage_taken = self._on_player_damage_taken
        self.player.on_heal = self._on_player_heal_callback
        self.player.on_crit = self._on_player_crit
        self.player.on_status_applied = self._on_player_status_applied
        self.player.on_status_removed = self._on_player_status_removed
        self.player.on_level_up = self._on_player_level_up
        self.player.on_mana_regen = self._on_player_mana_regen
        
        self.enemy.on_health_changed = self._on_enemy_health_changed
        self.enemy.on_mana_changed = self._on_enemy_mana_changed
        self.enemy.on_damage_taken = self._on_enemy_damage_taken
        self.enemy.on_heal = self._on_enemy_heal
        self.enemy.on_crit = self._on_enemy_crit
        self.enemy.on_status_applied = self._on_enemy_status_applied
        self.enemy.on_status_removed = self._on_enemy_status_removed
        self.enemy.on_death = self._on_enemy_death
        self.enemy.on_phase_change = self._on_enemy_phase_change
        self.enemy.on_ai_message = self._on_enemy_ai_message
    
    def _on_player_health_changed(self, current: int, max_hp: int):
        pass
    
    def _on_player_mana_changed(self, current: int, max_mana: int):
        pass
    
    def _on_player_damage_taken(self, damage: int, is_crit: bool, is_miss: bool):
        self.damage_taken_this_battle += damage
        if self.on_enemy_attack:
            self.on_enemy_attack(damage, is_crit, is_miss)
    
    def _on_player_heal_callback(self, amount: int):
        if self.on_player_heal:
            self.on_player_heal(amount)
    
    def _on_player_crit(self, damage: int):
        pass
    
    def _on_player_status_applied(self, effect, duration: int):
        if self.on_log_message:
            self.on_log_message(f"{self.player.name} is afflicted by {effect.value}!", "status")
    
    def _on_player_status_removed(self, effect):
        if self.on_log_message:
            self.on_log_message(f"{self.player.name} recovered from {effect.value}.", "status")
    
    def _on_player_level_up(self, level: int):
        if self.on_log_message:
            self.on_log_message(f"Level up! {self.player.name} reached level {level}!", "levelup")
    
    def _on_player_mana_regen(self, amount: int):
        if self.on_mana_regen:
            self.on_mana_regen(amount)
    
    def _on_enemy_health_changed(self, current: int, max_hp: int):
        pass
    
    def _on_enemy_mana_changed(self, current: int, max_mana: int):
        pass
    
    def _on_enemy_damage_taken(self, damage: int, is_crit: bool, is_miss: bool):
        self.damage_dealt_this_battle += damage
        if self.on_player_attack:
            self.on_player_attack(damage, is_crit, is_miss)
    
    def _on_enemy_heal(self, amount: int):
        if self.on_log_message:
            self.on_log_message(f"{self.enemy.name} heals for {amount} HP.", "heal")
    
    def _on_enemy_crit(self, damage: int):
        pass
    
    def _on_enemy_status_applied(self, effect, duration: int):
        if self.on_log_message:
            self.on_log_message(f"{self.enemy.name} is afflicted by {effect.value}!", "status")
    
    def _on_enemy_status_removed(self, effect):
        if self.on_log_message:
            self.on_log_message(f"{self.enemy.name} recovered from {effect.value}.", "status")
    
    def _on_enemy_death(self):
        if self.on_log_message:
            self.on_log_message(f"{self.enemy.name} has been defeated! You win!", "victory")
        self._end_battle(BattleResult.PLAYER_WIN)
    
    def _on_enemy_phase_change(self, phase_name: str):
        if self.on_log_message:
            self.on_log_message(f"{self.enemy.name} enters {phase_name}!", "phase")
        if self.enemy.on_ai_message:
            self.enemy.on_ai_message(f"The {self.enemy.name} transforms into {phase_name}!")
    
    def _on_enemy_ai_message(self, message: str):
        if self.on_enemy_ai_message:
            self.on_enemy_ai_message(message)
    
    def _set_state(self, state: BattleState):
        self.state = state
        if self.on_state_change:
            self.on_state_change(state)
    
    def _log(self, message: str, msg_type: str = "info"):
        if self.on_log_message:
            self.on_log_message(message, msg_type)
    
    def _end_battle(self, result: BattleResult):
        self._set_state(BattleState.PLAYER_WON if result == BattleResult.PLAYER_WIN else BattleState.ENEMY_WON)
        if self.on_battle_end:
            self.on_battle_end(result)
    
    def player_attack(self):
        if self.state != BattleState.PLAYER_TURN and self.state != BattleState.WAITING_ACTION:
            return
        self._set_state(BattleState.ANIMATING)
        
        effective_stats = self.player.get_effective_stats()
        attack = random.randint(effective_stats["attack"] - 4, effective_stats["attack"] + 4)
        damage = attack - self.enemy.defense
        is_crit = random.random() < (effective_stats["crit_chance"] / 100)
        is_miss = random.random() > (effective_stats["accuracy"] / 100)
        
        if is_miss:
            damage = 0
            self._log(f"{self.player.name} attacks but misses!", "miss")
        else:
            if damage < 0:
                damage = 0
            if is_crit:
                damage *= 2
                self._log(f"Critical hit! {self.player.name} deals double damage!", "crit")
            self._log(f"{self.player.name} attacks {self.enemy.name} for {damage} damage!", "attack")
        
        self.enemy.take_damage(damage, is_crit, is_miss)
        self.player_attack_count += 1
        
        if not self.enemy.is_alive():
            self._end_battle(BattleResult.PLAYER_WIN)
            return
        
        self._set_state(BattleState.ENEMY_TURN)
        self._enemy_turn()
    
    def player_heal(self):
        if self.state != BattleState.PLAYER_TURN and self.state != BattleState.WAITING_ACTION:
            return
        self._set_state(BattleState.ANIMATING)
        
        heal_amount = 20
        heal_cost = 25
        
        if self.player.health >= self.player.maxhealth:
            self._log("Health is already full!", "info")
            self._set_state(BattleState.WAITING_ACTION)
            return
        
        if self.player.mana < heal_cost:
            self._log("Not enough mana to heal!", "info")
            self._set_state(BattleState.WAITING_ACTION)
            return
        
        self.player.mana -= heal_cost
        if self.player.on_mana_changed:
            self.player.on_mana_changed(self.player.mana, self.player.maxmana)
        
        self.player.heal(heal_amount)
        self.player_heal_count += 1
        
        if self.on_player_heal:
            self.on_player_heal(heal_amount)
        
        if not self.enemy.is_alive():
            self._end_battle(BattleResult.PLAYER_WIN)
            return
        
        self._set_state(BattleState.ENEMY_TURN)
        self._enemy_turn()
    
    def player_defend(self):
        if self.state != BattleState.PLAYER_TURN and self.state != BattleState.WAITING_ACTION:
            return
        self._set_state(BattleState.ANIMATING)
        
        defense_cost = 15
        
        if self.player.mana < defense_cost:
            self._log("Not enough mana to defend!", "info")
            self._set_state(BattleState.WAITING_ACTION)
            return
        
        self.player.mana -= defense_cost
        if self.player.on_mana_changed:
            self.player.on_mana_changed(self.player.mana, self.player.maxmana)
        
        self.player.defending = True
        self.player_defend_count += 1
        
        self._log(f"{self.player.name} takes a defensive stance!", "defend")
        
        if self.on_player_defend:
            self.on_player_defend()
        
        if not self.enemy.is_alive():
            self._end_battle(BattleResult.PLAYER_WIN)
            return
        
        self._set_state(BattleState.ENEMY_TURN)
        self._enemy_turn()
    
    def player_use_item(self, item_id: str):
        if self.state != BattleState.PLAYER_TURN and self.state != BattleState.WAITING_ACTION:
            return
        self._set_state(BattleState.ANIMATING)
        
        success = self.player.use_consumable(item_id)
        if success:
            self._log(f"{self.player.name} used {item_id}!", "heal")
        
        if not self.enemy.is_alive():
            self._end_battle(BattleResult.PLAYER_WIN)
            return
        
        self._set_state(BattleState.ENEMY_TURN)
        self._enemy_turn()
    
    def _enemy_turn(self):
        self.enemy.check_phase_change()
        self.enemy.process_status_effects()
        
        if not self.enemy.is_alive():
            self._end_battle(BattleResult.PLAYER_WIN)
            return
        
        if self.player_defend_count > 2:
            self._trigger_ai_message("Enemy adapts to defense!")
        
        attack = self._calculate_enemy_attack()
        
        is_crit = random.random() < (self.enemy.crit_chance / 100)
        is_miss = random.random() > (self.enemy.accuracy / 100)
        
        if is_miss:
            damage = 0
            self._log(f"{self.enemy.name} attacks but misses!", "miss")
        else:
            damage = attack - self.player.defense
            if damage < 0:
                damage = 0
            
            if is_crit:
                damage *= 2
                self._log("Enemy CRITICAL HIT!", "crit")
            
            if self.player.defending:
                damage //= 2
                self._log(f"{self.player.name} blocks the attack! Damage reduced!", "defend")
            
            self._log(f"{self.enemy.name} attacks {self.player.name} for {damage} damage!", "enemy_attack")
        
        self.player.take_damage(damage, is_crit, is_miss)
        self.player.defending = False
        
        if not self.player.is_alive():
            self._log(f"{self.player.name} has been defeated! Game Over.", "defeat")
            self._end_battle(BattleResult.ENEMY_WIN)
            return
        
        self.player.regenerate_mana()
        
        self._set_state(BattleState.WAITING_ACTION)
        if self.on_turn_change:
            self.on_turn_change(True)
    
    def _calculate_enemy_attack(self) -> int:
        base_attack = self.enemy.attack
        ai_profile = self.enemy.ai_profile
        
        if ai_profile == "aggressive":
            if self.player_heal_count > self.player_attack_count:
                self._trigger_ai_message("Enemy notices healing pattern!")
                return random.randint(base_attack, base_attack + 8)
            elif self.player_defend_count > 2:
                self._trigger_ai_message("Enemy adapts to defense!")
                return random.randint(base_attack + 3, base_attack + 8)
            else:
                return random.randint(base_attack - 2, base_attack + 6)
        
        elif ai_profile == "defensive":
            if self.player_defend_count > 1:
                self._trigger_ai_message("Enemy waits for an opening...")
                return random.randint(base_attack - 3, base_attack + 2)
            elif self.player_heal_count > self.player_attack_count:
                self._trigger_ai_message("Enemy prepares a crushing blow!")
                return random.randint(base_attack + 2, base_attack + 7)
            else:
                return random.randint(base_attack - 4, base_attack + 4)
        
        elif ai_profile == "tactical":
            if self.player_attack_count > 5:
                self._trigger_ai_message("Enemy raises its guard!")
                self.enemy.defense += 2
            if self.player_heal_count > 2:
                self._trigger_ai_message("Enemy predicts your healing!")
                return random.randint(base_attack, base_attack + 8)
            return random.randint(base_attack - 2, base_attack + 5)
        
        elif ai_profile == "caster":
            if self.enemy.mana >= 30 and random.random() < 0.3:
                self._trigger_ai_message("Enemy channels a spell!")
                return random.randint(base_attack + 5, base_attack + 12)
            return random.randint(base_attack - 4, base_attack + 4)
        
        elif ai_profile == "predator":
            if self.player.health < self.player.maxhealth * 0.3:
                self._trigger_ai_message("Enemy smells blood!")
                return random.randint(base_attack + 5, base_attack + 10)
            return random.randint(base_attack - 2, base_attack + 6)
        
        elif ai_profile == "summoner":
            if self.enemy.mana >= 40 and random.random() < 0.25:
                self._trigger_ai_message("Enemy summons a minion!")
                return 0
            return random.randint(base_attack - 3, base_attack + 5)
        
        elif ai_profile == "boss":
            if self.enemy.current_phase >= 2:
                if random.random() < 0.3:
                    self._trigger_ai_message("The boss unleashes a devastating attack!")
                    return random.randint(base_attack + 10, base_attack + 20)
            return random.randint(base_attack - 2, base_attack + 8)
        
        else:
            if self.player_heal_count > self.player_attack_count:
                self._trigger_ai_message("Enemy notices healing pattern!")
                return random.randint(base_attack, base_attack + 6)
            elif self.player_defend_count > 2:
                self._trigger_ai_message("Enemy adapts to defense!")
                return random.randint(base_attack + 2, base_attack + 5)
            else:
                return random.randint(base_attack - 4, base_attack + 4)
    
    def _trigger_ai_message(self, message: str):
        if self.on_enemy_ai_message:
            self.on_enemy_ai_message(message)
        self._log(message, "ai")
    
    def start_battle(self):
        self._log(f"A wild {self.enemy.name} appears!", "battle_start")
        if self.enemy.dialogue and "intro" in self.enemy.dialogue:
            self._log(self.enemy.dialogue["intro"], "battle_start")
        self._set_state(BattleState.WAITING_ACTION)
        if self.on_turn_change:
            self.on_turn_change(True)
    
    def get_battle_state(self) -> dict:
        return {
            "player": self.player.get_stats_dict(),
            "enemy": self.enemy.get_stats_dict(),
            "state": self.state.value,
            "player_turn": self.state in (BattleState.PLAYER_TURN, BattleState.WAITING_ACTION),
        }