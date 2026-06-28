from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QScrollArea, QSizePolicy,
    QGridLayout, QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
    QSlider, QCheckBox, QComboBox, QLineEdit, QApplication
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor, QPixmap

from ui.styles import get_stylesheet
from ui.widgets import CharacterStatsPanel, CombatLog, FloatingText, ActionButton


class BattleScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.battle = None
        self.player = None
        self.enemy = None
        self._setup_ui()
        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet(get_stylesheet())

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(16)
        left_layout.setAlignment(Qt.AlignTop)

        self.enemy_panel = CharacterStatsPanel(is_player=False)
        left_layout.addWidget(self.enemy_panel)

        self.ai_message = QLabel()
        self.ai_message.setObjectName("aiMessageLabel")
        self.ai_message.setAlignment(Qt.AlignCenter)
        self.ai_message.setWordWrap(True)
        self.ai_message.setVisible(False)
        left_layout.addWidget(self.ai_message)

        left_layout.addStretch()

        center_layout = QVBoxLayout()
        center_layout.setSpacing(16)

        self.arena = QFrame()
        self.arena.setObjectName("arenaPanel")
        self.arena.setMinimumSize(400, 300)
        
        arena_layout = QVBoxLayout(self.arena)
        arena_layout.setContentsMargins(20, 20, 20, 20)
        
        self.floating_container = QWidget()
        self.floating_container.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        arena_layout.addWidget(self.floating_container)
        
        center_layout.addWidget(self.arena)

        self.player_panel = CharacterStatsPanel(is_player=True)
        center_layout.addWidget(self.player_panel, alignment=Qt.AlignBottom)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(16)

        self.action_panel = QFrame()
        self.action_panel.setObjectName("actionPanel")
        self.action_panel.setFixedWidth(320)
        
        action_layout = QVBoxLayout(self.action_panel)
        action_layout.setContentsMargins(16, 16, 16, 16)
        action_layout.setSpacing(12)

        action_title = QLabel("ACTIONS")
        action_title.setObjectName("sectionTitle")
        action_title.setAlignment(Qt.AlignCenter)
        action_layout.addWidget(action_title)

        self.attack_btn = ActionButton("ATTACK", "Deal damage", "attack", self._on_attack)
        self.heal_btn = ActionButton("HEAL", "Restore 20 HP (25 MP)", "heal", self._on_heal)
        self.defend_btn = ActionButton("DEFEND", "Block 50% dmg (15 MP)", "defend", self._on_defend)
        
        action_layout.addWidget(self.attack_btn)
        action_layout.addWidget(self.heal_btn)
        action_layout.addWidget(self.defend_btn)

        right_layout.addWidget(self.action_panel)

        self.combat_log = CombatLog()
        right_layout.addWidget(self.combat_log)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(center_layout, 2)
        main_layout.addLayout(right_layout, 1)

    def setup_battle(self, battle, player, enemy):
        self.battle = battle
        self.player = player
        self.enemy = enemy
        
        self.enemy_panel.update_stats(enemy.get_stats_dict())
        self.player_panel.update_stats(player.get_stats_dict())

    def on_state_change(self, state):
        is_player_turn = state.value in ("player_turn", "waiting_action")
        self.attack_btn.setEnabled(is_player_turn)
        self.heal_btn.setEnabled(is_player_turn)
        self.defend_btn.setEnabled(is_player_turn)

    def on_turn_change(self, is_player_turn: bool):
        pass

    def _on_attack(self):
        if self.battle:
            self.battle.player_attack()

    def _on_heal(self):
        if self.battle:
            self.battle.player_heal()

    def _on_defend(self):
        if self.battle:
            self.battle.player_defend()

    def show_ai_message(self, message: str):
        self.ai_message.setText(message)
        self.ai_message.setVisible(True)
        QTimer.singleShot(3000, lambda: self.ai_message.setVisible(False))

    def show_damage(self, target, damage: int, is_crit: bool, is_miss: bool, is_enemy: bool = False):
        if is_miss:
            text = "MISS"
            color = "#9ca3af"
        elif is_crit:
            text = f"CRIT {damage}!"
            color = "#fbbf24"
        else:
            text = str(damage)
            color = "#f87171" if not is_enemy else "#fca5a5"

        floating = FloatingText(text, color, self.floating_container, is_crit=is_crit, is_miss=is_miss)
        
        container_rect = self.floating_container.rect()
        
        if is_enemy:
            start_x = container_rect.width() // 2
            start_y = container_rect.height() // 2 + 40
        else:
            start_x = container_rect.width() // 2
            start_y = container_rect.height() // 2 - 40
        
        end_x = start_x
        end_y = start_y - 100

        start_rect = QRect(start_x - 60, start_y, 120, 50)
        end_rect = QRect(end_x - 60, end_y, 120, 50)
        
        floating.setGeometry(start_rect)
        floating.animate(start_rect, end_rect)

        if is_crit:
            self._screen_shake()
        
        if is_enemy:
            self._flash_widget(self.enemy_panel, "#f87171")
        else:
            self._flash_widget(self.player_panel, "#f87171")

    def show_heal(self, target, amount: int):
        floating = FloatingText(f"+{amount}", "#4ade80", self.floating_container)
        
        container_rect = self.floating_container.rect()
        start_x = container_rect.width() // 2
        start_y = container_rect.height() // 2 + 40
        end_x = start_x
        end_y = start_y - 100

        start_rect = QRect(start_x - 60, start_y, 120, 50)
        end_rect = QRect(end_x - 60, end_y, 120, 50)
        
        floating.setGeometry(start_rect)
        floating.animate(start_rect, end_rect)
        
        self._flash_widget(self.player_panel, "#4ade80", 800)

    def show_defend(self, target):
        floating = FloatingText("GUARD", "#60a5fa", self.floating_container)
        
        container_rect = self.floating_container.rect()
        start_x = container_rect.width() // 2
        start_y = container_rect.height() // 2 + 40
        end_x = start_x
        end_y = start_y - 80

        start_rect = QRect(start_x - 60, start_y, 120, 50)
        end_rect = QRect(end_x - 60, end_y, 120, 50)
        
        floating.setGeometry(start_rect)
        floating.animate(start_rect, end_rect)
        
        self._flash_widget(self.player_panel, "#60a5fa", 800)

    def _flash_widget(self, widget: QWidget, color: str, duration: int = 300):
        original_style = widget.styleSheet()
        flash_style = f"""
            {original_style}
            border: 3px solid {color};
        """
        widget.setStyleSheet(flash_style)
        QTimer.singleShot(duration, lambda: widget.setStyleSheet(original_style))

    def _screen_shake(self):
        anim = QPropertyAnimation(self.arena, b"pos")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        
        original_pos = self.arena.pos()
        shake_offsets = [(8, 0), (-8, 0), (6, 0), (-6, 0), (4, 0), (-4, 0), (0, 0)]
        
        def do_shake(index=0):
            if index < len(shake_offsets):
                dx, dy = shake_offsets[index]
                anim.setStartValue(original_pos)
                anim.setEndValue(QRect(original_pos.x() + dx, original_pos.y() + dy, 
                                       self.arena.width(), self.arena.height()).topLeft())
                anim.start()
                QTimer.singleShot(50, lambda: do_shake(index + 1))
            else:
                self.arena.move(original_pos)
        
        do_shake()


class ClassCard(QFrame):
    selected = Signal(str)
    
    def __init__(self, class_id: str, class_data: dict):
        super().__init__()
        self.class_id = class_id
        self.class_data = class_data
        self.setFixedSize(220, 360)
        self.setCursor(Qt.PointingHandCursor)
        self._selected = False
        self._setup_ui()
    
    def _setup_ui(self):
        color = self.class_data.get('color', '#9ca3af')
        glow = self.class_data.get('glow_color', color)
        
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 26, 62, 220), stop:1 rgba(13, 13, 43, 240));
                border: 2px solid rgba(90, 79, 255, 0.3);
                border-radius: 16px;
            }}
            QFrame:hover {{
                border: 2px solid {color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 30, 70, 230), stop:1 rgba(18, 18, 50, 250));
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setFixedSize(100, 100)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            background: qradialgradient(cx:0.5, cy:0.5, radius:1,
                fx:0.5, fy:0.5, stop:0 {color}40, stop:1 transparent);
            border-radius: 50px;
            border: 2px solid {color}80;
        """)
        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        
        name = QLabel(self.class_data.get('name', 'Unknown'))
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: 700;")
        layout.addWidget(name)
        
        desc = QLabel(self.class_data.get('description', ''))
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #d1d5db; font-size: 12px; line-height: 1.5;")
        layout.addWidget(desc)
        
        layout.addStretch()
        
        stats = self.class_data.get('primary_stats', {})
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(4)
        
        stat_items = [
            ("HP", stats.get('maxhealth', 100)),
            ("ATK", stats.get('attack', 10)),
            ("DEF", stats.get('defense', 5)),
            ("MP", stats.get('mana', 50)),
            ("SPD", stats.get('speed', 10)),
            ("CRIT", f"{stats.get('crit_chance', 5)}%"),
        ]
        
        for label, value in stat_items:
            row = QHBoxLayout()
            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: #9ca3af; font-size: 11px; font-weight: 600; min-width: 40px;")
            stat_value = QLabel(str(value))
            stat_value.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 700;")
            stat_value.setAlignment(Qt.AlignRight)
            row.addWidget(stat_label)
            row.addStretch()
            row.addWidget(stat_value)
            stats_layout.addLayout(row)
        
        layout.addLayout(stats_layout)
        
        select_btn = QPushButton("SELECT")
        select_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {glow});
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
                font-weight: 600;
                padding: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {glow}, stop:1 {color});
            }}
        """)
        select_btn.clicked.connect(lambda: self.selected.emit(self.class_id))
        layout.addWidget(select_btn)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected.emit(self.class_id)
        super().mousePressEvent(event)


class ProfileCard(QFrame):
    select_requested = Signal(str)
    delete_requested = Signal(str)
    rename_requested = Signal(str)
    
    def __init__(self, profile_data: dict):
        super().__init__()
        self.profile_data = profile_data
        self.setObjectName("profileCard")
        self.setFixedSize(300, 200)
        self.setCursor(Qt.PointingHandCursor)
        self._setup_ui()
    
    def _setup_ui(self):
        self.setStyleSheet("""
            QFrame#profileCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(26, 26, 62, 220), stop:1 rgba(13, 13, 43, 240));
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 16px;
            }
            QFrame#profileCard:hover {
                border: 2px solid rgba(90, 79, 255, 0.7);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 30, 70, 230), stop:1 rgba(18, 18, 50, 250));
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        header_layout = QHBoxLayout()
        
        class_colors = {
            "knight": "#9ca3af", "mage": "#a855f7", "duelist": "#fbbf24",
            "tank": "#78716c", "ranger": "#22c55e"
        }
        class_color = class_colors.get(self.profile_data.get('character_class', 'knight'), "#9ca3af")
        
        class_badge = QLabel(self.profile_data.get('character_class', 'Knight').upper())
        class_badge.setStyleSheet(f"""
            color: {class_color};
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 4px 8px;
            border: 1px solid {class_color};
            border-radius: 4px;
        """)
        header_layout.addWidget(class_badge)
        header_layout.addStretch()
        
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6b7280;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ef4444;
                background: rgba(239, 9, 68, 0.1);
                border-radius: 12px;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.profile_data['id']))
        header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        name = QLabel(self.profile_data.get('name', 'Unknown'))
        name.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 700;")
        layout.addWidget(name)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        level_info = QLabel(f"Level {self.profile_data.get('level', 1)}")
        level_info.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 600;")
        stats_layout.addWidget(level_info)
        
        gold_info = QLabel(f"{self.profile_data.get('gold', 0)} 💰")
        gold_info.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 600;")
        stats_layout.addWidget(gold_info)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        battles_info = QLabel(f"Battles Won: {self.profile_data.get('completed_battles', 0)}")
        battles_info.setStyleSheet("color: #9ca3af; font-size: 12px;")
        layout.addWidget(battles_info)
        
        last_played = self.profile_data.get('last_played', '')
        if last_played:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(last_played.replace('Z', '+00:00'))
                time_str = dt.strftime("%b %d, %Y %H:%M")
                playtime = self.profile_data.get('playtime_seconds', 0)
                hours = playtime // 3600
                minutes = (playtime % 3600) // 60
                time_str += f"  •  {hours}h {minutes}m played"
            except:
                time_str = last_played
        else:
            time_str = "Never played"
        
        last_played_label = QLabel(time_str)
        last_played_label.setStyleSheet("color: #6b7280; font-size: 11px;")
        layout.addWidget(last_played_label)
        
        layout.addStretch()
        
        continue_btn = QPushButton("CONTINUE")
        continue_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-size: 13px;
                font-weight: 600;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c6fff, stop:1 #c084fc);
            }
        """)
        continue_btn.clicked.connect(lambda: self.select_requested.emit(self.profile_data['id']))
        layout.addWidget(continue_btn)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.select_requested.emit(self.profile_data['id'])
        super().mousePressEvent(event)


class ProfileSelectScreen(QFrame):
    profile_selected = Signal(str)
    new_profile_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setObjectName("profileSelectScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("SELECT PROFILE")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Choose your adventure")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        from save.save_manager import SaveManager
        save_manager = SaveManager()
        profiles = save_manager.get_all_profiles()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(30, 30, 60, 150);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 4px;
                min-height: 30px;
            }
        """)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(16)
        container_layout.setAlignment(Qt.AlignTop)
        
        if profiles:
            for profile in profiles:
                card = ProfileCard(profile)
                card.select_requested.connect(self.profile_selected.emit)
                card.delete_requested.connect(self._on_delete_profile)
                container_layout.addWidget(card, alignment=Qt.AlignHCenter)
        else:
            empty_label = QLabel("No profiles found.\nCreate your first hero!")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 40px;")
            container_layout.addWidget(empty_label)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        new_btn = QPushButton("NEW PROFILE")
        new_btn.setObjectName("startButton")
        new_btn.setMinimumWidth(180)
        new_btn.clicked.connect(self.new_profile_requested.emit)
        btn_layout.addWidget(new_btn)
        
        exit_btn = QPushButton("EXIT")
        exit_btn.setObjectName("menuButton")
        exit_btn.setMinimumWidth(140)
        exit_btn.clicked.connect(lambda: QApplication.quit())
        btn_layout.addWidget(exit_btn)
        
        layout.addLayout(btn_layout)
    
    def _on_delete_profile(self, profile_id: str):
        from save.save_manager import SaveManager
        save_manager = SaveManager()
        if save_manager.delete_profile(profile_id):
            self._refresh()
    
    def _refresh(self):
        self.setParent(None)
        new_screen = ProfileSelectScreen()
        new_screen.profile_selected.connect(self.profile_selected)
        new_screen.new_profile_requested.connect(self.new_profile_requested)
        parent = self.parent()
        if parent:
            layout = parent.layout()
            if layout:
                layout.addWidget(new_screen)


class ClassSelectScreen(QFrame):
    class_selected = Signal(str, str)
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("CHOOSE YOUR CLASS")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Each class offers a unique playstyle")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        import json
        import os
        classes_path = "data/classes.json"
        if os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                classes_data = json.load(f)
        else:
            classes_data = {}
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:horizontal {
                background: rgba(30, 30, 60, 150);
                height: 8px; border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 4px; min-width: 30px;
            }
        """)
        
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setAlignment(Qt.AlignLeft)
        
        for class_id, class_data in classes_data.items():
            card = ClassCard(class_id, class_data)
            card.selected.connect(lambda cid: self.class_selected.emit(cid, self.name_input.text().strip() or "Hero"))
            container_layout.addWidget(card)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        name_layout = QVBoxLayout()
        name_layout.setSpacing(8)
        
        name_label = QLabel("HERO NAME")
        name_label.setObjectName("statLabel")
        name_label.setAlignment(Qt.AlignCenter)
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name...")
        self.name_input.setMaxLength(16)
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input.setFont(QFont("Segoe UI", 16))
        name_layout.addWidget(self.name_input)
        
        layout.addLayout(name_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        back_btn = QPushButton("BACK")
        back_btn.setObjectName("menuButton")
        back_btn.setMinimumWidth(140)
        back_btn.clicked.connect(self.back_requested.emit)
        btn_layout.addWidget(back_btn)
        
        start_btn = QPushButton("BEGIN JOURNEY")
        start_btn.setObjectName("startButton")
        start_btn.setMinimumWidth(180)
        start_btn.clicked.connect(lambda: self.class_selected.emit("knight", self.name_input.text().strip() or "Hero"))
        btn_layout.addWidget(start_btn)
        
        layout.addLayout(btn_layout)


class ProfileCard(QFrame):
    confirmed = Signal(dict)
    cancelled = Signal()
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setObjectName("levelUpScreen")
        self.pending_stats = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("LEVEL UP!")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #fbbf24;")
        layout.addWidget(title)
        
        subtitle = QLabel(f"You reached level {self.player.level}!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        points_label = QLabel(f"Stat Points Available: {self.player.stat_points}")
        points_label.setAlignment(Qt.AlignCenter)
        points_label.setStyleSheet("color: #fbbf24; font-size: 18px; font-weight: 700;")
        layout.addWidget(points_label)
        
        self.points_label = points_label
        
        stats_container = QFrame()
        stats_container.setStyleSheet("""
            QFrame {
                background: rgba(13, 13, 43, 200);
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 16px;
            }
        """)
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(24, 24, 24, 24)
        stats_layout.setSpacing(16)
        
        stats_title = QLabel("ALLOCATE STAT POINTS")
        stats_title.setObjectName("sectionTitle")
        stats_title.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(stats_title)
        
        effective = self.player.get_effective_stats()
        
        stat_options = [
            ("maxhealth", "Max HP", effective["maxhealth"], "+5-15 HP per point"),
            ("attack", "Attack", effective["attack"], "+3-4 Attack per point"),
            ("defense", "Defense", effective["defense"], "+2-3 Defense per point"),
            ("mana", "Max Mana", effective["maxmana"], "+5-15 Mana per point"),
            ("crit_chance", "Crit Chance", effective["crit_chance"], "+1-2% Crit per point"),
            ("mana_regen", "Mana Regen", effective["mana_regen"], "+1 Mana/sec per point"),
        ]
        
        self.stat_rows = {}
        
        for stat_key, stat_name, current_value, description in stat_options:
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background: rgba(26, 26, 62, 180);
                    border: 1px solid rgba(90, 79, 255, 0.2);
                    border-radius: 8px;
                }
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(16, 12, 16, 12)
            row_layout.setSpacing(16)
            
            name_label = QLabel(stat_name)
            name_label.setStyleSheet("color: #e0e0f0; font-size: 14px; font-weight: 600; min-width: 120px;")
            row_layout.addWidget(name_label)
            
            value_label = QLabel(str(current_value))
            value_label.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 700; min-width: 50px;")
            row_layout.addWidget(value_label)
            
            pending_label = QLabel("+0")
            pending_label.setStyleSheet("color: #4ade80; font-size: 14px; font-weight: 700; min-width: 50px;")
            pending_label.setVisible(False)
            row_layout.addWidget(pending_label)
            
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
            row_layout.addWidget(desc_label)
            
            row_layout.addStretch()
            
            minus_btn = QPushButton("−")
            minus_btn.setFixedSize(36, 36)
            minus_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 9, 68, 0.2);
                    border: 1px solid rgba(239, 9, 68, 0.4);
                    border-radius: 18px;
                    color: #ef4444;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(239, 9, 68, 0.4);
                    border: 1px solid rgba(239, 9, 68, 0.7);
                }
                QPushButton:disabled {
                    background: rgba(30, 30, 60, 150);
                    border: 1px solid rgba(90, 79, 255, 0.15);
                    color: rgba(156, 163, 175, 0.5);
                }
            """)
            minus_btn.setEnabled(False)
            minus_btn.clicked.connect(lambda checked, k=stat_key: self._modify_stat(k, -1))
            row_layout.addWidget(minus_btn)
            
            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(36, 36)
            plus_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(74, 222, 128, 0.2);
                    border: 1px solid rgba(74, 222, 128, 0.4);
                    border-radius: 18px;
                    color: #4ade80;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(74, 222, 128, 0.4);
                    border: 1px solid rgba(74, 222, 128, 0.7);
                }
                QPushButton:disabled {
                    background: rgba(30, 30, 60, 150);
                    border: 1px solid rgba(90, 79, 255, 0.15);
                    color: rgba(156, 163, 175, 0.5);
                }
            """)
            plus_btn.setEnabled(self.player.stat_points > 0)
            plus_btn.clicked.connect(lambda checked, k=stat_key: self._modify_stat(k, 1))
            row_layout.addWidget(plus_btn)
            
            self.stat_rows[stat_key] = {
                'value_label': value_label,
                'pending_label': pending_label,
                'minus_btn': minus_btn,
                'plus_btn': plus_btn,
                'pending': 0
            }
            
            stats_layout.addWidget(row)
        
        layout.addWidget(stats_container)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        reset_btn = QPushButton("RESET")
        reset_btn.setObjectName("menuButton")
        reset_btn.setMinimumWidth(140)
        reset_btn.clicked.connect(self._reset_stats)
        btn_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setObjectName("menuButton")
        cancel_btn.setMinimumWidth(140)
        cancel_btn.clicked.connect(self.cancelled.emit)
        btn_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("CONFIRM")
        confirm_btn.setObjectName("startButton")
        confirm_btn.setMinimumWidth(180)
        confirm_btn.clicked.connect(self._confirm)
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)
    
    def _modify_stat(self, stat_key: str, delta: int):
        if delta > 0 and self.player.stat_points <= 0:
            return
        
        row = self.stat_rows[stat_key]
        new_pending = row['pending'] + delta
        
        if new_pending < 0:
            return
        
        if delta > 0:
            self.player.stat_points -= 1
        else:
            self.player.stat_points += 1
        
        row['pending'] = new_pending
        
        if row['pending'] > 0:
            row['pending_label'].setText(f"+{row['pending']}")
            row['pending_label'].setVisible(True)
        else:
            row['pending_label'].setVisible(False)
        
        row['minus_btn'].setEnabled(row['pending'] > 0)
        
        for k, r in self.stat_rows.items():
            r['plus_btn'].setEnabled(self.player.stat_points > 0)
        
        self.points_label.setText(f"Stat Points Available: {self.player.stat_points}")
    
    def _reset_stats(self):
        for stat_key, row in self.stat_rows.items():
            if row['pending'] > 0:
                self.player.stat_points += row['pending']
                row['pending'] = 0
                row['pending_label'].setVisible(False)
                row['minus_btn'].setEnabled(False)
        
        for k, r in self.stat_rows.items():
            r['plus_btn'].setEnabled(self.player.stat_points > 0)
        
        self.points_label.setText(f"Stat Points Available: {self.player.stat_points}")
    
    def _confirm(self):
        allocations = {}
        for stat_key, row in self.stat_rows.items():
            if row['pending'] > 0:
                for _ in range(row['pending']):
                    self.player.allocate_stat(stat_key)
                allocations[stat_key] = row['pending']
        
        if allocations:
            self.confirmed.emit(allocations)
        else:
            self.cancelled.emit()


class SettingsScreen(QFrame):
    closed = Signal()
    settings_changed = Signal(dict)
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.setObjectName("settingsScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("SETTINGS")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 8px;
                background: rgba(13, 13, 43, 200);
            }
            QTabBar::tab {
                background: rgba(26, 26, 62, 180);
                border: 1px solid rgba(90, 79, 255, 0.2);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #9ca3af;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(90, 79, 255, 0.4), stop:1 rgba(168, 85, 247, 0.3));
                color: #ffffff;
                border: 1px solid rgba(90, 79, 255, 0.5);
            }
            QTabBar::tab:hover:!selected {
                background: rgba(90, 79, 255, 0.2);
                color: #c084fc;
            }
        """)
        
        # Audio Tab
        audio_tab = QWidget()
        audio_layout = QVBoxLayout(audio_tab)
        audio_layout.setContentsMargins(24, 24, 24, 24)
        audio_layout.setSpacing(20)
        
        self.music_slider = self._create_slider(audio_layout, "Music Volume", self.config.get('music_volume', 0.7))
        self.sfx_slider = self._create_slider(audio_layout, "SFX Volume", self.config.get('sfx_volume', 0.8))
        
        self.music_slider.valueChanged.connect(lambda v: self._update_config('music_volume', v / 100))
        self.sfx_slider.valueChanged.connect(lambda v: self._update_config('sfx_volume', v / 100))
        
        audio_layout.addStretch()
        tabs.addTab(audio_tab, "AUDIO")
        
        # Video Tab
        video_tab = QWidget()
        video_layout = QVBoxLayout(video_tab)
        video_layout.setContentsMargins(24, 24, 24, 24)
        video_layout.setSpacing(20)
        
        fullscreen_cb = QCheckBox("Fullscreen")
        fullscreen_cb.setChecked(self.config.get('fullscreen', False))
        fullscreen_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        fullscreen_cb.toggled.connect(lambda v: self._update_config('fullscreen', v))
        video_layout.addWidget(fullscreen_cb)
        
        animations_cb = QCheckBox("Enable Animations")
        animations_cb.setChecked(self.config.get('animations', True))
        animations_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        animations_cb.toggled.connect(lambda v: self._update_config('animations', v))
        video_layout.addWidget(animations_cb)
        
        particles_cb = QCheckBox("Particle Effects")
        particles_cb.setChecked(self.config.get('particles', True))
        particles_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        particles_cb.toggled.connect(lambda v: self._update_config('particles', v))
        video_layout.addWidget(particles_cb)
        
        video_layout.addStretch()
        tabs.addTab(video_tab, "VIDEO")
        
        # Gameplay Tab
        gameplay_tab = QWidget()
        gameplay_layout = QVBoxLayout(gameplay_tab)
        gameplay_layout.setContentsMargins(24, 24, 24, 24)
        gameplay_layout.setSpacing(20)
        
        autosave_cb = QCheckBox("Auto-save")
        autosave_cb.setChecked(self.config.get('autosave', True))
        autosave_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        autosave_cb.toggled.connect(lambda v: self._update_config('autosave', v))
        gameplay_layout.addWidget(autosave_cb)
        
        combat_log_cb = QCheckBox("Detailed Combat Log")
        combat_log_cb.setChecked(self.config.get('detailed_log', True))
        combat_log_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        combat_log_cb.toggled.connect(lambda v: self._update_config('detailed_log', v))
        gameplay_layout.addWidget(combat_log_cb)
        
        gameplay_layout.addStretch()
        tabs.addTab(gameplay_tab, "GAMEPLAY")
        
        # Data Tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(24, 24, 24, 24)
        data_layout.setSpacing(20)
        
        reset_btn = QPushButton("RESET ALL SAVE DATA")
        reset_btn.setObjectName("attackButton")
        reset_btn.setMinimumHeight(48)
        reset_btn.setStyleSheet("font-size: 14px; font-weight: 700;")
        reset_btn.clicked.connect(self._confirm_reset)
        data_layout.addWidget(reset_btn)
        
        export_btn = QPushButton("EXPORT SAVE DATA")
        export_btn.setObjectName("healButton")
        export_btn.setMinimumHeight(48)
        export_btn.setStyleSheet("font-size: 14px; font-weight: 700;")
        export_btn.clicked.connect(self._export_save)
        data_layout.addWidget(export_btn)
        
        data_layout.addStretch()
        tabs.addTab(data_tab, "DATA")
        
        layout.addWidget(tabs)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("DONE")
        close_btn.setObjectName("startButton")
        close_btn.setMinimumWidth(160)
        close_btn.clicked.connect(self._on_close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_slider(self, parent_layout, label_text, value):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)
        
        label = QLabel(f"{label_text}: {int(value * 100)}%")
        label.setStyleSheet("color: #e0e0f0; font-size: 14px; font-weight: 600;")
        container_layout.addWidget(label)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(int(value * 100))
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(30, 30, 60, 180);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border: 2px solid #ffffff;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 3px;
            }
        """)
        slider.valueChanged.connect(lambda v: label.setText(f"{label_text}: {v}%"))
        container_layout.addWidget(slider)
        
        parent_layout.addWidget(container)
        return slider
    
    def _update_config(self, key, value):
        self.config[key] = value
    
    def _confirm_reset(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "This will permanently delete ALL save data.\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            import shutil
            saves_dir = "saves"
            if os.path.exists(saves_dir):
                shutil.rmtree(saves_dir)
                os.makedirs(saves_dir)
            QMessageBox.information(self, "Done", "All save data has been reset.")
    
    def _export_save(self):
        import json
        from datetime import datetime
        saves_dir = "saves"
        if os.path.exists(saves_dir):
            export_data = {}
            for filename in os.listdir(saves_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(saves_dir, filename), 'r') as f:
                        export_data[filename[:-5]] = json.load(f)
            
            export_path = f"save_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            QMessageBox.information(self, "Exported", f"Save data exported to {export_path}")
        else:
            QMessageBox.warning(self, "Error", "No save data found.")
    
    def _on_close(self):
        self.settings_changed.emit(self.config)
        self.closed.emit()


class ShopScreen(QFrame):
    closed = Signal()
    item_bought = Signal(str)
    item_sold = Signal(str)
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setObjectName("shopScreen")
        self._setup_ui()
        self._load_shop()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        title = QLabel("MERCHANT")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.gold_label = QLabel(f"{self.player.gold} 💰")
        self.gold_label.setStyleSheet("color: #fbbf24; font-size: 18px; font-weight: 700;")
        header_layout.addWidget(self.gold_label)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 9, 68, 0.2);
                border: 1px solid rgba(239, 9, 68, 0.4);
                border-radius: 18px;
                color: #ef4444;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 9, 68, 0.4);
                border: 1px solid rgba(239, 9, 68, 0.7);
            }
        """)
        close_btn.clicked.connect(self.closed.emit)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        merchant_label = QLabel('"Welcome, traveler! Take a look at my wares."')
        merchant_label.setAlignment(Qt.AlignCenter)
        merchant_label.setStyleSheet("color: #a855f7; font-size: 14px; font-style: italic; padding: 16px;")
        layout.addWidget(merchant_label)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 8px;
                background: rgba(13, 13, 43, 200);
            }
            QTabBar::tab {
                background: rgba(26, 26, 62, 180);
                border: 1px solid rgba(90, 79, 255, 0.2);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #9ca3af;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(90, 79, 255, 0.4), stop:1 rgba(168, 85, 247, 0.3));
                color: #ffffff;
                border: 1px solid rgba(90, 79, 255, 0.5);
            }
            QTabBar::tab:hover:!selected {
                background: rgba(90, 79, 255, 0.2);
                color: #c084fc;
            }
        """)
        
        self.buy_list = QListWidget()
        self.buy_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                color: #e0e0f0;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid rgba(90, 79, 255, 0.1);
            }
            QListWidget::item:selected {
                background: rgba(90, 79, 255, 0.3);
                color: #ffffff;
            }
            QListWidget::item:hover {
                background: rgba(90, 79, 255, 0.15);
            }
        """)
        self.tabs.addTab(self.buy_list, "BUY")
        
        self.sell_list = QListWidget()
        self.sell_list.setStyleSheet(self.buy_list.styleSheet())
        self.tabs.addTab(self.sell_list, "SELL")
        
        layout.addWidget(self.tabs)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.buy_btn = QPushButton("BUY")
        self.buy_btn.setObjectName("healButton")
        self.buy_btn.setMinimumWidth(120)
        self.buy_btn.clicked.connect(self._on_buy_item)
        btn_layout.addWidget(self.buy_btn)
        
        self.sell_btn = QPushButton("SELL")
        self.sell_btn.setObjectName("attackButton")
        self.sell_btn.setMinimumWidth(120)
        self.sell_btn.clicked.connect(self._on_sell_item)
        btn_layout.addWidget(self.sell_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.buy_list.itemSelectionChanged.connect(self._update_buttons)
        self.sell_list.itemSelectionChanged.connect(self._update_buttons)
    
    def _load_shop(self):
        import json
        items_path = "data/items.json"
        if not os.path.exists(items_path):
            return
        
        with open(items_path, 'r') as f:
            all_items = json.load(f)
        
        self._populate_buy_list(all_items)
        self._populate_sell_list(all_items)
    
    def _populate_buy_list(self, all_items):
        self.buy_list.clear()
        
        available_items = {}
        for category_name in ['weapons', 'armor', 'accessories', 'consumables']:
            category = all_items.get(category_name, {})
            for item_id, data in category.items():
                level_req = data.get('level_req', 1)
                if self.player.level >= level_req:
                    available_items[item_id] = data
        
        rarity_order = {'mythic': 0, 'legendary': 1, 'epic': 2, 'rare': 3, 'uncommon': 4, 'common': 5}
        sorted_items = sorted(available_items.items(), key=lambda x: rarity_order.get(x[1].get('rarity', 'common'), 99))
        
        for item_id, data in sorted_items:
            self._add_buy_item(item_id, data)
    
    def _add_buy_item(self, item_id, data):
        rarity = data.get('rarity', 'common')
        rarity_colors = {
            'common': '#9ca3af', 'uncommon': '#4ade80', 'rare': '#60a5fa',
            'epic': '#a855f7', 'legendary': '#fbbf24', 'mythic': '#f97316'
        }
        color = rarity_colors.get(rarity, '#9ca3af')
        
        name = data.get('name', item_id)
        
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 4, 8, 4)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 600;")
        item_layout.addWidget(name_label)
        
        stats = data.get('base_stats', {})
        if stats:
            stat_text = ", ".join([f"+{v} {k}" for k, v in stats.items()])
            stat_label = QLabel(stat_text)
            stat_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
            item_layout.addWidget(stat_label)
        
        item_layout.addStretch()
        
        value = data.get('value', 0)
        value_label = QLabel(f"{value} 💰")
        value_label.setStyleSheet("color: #fbbf24; font-size: 11px; font-weight: 600;")
        item_layout.addWidget(value_label)
        
        list_item = QListWidgetItem()
        list_item.setData(Qt.UserRole, item_id)
        list_item.setSizeHint(item_widget.sizeHint())
        self.buy_list.addItem(list_item)
        self.buy_list.setItemWidget(list_item, item_widget)
    
    def _populate_sell_list(self, all_items):
        self.sell_list.clear()
        
        item_counts = {}
        for inv_item in self.player.inventory:
            if isinstance(inv_item, dict):
                item_id = inv_item.get('id', '')
                qty = inv_item.get('quantity', 1)
            else:
                item_id = inv_item
                qty = 1
            
            for category in all_items.values():
                if isinstance(category, dict) and item_id in category:
                    if item_id not in item_counts:
                        item_counts[item_id] = {'qty': 0, 'data': category[item_id]}
                    item_counts[item_id]['qty'] += qty
                    break
        
        for item_id, info in item_counts.items():
            data = info['data']
            qty = info['qty']
            
            rarity = data.get('rarity', 'common')
            rarity_colors = {
                'common': '#9ca3af', 'uncommon': '#4ade80', 'rare': '#60a5fa',
                'epic': '#a855f7', 'legendary': '#fbbf24', 'mythic': '#f97316'
            }
            color = rarity_colors.get(rarity, '#9ca3af')
            
            name = data.get('name', item_id)
            if qty > 1:
                name += f" x{qty}"
            
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(8, 4, 8, 4)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 600;")
            item_layout.addWidget(name_label)
            
            item_layout.addStretch()
            
            value = data.get('value', 0) // 2
            value_label = QLabel(f"{value} 💰")
            value_label.setStyleSheet("color: #fbbf24; font-size: 11px; font-weight: 600;")
            item_layout.addWidget(value_label)
            
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, item_id)
            list_item.setSizeHint(item_widget.sizeHint())
            self.sell_list.addItem(list_item)
            self.sell_list.setItemWidget(list_item, item_widget)
    
    def _on_tab_changed(self, index):
        self._update_buttons()
    
    def _update_buttons(self):
        if self.tabs.currentIndex() == 0:
            has_selection = len(self.buy_list.selectedItems()) > 0
            self.buy_btn.setEnabled(has_selection)
            self.sell_btn.setEnabled(False)
        else:
            has_selection = len(self.sell_list.selectedItems()) > 0
            self.buy_btn.setEnabled(False)
            self.sell_btn.setEnabled(has_selection)
    
    def _on_buy_item(self):
        if self.tabs.currentIndex() == 0 and self.buy_list.selectedItems():
            item_id = self.buy_list.selectedItems()[0].data(Qt.UserRole)
            item_data = self._get_item_data(item_id)
            if item_data and self.player.spend_gold(item_data.get('value', 0)):
                self.player.add_to_inventory(item_id, 1)
                self.item_bought.emit(item_id)
                self.gold_label.setText(f"{self.player.gold} 💰")
                self._load_shop()
    
    def _on_sell_item(self):
        if self.tabs.currentIndex() == 1 and self.sell_list.selectedItems():
            item_id = self.sell_list.selectedItems()[0].data(Qt.UserRole)
            item_data = self._get_item_data(item_id)
            if item_data and self.player.remove_from_inventory(item_id, 1):
                value = item_data.get('value', 0) // 2
                self.player.add_gold(value)
                self.item_sold.emit(item_id)
                self.gold_label.setText(f"{self.player.gold} 💰")
                self._load_shop()
    
    def _get_item_data(self, item_id):
        import json
        items_path = "data/items.json"
        if os.path.exists(items_path):
            with open(items_path, 'r') as f:
                all_items = json.load(f)
                for category in all_items.values():
                    if isinstance(category, dict) and item_id in category:
                        return category[item_id]
        return None


class InventoryScreen(QFrame):
    closed = Signal()
    item_used = Signal(str)
    item_equipped = Signal(str)
    item_unequipped = Signal(str)
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setObjectName("inventoryScreen")
        self._setup_ui()
        self._load_items()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        title = QLabel("INVENTORY")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.gold_label = QLabel(f"{self.player.gold} 💰")
        self.gold_label.setStyleSheet("color: #fbbf24; font-size: 18px; font-weight: 700;")
        header_layout.addWidget(self.gold_label)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 9, 68, 0.2);
                border: 1px solid rgba(239, 9, 68, 0.4);
                border-radius: 18px;
                color: #ef4444;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(239, 9, 68, 0.4);
                border: 1px solid rgba(239, 9, 68, 0.7);
            }
        """)
        close_btn.clicked.connect(self.closed.emit)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 8px;
                background: rgba(13, 13, 43, 200);
            }
            QTabBar::tab {
                background: rgba(26, 26, 62, 180);
                border: 1px solid rgba(90, 79, 255, 0.2);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #9ca3af;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(90, 79, 255, 0.4), stop:1 rgba(168, 85, 247, 0.3));
                color: #ffffff;
                border: 1px solid rgba(90, 79, 255, 0.5);
            }
            QTabBar::tab:hover:!selected {
                background: rgba(90, 79, 255, 0.2);
                color: #c084fc;
            }
        """)
        
        self.consumables_list = QListWidget()
        self.consumables_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                color: #e0e0f0;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid rgba(90, 79, 255, 0.1);
            }
            QListWidget::item:selected {
                background: rgba(90, 79, 255, 0.3);
                color: #ffffff;
            }
            QListWidget::item:hover {
                background: rgba(90, 79, 255, 0.15);
            }
        """)
        self.tabs.addTab(self.consumables_list, "CONSUMABLES")
        
        self.weapons_list = QListWidget()
        self.weapons_list.setStyleSheet(self.consumables_list.styleSheet())
        self.tabs.addTab(self.weapons_list, "WEAPONS")
        
        self.armor_list = QListWidget()
        self.armor_list.setStyleSheet(self.consumables_list.styleSheet())
        self.tabs.addTab(self.armor_list, "ARMOR")
        
        self.accessories_list = QListWidget()
        self.accessories_list.setStyleSheet(self.consumables_list.styleSheet())
        self.tabs.addTab(self.accessories_list, "ACCESSORIES")
        
        layout.addWidget(self.tabs)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.use_btn = QPushButton("USE")
        self.use_btn.setObjectName("healButton")
        self.use_btn.setMinimumWidth(100)
        self.use_btn.clicked.connect(self._on_use_item)
        btn_layout.addWidget(self.use_btn)
        
        self.equip_btn = QPushButton("EQUIP")
        self.equip_btn.setObjectName("attackButton")
        self.equip_btn.setMinimumWidth(100)
        self.equip_btn.clicked.connect(self._on_equip_item)
        btn_layout.addWidget(self.equip_btn)
        
        self.unequip_btn = QPushButton("UNEQUIP")
        self.unequip_btn.setObjectName("menuButton")
        self.unequip_btn.setMinimumWidth(100)
        self.unequip_btn.clicked.connect(self._on_unequip_item)
        btn_layout.addWidget(self.unequip_btn)
        
        self.sell_btn = QPushButton("SELL")
        self.sell_btn.setObjectName("menuButton")
        self.sell_btn.setMinimumWidth(100)
        self.sell_btn.clicked.connect(self._on_sell_item)
        btn_layout.addWidget(self.sell_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.current_list = self.consumables_list
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.consumables_list.itemSelectionChanged.connect(self._update_buttons)
        self.weapons_list.itemSelectionChanged.connect(self._update_buttons)
        self.armor_list.itemSelectionChanged.connect(self._update_buttons)
        self.accessories_list.itemSelectionChanged.connect(self._update_buttons)
    
    def _load_items(self):
        import json
        items_path = "data/items.json"
        if not os.path.exists(items_path):
            return
        
        with open(items_path, 'r') as f:
            all_items = json.load(f)
        
        self._populate_list(self.consumables_list, self.player.inventory, all_items.get('consumables', {}), is_consumable=True)
        self._populate_list(self.weapons_list, [i for i in self.player.inventory if isinstance(i, str) or (isinstance(i, dict) and i.get('id', '').startswith('weapon'))], all_items.get('weapons', {}), is_equipment=True)
        self._populate_list(self.armor_list, [i for i in self.player.inventory if isinstance(i, str) or (isinstance(i, dict) and i.get('id', '').startswith('armor'))], all_items.get('armor', {}), is_equipment=True)
        self._populate_list(self.accessories_list, [i for i in self.player.inventory if isinstance(i, str) or (isinstance(i, dict) and i.get('id', '').startswith('accessory'))], all_items.get('accessories', {}), is_equipment=True)
    
    def _populate_list(self, list_widget, inventory, item_db, is_consumable=False, is_equipment=False):
        list_widget.clear()
        
        item_counts = {}
        for inv_item in inventory:
            if isinstance(inv_item, dict):
                item_id = inv_item.get('id', '')
                qty = inv_item.get('quantity', 1)
            else:
                item_id = inv_item
                qty = 1
            
            if item_id in item_db:
                if item_id not in item_counts:
                    item_counts[item_id] = {'qty': 0, 'data': item_db[item_id]}
                item_counts[item_id]['qty'] += qty
        
        for item_id, info in item_counts.items():
            data = info['data']
            qty = info['qty']
            
            rarity = data.get('rarity', 'common')
            rarity_colors = {
                'common': '#9ca3af', 'uncommon': '#4ade80', 'rare': '#60a5fa',
                'epic': '#a855f7', 'legendary': '#fbbf24', 'mythic': '#f97316'
            }
            color = rarity_colors.get(rarity, '#9ca3af')
            
            name = data.get('name', item_id)
            if qty > 1:
                name += f" x{qty}"
            
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(8, 4, 8, 4)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 600;")
            item_layout.addWidget(name_label)
            
            if is_equipment:
                stats = data.get('base_stats', {})
                stat_text = ", ".join([f"+{v} {k}" for k, v in stats.items()])
                stat_label = QLabel(stat_text)
                stat_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
                item_layout.addWidget(stat_label)
            
            item_layout.addStretch()
            
            value = data.get('value', 0)
            value_label = QLabel(f"{value} 💰")
            value_label.setStyleSheet("color: #fbbf24; font-size: 11px; font-weight: 600;")
            item_layout.addWidget(value_label)
            
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, item_id)
            list_item.setSizeHint(item_widget.sizeHint())
            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, item_widget)
    
    def _on_tab_changed(self, index):
        self._update_buttons()
    
    def _update_buttons(self):
        current_list = self.tabs.currentWidget()
        has_selection = len(current_list.selectedItems()) > 0
        
        if current_list == self.consumables_list:
            self.use_btn.setEnabled(has_selection)
            self.equip_btn.setEnabled(False)
            self.unequip_btn.setEnabled(False)
        else:
            self.use_btn.setEnabled(False)
            self.equip_btn.setEnabled(has_selection)
            self.unequip_btn.setEnabled(has_selection)
        
        self.sell_btn.setEnabled(has_selection)
    
    def _on_use_item(self):
        current_list = self.consumables_list
        if current_list.selectedItems():
            item_id = current_list.selectedItems()[0].data(Qt.UserRole)
            if self.player.use_consumable(item_id):
                self.item_used.emit(item_id)
                self.gold_label.setText(f"{self.player.gold} 💰")
                self._load_items()
    
    def _on_equip_item(self):
        current_list = self.tabs.currentWidget()
        if current_list.selectedItems():
            item_id = current_list.selectedItems()[0].data(Qt.UserRole)
            if self.player.equip_item(item_id):
                self.item_equipped.emit(item_id)
                self._load_items()
    
    def _on_unequip_item(self):
        current_list = self.tabs.currentWidget()
        if current_list.selectedItems():
            item_id = current_list.selectedItems()[0].data(Qt.UserRole)
            slot = None
            for s, i in self.player.equipment.items():
                if i == item_id:
                    slot = s
                    break
            if slot and self.player.unequip_item(slot):
                self.item_unequipped.emit(item_id)
                self._load_items()
    
    def _on_sell_item(self):
        current_list = self.tabs.currentWidget()
        if current_list.selectedItems():
            item_id = current_list.selectedItems()[0].data(Qt.UserRole)
            item_data = self.player.get_item(item_id)
            if item_data:
                value = item_data.get('value', 0) // 2
                if self.player.remove_from_inventory(item_id, 1):
                    self.player.add_gold(value)
                    self.gold_label.setText(f"{self.player.gold} 💰")
                    self._load_items()


class ProfileSelectScreen(QFrame):
    profile_selected = Signal(str)
    new_profile_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setObjectName("profileSelectScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("SELECT PROFILE")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Choose your adventure")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        from save.save_manager import SaveManager
        save_manager = SaveManager()
        profiles = save_manager.get_all_profiles()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(30, 30, 60, 150);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 4px;
                min-height: 30px;
            }
        """)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(16)
        container_layout.setAlignment(Qt.AlignTop)
        
        if profiles:
            for profile in profiles:
                card = ProfileCard(profile)
                card.select_requested.connect(self.profile_selected.emit)
                card.delete_requested.connect(self._on_delete_profile)
                container_layout.addWidget(card, alignment=Qt.AlignHCenter)
        else:
            empty_label = QLabel("No profiles found.\nCreate your first hero!")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 40px;")
            container_layout.addWidget(empty_label)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        new_btn = QPushButton("NEW PROFILE")
        new_btn.setObjectName("startButton")
        new_btn.setMinimumWidth(180)
        new_btn.clicked.connect(self.new_profile_requested.emit)
        btn_layout.addWidget(new_btn)
        
        exit_btn = QPushButton("EXIT")
        exit_btn.setObjectName("menuButton")
        exit_btn.setMinimumWidth(140)
        exit_btn.clicked.connect(lambda: QApplication.quit())
        btn_layout.addWidget(exit_btn)
        
        layout.addLayout(btn_layout)
    
    def _on_delete_profile(self, profile_id: str):
        from save.save_manager import SaveManager
        save_manager = SaveManager()
        if save_manager.delete_profile(profile_id):
            pass


class ClassSelectScreen(QFrame):
    class_selected = Signal(str, str)
    back_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("CHOOSE YOUR CLASS")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Each class offers a unique playstyle")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        import json
        classes_path = "data/classes.json"
        if os.path.exists(classes_path):
            with open(classes_path, 'r') as f:
                classes_data = json.load(f)
        else:
            classes_data = {}
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:horizontal {
                background: rgba(30, 30, 60, 150);
                height: 8px; border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 4px; min-width: 30px;
            }
        """)
        
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setAlignment(Qt.AlignLeft)
        
        for class_id, class_data in classes_data.items():
            card = ClassCard(class_id, class_data)
            card.selected.connect(lambda cid: self.class_selected.emit(cid, self.name_input.text().strip() or "Hero"))
            container_layout.addWidget(card)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        name_layout = QVBoxLayout()
        name_layout.setSpacing(8)
        
        name_label = QLabel("HERO NAME")
        name_label.setObjectName("statLabel")
        name_label.setAlignment(Qt.AlignCenter)
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name...")
        self.name_input.setMaxLength(16)
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input.setFont(QFont("Segoe UI", 16))
        name_layout.addWidget(self.name_input)
        
        layout.addLayout(name_layout)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        back_btn = QPushButton("BACK")
        back_btn.setObjectName("menuButton")
        back_btn.setMinimumWidth(140)
        back_btn.clicked.connect(self.back_requested.emit)
        btn_layout.addWidget(back_btn)
        
        start_btn = QPushButton("BEGIN JOURNEY")
        start_btn.setObjectName("startButton")
        start_btn.setMinimumWidth(180)
        start_btn.clicked.connect(lambda: self.class_selected.emit("knight", self.name_input.text().strip() or "Hero"))
        btn_layout.addWidget(start_btn)
        
        layout.addLayout(btn_layout)


class LevelUpScreen(QFrame):
    confirmed = Signal(dict)
    cancelled = Signal()
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setObjectName("levelUpScreen")
        self.pending_stats = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("LEVEL UP!")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #fbbf24;")
        layout.addWidget(title)
        
        subtitle = QLabel(f"You reached level {self.player.level}!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        points_label = QLabel(f"Stat Points Available: {self.player.stat_points}")
        points_label.setAlignment(Qt.AlignCenter)
        points_label.setStyleSheet("color: #fbbf24; font-size: 18px; font-weight: 700;")
        layout.addWidget(points_label)
        
        self.points_label = points_label
        
        stats_container = QFrame()
        stats_container.setStyleSheet("""
            QFrame {
                background: rgba(13, 13, 43, 200);
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 16px;
            }
        """)
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(24, 24, 24, 24)
        stats_layout.setSpacing(16)
        
        stats_title = QLabel("ALLOCATE STAT POINTS")
        stats_title.setObjectName("sectionTitle")
        stats_title.setAlignment(Qt.AlignCenter)
        stats_layout.addWidget(stats_title)
        
        effective = self.player.get_effective_stats()
        
        stat_options = [
            ("maxhealth", "Max HP", effective["maxhealth"], "+5-15 HP per point"),
            ("attack", "Attack", effective["attack"], "+3-4 Attack per point"),
            ("defense", "Defense", effective["defense"], "+2-3 Defense per point"),
            ("mana", "Max Mana", effective["maxmana"], "+5-15 Mana per point"),
            ("crit_chance", "Crit Chance", effective["crit_chance"], "+1-2% Crit per point"),
            ("mana_regen", "Mana Regen", effective["mana_regen"], "+1 Mana/sec per point"),
        ]
        
        self.stat_rows = {}
        
        for stat_key, stat_name, current_value, description in stat_options:
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background: rgba(26, 26, 62, 180);
                    border: 1px solid rgba(90, 79, 255, 0.2);
                    border-radius: 8px;
                }
            """)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(16, 12, 16, 12)
            row_layout.setSpacing(16)
            
            name_label = QLabel(stat_name)
            name_label.setStyleSheet("color: #e0e0f0; font-size: 14px; font-weight: 600; min-width: 120px;")
            row_layout.addWidget(name_label)
            
            value_label = QLabel(str(current_value))
            value_label.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 700; min-width: 50px;")
            row_layout.addWidget(value_label)
            
            pending_label = QLabel("+0")
            pending_label.setStyleSheet("color: #4ade80; font-size: 14px; font-weight: 700; min-width: 50px;")
            pending_label.setVisible(False)
            row_layout.addWidget(pending_label)
            
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
            row_layout.addWidget(desc_label)
            
            row_layout.addStretch()
            
            minus_btn = QPushButton("−")
            minus_btn.setFixedSize(36, 36)
            minus_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 9, 68, 0.2);
                    border: 1px solid rgba(239, 9, 68, 0.4);
                    border-radius: 18px;
                    color: #ef4444;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(239, 9, 68, 0.4);
                    border: 1px solid rgba(239, 9, 68, 0.7);
                }
                QPushButton:disabled {
                    background: rgba(30, 30, 60, 150);
                    border: 1px solid rgba(90, 79, 255, 0.15);
                    color: rgba(156, 163, 175, 0.5);
                }
            """)
            minus_btn.setEnabled(False)
            minus_btn.clicked.connect(lambda checked, k=stat_key: self._modify_stat(k, -1))
            row_layout.addWidget(minus_btn)
            
            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(36, 36)
            plus_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(74, 222, 128, 0.2);
                    border: 1px solid rgba(74, 222, 128, 0.4);
                    border-radius: 18px;
                    color: #4ade80;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(74, 222, 128, 0.4);
                    border: 1px solid rgba(74, 222, 128, 0.7);
                }
                QPushButton:disabled {
                    background: rgba(30, 30, 60, 150);
                    border: 1px solid rgba(90, 79, 255, 0.15);
                    color: rgba(156, 163, 175, 0.5);
                }
            """)
            plus_btn.setEnabled(self.player.stat_points > 0)
            plus_btn.clicked.connect(lambda checked, k=stat_key: self._modify_stat(k, 1))
            row_layout.addWidget(plus_btn)
            
            self.stat_rows[stat_key] = {
                'value_label': value_label,
                'pending_label': pending_label,
                'minus_btn': minus_btn,
                'plus_btn': plus_btn,
                'pending': 0
            }
            
            stats_layout.addWidget(row)
        
        layout.addWidget(stats_container)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)
        
        reset_btn = QPushButton("RESET")
        reset_btn.setObjectName("menuButton")
        reset_btn.setMinimumWidth(140)
        reset_btn.clicked.connect(self._reset_stats)
        btn_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setObjectName("menuButton")
        cancel_btn.setMinimumWidth(140)
        cancel_btn.clicked.connect(self.cancelled.emit)
        btn_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("CONFIRM")
        confirm_btn.setObjectName("startButton")
        confirm_btn.setMinimumWidth(180)
        confirm_btn.clicked.connect(self._confirm)
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)
    
    def _modify_stat(self, stat_key: str, delta: int):
        if delta > 0 and self.player.stat_points <= 0:
            return
        
        row = self.stat_rows[stat_key]
        new_pending = row['pending'] + delta
        
        if new_pending < 0:
            return
        
        if delta > 0:
            self.player.stat_points -= 1
        else:
            self.player.stat_points += 1
        
        row['pending'] = new_pending
        
        if row['pending'] > 0:
            row['pending_label'].setText(f"+{row['pending']}")
            row['pending_label'].setVisible(True)
        else:
            row['pending_label'].setVisible(False)
        
        row['minus_btn'].setEnabled(row['pending'] > 0)
        
        for k, r in self.stat_rows.items():
            r['plus_btn'].setEnabled(self.player.stat_points > 0)
        
        self.points_label.setText(f"Stat Points Available: {self.player.stat_points}")
    
    def _reset_stats(self):
        for stat_key, row in self.stat_rows.items():
            if row['pending'] > 0:
                self.player.stat_points += row['pending']
                row['pending'] = 0
                row['pending_label'].setVisible(False)
                row['minus_btn'].setEnabled(False)
        
        for k, r in self.stat_rows.items():
            r['plus_btn'].setEnabled(self.player.stat_points > 0)
        
        self.points_label.setText(f"Stat Points Available: {self.player.stat_points}")
    
    def _confirm(self):
        allocations = {}
        for stat_key, row in self.stat_rows.items():
            if row['pending'] > 0:
                for _ in range(row['pending']):
                    self.player.allocate_stat(stat_key)
                allocations[stat_key] = row['pending']
        
        if allocations:
            self.confirmed.emit(allocations)
        else:
            self.cancelled.emit()


class SettingsScreen(QFrame):
    closed = Signal()
    settings_changed = Signal(dict)
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.setObjectName("settingsScreen")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        title = QLabel("SETTINGS")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(90, 79, 255, 0.3);
                border-radius: 8px;
                background: rgba(13, 13, 43, 200);
            }
            QTabBar::tab {
                background: rgba(26, 26, 62, 180);
                border: 1px solid rgba(90, 79, 255, 0.2);
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #9ca3af;
                font-size: 13px;
                font-weight: 600;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(90, 79, 255, 0.4), stop:1 rgba(168, 85, 247, 0.3));
                color: #ffffff;
                border: 1px solid rgba(90, 79, 255, 0.5);
            }
            QTabBar::tab:hover:!selected {
                background: rgba(90, 79, 255, 0.2);
                color: #c084fc;
            }
        """)
        
        # Audio Tab
        audio_tab = QWidget()
        audio_layout = QVBoxLayout(audio_tab)
        audio_layout.setContentsMargins(24, 24, 24, 24)
        audio_layout.setSpacing(20)
        
        self.music_slider = self._create_slider(audio_layout, "Music Volume", self.config.get('music_volume', 0.7))
        self.sfx_slider = self._create_slider(audio_layout, "SFX Volume", self.config.get('sfx_volume', 0.8))
        
        self.music_slider.valueChanged.connect(lambda v: self._update_config('music_volume', v / 100))
        self.sfx_slider.valueChanged.connect(lambda v: self._update_config('sfx_volume', v / 100))
        
        audio_layout.addStretch()
        tabs.addTab(audio_tab, "AUDIO")
        
        # Video Tab
        video_tab = QWidget()
        video_layout = QVBoxLayout(video_tab)
        video_layout.setContentsMargins(24, 24, 24, 24)
        video_layout.setSpacing(20)
        
        fullscreen_cb = QCheckBox("Fullscreen")
        fullscreen_cb.setChecked(self.config.get('fullscreen', False))
        fullscreen_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        fullscreen_cb.toggled.connect(lambda v: self._update_config('fullscreen', v))
        video_layout.addWidget(fullscreen_cb)
        
        animations_cb = QCheckBox("Enable Animations")
        animations_cb.setChecked(self.config.get('animations', True))
        animations_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        animations_cb.toggled.connect(lambda v: self._update_config('animations', v))
        video_layout.addWidget(animations_cb)
        
        particles_cb = QCheckBox("Particle Effects")
        particles_cb.setChecked(self.config.get('particles', True))
        particles_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        particles_cb.toggled.connect(lambda v: self._update_config('particles', v))
        video_layout.addWidget(particles_cb)
        
        video_layout.addStretch()
        tabs.addTab(video_tab, "VIDEO")
        
        # Gameplay Tab
        gameplay_tab = QWidget()
        gameplay_layout = QVBoxLayout(gameplay_tab)
        gameplay_layout.setContentsMargins(24, 24, 24, 24)
        gameplay_layout.setSpacing(20)
        
        autosave_cb = QCheckBox("Auto-save")
        autosave_cb.setChecked(self.config.get('autosave', True))
        autosave_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        autosave_cb.toggled.connect(lambda v: self._update_config('autosave', v))
        gameplay_layout.addWidget(autosave_cb)
        
        combat_log_cb = QCheckBox("Detailed Combat Log")
        combat_log_cb.setChecked(self.config.get('detailed_log', True))
        combat_log_cb.setStyleSheet("color: #e0e0f0; font-size: 14px;")
        combat_log_cb.toggled.connect(lambda v: self._update_config('detailed_log', v))
        gameplay_layout.addWidget(combat_log_cb)
        
        gameplay_layout.addStretch()
        tabs.addTab(gameplay_tab, "GAMEPLAY")
        
        # Data Tab
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(24, 24, 24, 24)
        data_layout.setSpacing(20)
        
        reset_btn = QPushButton("RESET ALL SAVE DATA")
        reset_btn.setObjectName("attackButton")
        reset_btn.setMinimumHeight(48)
        reset_btn.setStyleSheet("font-size: 14px; font-weight: 700;")
        reset_btn.clicked.connect(self._confirm_reset)
        data_layout.addWidget(reset_btn)
        
        export_btn = QPushButton("EXPORT SAVE DATA")
        export_btn.setObjectName("healButton")
        export_btn.setMinimumHeight(48)
        export_btn.setStyleSheet("font-size: 14px; font-weight: 700;")
        export_btn.clicked.connect(self._export_save)
        data_layout.addWidget(export_btn)
        
        data_layout.addStretch()
        tabs.addTab(data_tab, "DATA")
        
        layout.addWidget(tabs)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("DONE")
        close_btn.setObjectName("startButton")
        close_btn.setMinimumWidth(160)
        close_btn.clicked.connect(self._on_close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_slider(self, parent_layout, label_text, value):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)
        
        label = QLabel(f"{label_text}: {int(value * 100)}%")
        label.setStyleSheet("color: #e0e0f0; font-size: 14px; font-weight: 600;")
        container_layout.addWidget(label)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(int(value * 100))
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(30, 30, 60, 180);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border: 2px solid #ffffff;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a4fff, stop:1 #a855f7);
                border-radius: 3px;
            }
        """)
        slider.valueChanged.connect(lambda v: label.setText(f"{label_text}: {v}%"))
        container_layout.addWidget(slider)
        
        parent_layout.addWidget(container)
        return slider
    
    def _update_config(self, key, value):
        self.config[key] = value
    
    def _confirm_reset(self):
        reply = QMessageBox.question(
            self, "Confirm Reset",
            "This will permanently delete ALL save data.\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            import shutil
            saves_dir = "saves"
            if os.path.exists(saves_dir):
                shutil.rmtree(saves_dir)
                os.makedirs(saves_dir)
            QMessageBox.information(self, "Done", "All save data has been reset.")
    
    def _export_save(self):
        import json
        from datetime import datetime
        saves_dir = "saves"
        if os.path.exists(saves_dir):
            export_data = {}
            for filename in os.listdir(saves_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(saves_dir, filename), 'r') as f:
                        export_data[filename[:-5]] = json.load(f)
            
            export_path = f"save_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            QMessageBox.information(self, "Exported", f"Save data exported to {export_path}")
        else:
            QMessageBox.warning(self, "Error", "No save data found.")
    
    def _on_close(self):
        self.settings_changed.emit(self.config)
        self.closed.emit()


import os