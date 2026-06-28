import sys
import os
import json
from datetime import datetime

# Fix Qt platform plugin on macOS - MUST be before importing PySide6
if sys.platform == "darwin":
    os.environ.setdefault("QT_QPA_PLATFORM", "cocoa")
    # Set Qt plugin path for PySide6 in virtual environment
    import PySide6
    pyside6_path = os.path.dirname(PySide6.__file__)
    plugin_path = os.path.join(pyside6_path, "Qt", "plugins")
    if os.path.exists(plugin_path):
        os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", plugin_path)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFrame, QLabel, QGraphicsDropShadowEffect, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QColor, QFont, QPixmap, QPainter, QBrush, QPen, QPolygon

from entities.player import Player
from entities.enemy import Enemy
from engine.battle import Battle, BattleState, BattleResult
from ui.styles import get_stylesheet
from ui.screens import BattleScreen, ProfileSelectScreen, ClassSelectScreen, InventoryScreen, ShopScreen, SettingsScreen, LevelUpScreen
from ui.widgets import CombatLog, FloatingText, ActionButton
from save.save_manager import SaveManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adaptive RPG Battle")
        self.setMinimumSize(1280, 800)
        self.resize(1400, 850)
        
        self.save_manager = SaveManager()
        self.config = self._load_config()
        
        self.battle: Battle = None
        self.player: Player = None
        self.enemy: Enemy = None
        self.current_enemy_type = "goblin"
        self.pending_level_up = None
        
        self._setup_ui()
        self._apply_styles()
        self._create_portraits()
        
        self._apply_config()
    
    def _load_config(self) -> dict:
        config_path = "config.json"
        default_config = {
            'music_volume': 0.7,
            'sfx_volume': 0.8,
            'fullscreen': False,
            'animations': True,
            'particles': True,
            'autosave': True,
            'detailed_log': True,
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass
        return default_config
    
    def _save_config(self):
        config_path = "config.json"
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def _apply_config(self):
        if self.config.get('fullscreen', False):
            self.showFullScreen()
        else:
            self.showNormal()
    
    def _setup_ui(self):
        self.central = QStackedWidget()
        self.setCentralWidget(self.central)
        
        self.profile_screen = ProfileSelectScreen()
        self.profile_screen.profile_selected.connect(self._on_profile_selected)
        self.profile_screen.new_profile_requested.connect(self._on_new_profile)
        self.central.addWidget(self.profile_screen)
        
        self.class_screen = ClassSelectScreen()
        self.class_screen.class_selected.connect(self._on_class_selected)
        self.class_screen.back_requested.connect(self._show_profile_screen)
        self.central.addWidget(self.class_screen)
        
        self.battle_screen = BattleScreen()
        self.central.addWidget(self.battle_screen)
        
        self.inventory_screen = None
        self.shop_screen = None
        self.settings_screen = None
        self.level_up_screen = None
        
        self.central.setCurrentWidget(self.profile_screen)
    
    def _apply_styles(self):
        self.setStyleSheet(get_stylesheet())
    
    def _create_portraits(self):
        self.portraits = {}
        enemy_types = ["goblin", "wolf", "skeleton", "orc", "bandit", "mage", "knight", "dragon", "slime", "spider", "necromancer", "golem", "wraith", "demon"]
        
        for etype in enemy_types:
            pixmap = self._generate_portrait(etype)
            self.portraits[etype] = pixmap
        
        player_pixmap = self._generate_portrait("player")
        self.portraits["player"] = player_pixmap
    
    def _generate_portrait(self, etype: str):
        size = 120
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        colors = {
            "goblin": (QColor("#22c55e"), QColor("#16a34a")),
            "wolf": (QColor("#78716c"), QColor("#57534e")),
            "skeleton": (QColor("#f5f5f4"), QColor("#e7e5e4")),
            "orc": (QColor("#65a30d"), QColor("#4d7c0f")),
            "bandit": (QColor("#78716c"), QColor("#57534e")),
            "mage": (QColor("#a855f7"), QColor("#9333ea")),
            "knight": (QColor("#9ca3af"), QColor("#71717a")),
            "dragon": (QColor("#f97316"), QColor("#ea580c")),
            "slime": (QColor("#22c55e"), QColor("#16a34a")),
            "spider": (QColor("#3f3f46"), QColor("#1f2937")),
            "necromancer": (QColor("#a855f7"), QColor("#9333ea")),
            "golem": (QColor("#78716c"), QColor("#57534e")),
            "wraith": (QColor("#60a5fa"), QColor("#3b82f6")),
            "demon": (QColor("#ef4444"), QColor("#dc2626")),
            "player": (QColor("#3b82f6"), QColor("#2563eb")),
        }
        
        c1, c2 = colors.get(etype, (QColor("#5a4fff"), QColor("#a855f7")))
        
        painter.setBrush(QBrush(c1))
        painter.setPen(QPen(c2, 3))
        painter.drawEllipse(10, 10, size - 20, size - 20)
        
        if etype == "goblin":
            painter.setBrush(QColor("#166534"))
            painter.drawEllipse(30, 40, 15, 15)
            painter.drawEllipse(75, 40, 15, 15)
            painter.setBrush(QColor("#dc2626"))
            painter.drawEllipse(52, 70, 16, 8)
        elif etype == "wolf":
            painter.setBrush(QColor("#3f3f46"))
            painter.drawEllipse(25, 30, 20, 15)
            painter.drawEllipse(75, 30, 20, 15)
            painter.setBrush(QColor("#ef4444"))
            painter.drawEllipse(40, 33, 8, 8)
            painter.drawEllipse(90, 33, 8, 8)
            painter.setBrush(QColor("#fbbf24"))
            painter.drawEllipse(50, 70, 20, 12)
        elif etype == "dragon":
            painter.setBrush(QColor("#9a3412"))
            painter.drawEllipse(20, 30, 35, 35)
            painter.drawEllipse(65, 30, 35, 35)
            painter.setBrush(QColor("#fbbf24"))
            painter.drawEllipse(35, 35, 12, 12)
            painter.drawEllipse(80, 35, 12, 12)
            painter.setBrush(QColor("#dc2626"))
            polygon = QPolygon([QPoint(45, 55), QPoint(52, 68), QPoint(38, 68),
                                QPoint(55, 55), QPoint(62, 68), QPoint(48, 68)])
            painter.drawPolygon(polygon)
        elif etype == "player":
            painter.setBrush(QColor("#1e3a8a"))
            painter.drawEllipse(35, 25, 50, 50)
            painter.setBrush(QColor("#60a5fa"))
            painter.drawEllipse(42, 32, 12, 12)
            painter.drawEllipse(66, 32, 12, 12)
            painter.setBrush(QColor("#fbbf24"))
            polygon = QPolygon([QPoint(50, 55), QPoint(60, 65), QPoint(40, 65)])
            painter.drawPolygon(polygon)
        
        painter.end()
        return pixmap
    
    def _show_profile_screen(self):
        self.profile_screen = ProfileSelectScreen()
        self.profile_screen.profile_selected.connect(self._on_profile_selected)
        self.profile_screen.new_profile_requested.connect(self._on_new_profile)
        self.central.addWidget(self.profile_screen)
        self.central.setCurrentWidget(self.profile_screen)
    
    def _on_profile_selected(self, profile_id: str):
        profile = self.save_manager.load_profile(profile_id)
        if not profile:
            return
        
        self.player = Player.create_from_class(profile.name, profile.character_class, profile.profile_id)
        self.save_manager.apply_to_player(profile, self.player)
        
        self._start_battle()
    
    def _on_new_profile(self):
        self.class_screen.name_input.clear()
        self.central.setCurrentWidget(self.class_screen)
    
    def _on_class_selected(self, class_id: str, name: str):
        self.player = Player.create_from_class(name, class_id)
        self._start_battle()
    
    def _start_battle(self):
        self.enemy = Enemy.create_random(player_level=self.player.level)
        self.current_enemy_type = self.enemy.enemy_type
        
        self.battle = Battle(self.player, self.enemy)
        self._connect_battle()
        
        if self.inventory_screen:
            self.central.removeWidget(self.inventory_screen)
        self.inventory_screen = InventoryScreen(self.player)
        self.inventory_screen.closed.connect(self._close_inventory)
        self.inventory_screen.item_used.connect(self._on_item_used)
        self.inventory_screen.item_equipped.connect(self._on_item_equipped)
        self.inventory_screen.item_unequipped.connect(self._on_item_unequipped)
        self.central.addWidget(self.inventory_screen)
        
        if self.shop_screen:
            self.central.removeWidget(self.shop_screen)
        self.shop_screen = ShopScreen(self.player)
        self.shop_screen.closed.connect(self._close_shop)
        self.shop_screen.item_bought.connect(self._on_item_bought)
        self.shop_screen.item_sold.connect(self._on_item_sold)
        self.central.addWidget(self.shop_screen)
        
        if self.settings_screen:
            self.central.removeWidget(self.settings_screen)
        self.settings_screen = SettingsScreen(self.config)
        self.settings_screen.closed.connect(self._close_settings)
        self.settings_screen.settings_changed.connect(self._on_settings_changed)
        self.central.addWidget(self.settings_screen)
        
        self.battle_screen.setup_battle(self.battle, self.player, self.enemy)
        self.central.setCurrentWidget(self.battle_screen)
        
        self.battle.start_battle()
    
    def _connect_battle(self):
        self.battle.on_log_message = self._on_log_message
        self.battle.on_player_attack = self._on_player_attack
        self.battle.on_enemy_attack = self._on_enemy_attack
        self.battle.on_player_heal = self._on_player_heal
        self.battle.on_player_defend = self._on_player_defend
        self.battle.on_enemy_ai_message = self._on_enemy_ai_message
        self.battle.on_battle_end = self._on_battle_end
        self.battle.on_state_change = self._on_state_change
        self.battle.on_turn_change = self._on_turn_change
        self.battle.on_mana_regen = self._on_mana_regen

        self.player.on_health_changed = self._on_player_health_changed
        self.player.on_mana_changed = self._on_player_mana_changed
        self.player.on_damage_taken = self._on_player_damage_taken
        self.player.on_heal = self._on_player_heal_effect
        self.player.on_crit = self._on_player_crit
        self.player.on_level_up = self._on_player_level_up
        self.player.on_gold_changed = self._on_gold_changed
        self.player.on_mana_regen = self._on_player_mana_regen

        self.enemy.on_health_changed = self._on_enemy_health_changed
        self.enemy.on_damage_taken = self._on_enemy_damage_taken
        self.enemy.on_death = self._on_enemy_death
        self.enemy.on_phase_change = self._on_enemy_phase_change
    
    def _on_log_message(self, message: str, msg_type: str):
        self.battle_screen.combat_log.add_message(message, msg_type)
    
    def _on_player_attack(self, damage: int, is_crit: bool, is_miss: bool):
        self.battle_screen.show_damage(self.enemy, damage, is_crit, is_miss)
        self._update_panels()
    
    def _on_enemy_attack(self, damage: int, is_crit: bool, is_miss: bool):
        self.battle_screen.show_damage(self.player, damage, is_crit, is_miss, is_enemy=True)
        self._update_panels()
    
    def _on_player_heal(self, amount: int):
        self.battle_screen.show_heal(self.player, amount)
        self._update_panels()
    
    def _on_player_defend(self):
        self.battle_screen.show_defend(self.player)
    
    def _on_enemy_ai_message(self, message: str):
        self.battle_screen.show_ai_message(message)
    
    def _on_battle_end(self, result: BattleResult):
        QTimer.singleShot(1500, lambda: self._show_game_over(result))
    
    def _on_state_change(self, state: BattleState):
        self.battle_screen.on_state_change(state)
    
    def _on_turn_change(self, is_player_turn: bool):
        self.battle_screen.on_turn_change(is_player_turn)
    
    def _on_mana_regen(self, amount: int):
        pass
    
    def _on_player_health_changed(self, current: int, max_hp: int):
        self.battle_screen.player_panel.update_stats(self.player.get_stats_dict())
    
    def _on_player_mana_changed(self, current: int, max_mana: int):
        self.battle_screen.player_panel.update_stats(self.player.get_stats_dict())
    
    def _on_player_damage_taken(self, damage: int, is_crit: bool, is_miss: bool):
        pass
    
    def _on_player_heal_effect(self, amount: int):
        pass
    
    def _on_player_crit(self, damage: int):
        pass
    
    def _on_player_level_up(self, level: int):
        self._show_level_up()
    
    def _on_gold_changed(self, gold: int):
        if self.inventory_screen:
            self.inventory_screen.gold_label.setText(f"{gold} 💰")
        if self.shop_screen:
            self.shop_screen.gold_label.setText(f"{gold} 💰")
    
    def _on_player_mana_regen(self, amount: int):
        pass
    
    def _on_enemy_health_changed(self, current: int, max_hp: int):
        self.battle_screen.enemy_panel.update_stats(self.enemy.get_stats_dict())
    
    def _on_enemy_damage_taken(self, damage: int, is_crit: bool, is_miss: bool):
        pass
    
    def _on_enemy_death(self):
        pass
    
    def _on_enemy_phase_change(self, phase_name: str):
        self.battle_screen.show_ai_message(f"Enemy enters {phase_name}!")
    
    def _update_panels(self):
        self.battle_screen.player_panel.update_stats(self.player.get_stats_dict())
        self.battle_screen.enemy_panel.update_stats(self.enemy.get_stats_dict())
    
    def _show_game_over(self, result: BattleResult):
        won = result == BattleResult.PLAYER_WIN
        xp_gained = self.enemy.xp_reward if won else 0
        gold_gained = self.enemy.gold_reward if won else 0
        
        if won:
            self.player.add_gold(gold_gained)
            self.player.gain_xp(xp_gained)
        
        self.player.record_battle_result(won, self.enemy.enemy_type, 
                                       self.battle.damage_dealt_this_battle,
                                       self.battle.damage_taken_this_battle)
        
        if self.config.get('autosave', True):
            profile = self.save_manager.extract_from_player(self.player)
            self.save_manager.save_profile(profile)
        
        if self.game_over_screen:
            self.central.removeWidget(self.game_over_screen)
        from ui.widgets import GameOverScreen
        self.game_over_screen = GameOverScreen()
        self.game_over_screen.restart_requested.connect(self._on_restart)
        self.game_over_screen.menu_requested.connect(self._on_menu)
        self.central.addWidget(self.game_over_screen)
        
        self.game_over_screen.show_result(won, self.player.get_stats_dict(), self.enemy.get_stats_dict(), xp_gained, gold_gained)
        self.central.setCurrentWidget(self.game_over_screen)
    
    def _show_level_up(self):
        if self.level_up_screen:
            self.central.removeWidget(self.level_up_screen)
        self.level_up_screen = LevelUpScreen(self.player)
        self.level_up_screen.confirmed.connect(self._on_level_up_confirmed)
        self.level_up_screen.cancelled.connect(self._on_level_up_cancelled)
        self.central.addWidget(self.level_up_screen)
        self.central.setCurrentWidget(self.level_up_screen)
    
    def _on_level_up_confirmed(self, allocations: dict):
        if self.level_up_screen:
            self.central.removeWidget(self.level_up_screen)
            self.level_up_screen = None
        self.central.setCurrentWidget(self.battle_screen)
        self._update_panels()
    
    def _on_level_up_cancelled(self):
        if self.level_up_screen:
            self.central.removeWidget(self.level_up_screen)
            self.level_up_screen = None
        self.central.setCurrentWidget(self.battle_screen)
        self._update_panels()
    
    def _on_restart(self):
        self._start_battle()
    
    def _on_menu(self):
        self._show_profile_screen()
    
    def _on_item_used(self, item_id: str):
        pass
    
    def _on_item_equipped(self, item_id: str):
        self._update_panels()
    
    def _on_item_unequipped(self, item_id: str):
        self._update_panels()
    
    def _on_item_bought(self, item_id: str):
        pass
    
    def _on_item_sold(self, item_id: str):
        pass
    
    def _close_inventory(self):
        self.central.setCurrentWidget(self.battle_screen)
    
    def _close_shop(self):
        self.central.setCurrentWidget(self.battle_screen)
    
    def _close_settings(self):
        self.central.setCurrentWidget(self.battle_screen)
    
    def _on_settings_changed(self, config: dict):
        self.config = config
        self._save_config()
        self._apply_config()
    
    def open_inventory(self):
        if self.inventory_screen:
            self.inventory_screen._load_items()
            self.inventory_screen.gold_label.setText(f"{self.player.gold} 💰")
            self.central.setCurrentWidget(self.inventory_screen)
    
    def open_shop(self):
        if self.shop_screen:
            self.shop_screen._load_shop()
            self.shop_screen.gold_label.setText(f"{self.player.gold} 💰")
            self.central.setCurrentWidget(self.shop_screen)
    
    def open_settings(self):
        if self.settings_screen:
            self.central.setCurrentWidget(self.settings_screen)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()