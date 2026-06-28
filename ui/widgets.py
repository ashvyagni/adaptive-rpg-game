from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor


class StartScreen(QFrame):
    start_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("startPanel")
        self.setFixedWidth(500)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("ADAPTIVE RPG")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Turn-Based Battle System")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        desc = QLabel("Enter your name and face adaptive enemies\nthat learn from your fighting style.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #9ca3af; font-size: 14px; line-height: 1.6;")
        layout.addWidget(desc)

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
        self.name_input.returnPressed.connect(self._on_start)
        name_layout.addWidget(self.name_input)

        layout.addLayout(name_layout)

        self.start_btn = QPushButton("BEGIN BATTLE")
        self.start_btn.setObjectName("startButton")
        self.start_btn.clicked.connect(self._on_start)
        layout.addWidget(self.start_btn)

        exit_btn = QPushButton("EXIT")
        exit_btn.setObjectName("menuButton")
        exit_btn.clicked.connect(lambda: QApplication.quit())
        layout.addWidget(exit_btn)

    def _on_start(self):
        name = self.name_input.text().strip() or "Hero"
        self.start_requested.emit(name)


class GameOverScreen(QFrame):
    restart_requested = Signal()
    menu_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("gameOverPanel")
        self.setFixedWidth(500)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.result_title = QLabel()
        self.result_title.setObjectName("titleLabel")
        self.result_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_title)

        self.result_desc = QLabel()
        self.result_desc.setAlignment(Qt.AlignCenter)
        self.result_desc.setWordWrap(True)
        self.result_desc.setStyleSheet("color: #9ca3af; font-size: 14px; line-height: 1.6;")
        layout.addWidget(self.result_desc)

        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet("background: transparent; border: none;")
        stats_layout = QVBoxLayout(self.stats_frame)
        stats_layout.setSpacing(8)

        self.xp_label = QLabel()
        self.xp_label.setAlignment(Qt.AlignCenter)
        self.xp_label.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 600;")
        stats_layout.addWidget(self.xp_label)

        self.gold_label = QLabel()
        self.gold_label.setAlignment(Qt.AlignCenter)
        self.gold_label.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: 600;")
        stats_layout.addWidget(self.gold_label)

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignCenter)
        self.level_label.setStyleSheet("color: #60a5fa; font-size: 14px; font-weight: 600;")
        stats_layout.addWidget(self.level_label)

        layout.addWidget(self.stats_frame)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)

        self.restart_btn = QPushButton("FIGHT AGAIN")
        self.restart_btn.setObjectName("restartButton")
        self.restart_btn.clicked.connect(self.restart_requested.emit)
        btn_layout.addWidget(self.restart_btn)

        self.menu_btn = QPushButton("MAIN MENU")
        self.menu_btn.setObjectName("menuButton")
        self.menu_btn.clicked.connect(self.menu_requested.emit)
        btn_layout.addWidget(self.menu_btn)

        layout.addLayout(btn_layout)

    def show_result(self, won: bool, player_stats: dict, enemy_stats: dict, xp: int, gold: int):
        if won:
            self.result_title.setText("VICTORY!")
            self.result_title.setStyleSheet("color: #4ade80;")
            self.result_desc.setText(f"You defeated the {enemy_stats.get('name', 'enemy')}!")
        else:
            self.result_title.setText("DEFEAT")
            self.result_title.setStyleSheet("color: #f87171;")
            self.result_desc.setText(f"The {enemy_stats.get('name', 'enemy')} was too strong...")

        self.xp_label.setText(f"+{xp} XP" if xp > 0 else "No XP gained")
        self.gold_label.setText(f"+{gold} Gold" if gold > 0 else "No Gold gained")
        
        level = player_stats.get('level', 1)
        self.level_label.setText(f"Level {level}  |  {player_stats.get('xp', 0)}/{player_stats.get('xp_to_next', 100)} XP")


class ActionButton(QPushButton):
    def __init__(self, title: str, subtitle: str, btn_type: str, callback):
        super().__init__()
        self.callback = callback
        self.setObjectName(f"{btn_type}Button")
        self.setMinimumHeight(90)
        self.setMinimumWidth(140)
        self._setup_ui(title, subtitle)
        self.clicked.connect(callback)

    def _setup_ui(self, title: str, subtitle: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        layout.addWidget(title_label)

        sub_label = QLabel(subtitle)
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("font-size: 11px; font-weight: 400; color: #9ca3af;")
        layout.addWidget(sub_label)


class CombatLog(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QLabel("COMBAT LOG")
        header.setObjectName("sectionTitle")
        header.setAlignment(Qt.AlignLeft)
        layout.addWidget(header)

        from PySide6.QtWidgets import QTextEdit, QScrollArea
        self.log_area = QTextEdit()
        self.log_area.setObjectName("combatLog")
        self.log_area.setReadOnly(True)
        self.log_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.log_area)

    def add_message(self, message: str, msg_type: str = "info"):
        color_map = {
            "info": "#d1d5db",
            "attack": "#f87171",
            "enemy_attack": "#fca5a5",
            "heal": "#4ade80",
            "defend": "#60a5fa",
            "crit": "#fbbf24",
            "miss": "#9ca3af",
            "ai": "#fcd34d",
            "status": "#c084fc",
            "levelup": "#fbbf24",
            "victory": "#4ade80",
            "defeat": "#f87171",
            "phase": "#f472b6",
            "battle_start": "#a78bfa",
        }
        color = color_map.get(msg_type, "#d1d5db")
        
        prefix_map = {
            "attack": "⚔ ",
            "enemy_attack": "💀 ",
            "heal": "✚ ",
            "defend": "🛡 ",
            "crit": "✦ ",
            "miss": "~ ",
            "ai": "🤖 ",
            "status": "✧ ",
            "levelup": "⬆ ",
            "victory": "★ ",
            "defeat": "✗ ",
            "phase": "◆ ",
            "battle_start": "⚡ ",
        }
        prefix = prefix_map.get(msg_type, "▸ ")

        html = f'<span style="color: {color};">{prefix}{message}</span><br>'
        self.log_area.insertHtml(html)
        
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class FloatingText(QWidget):
    def __init__(self, text: str, color: str, parent=None, is_crit=False, is_miss=False):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        
        font_size = 32 if is_crit else (24 if is_miss else 28)
        weight = 900 if is_crit else 700
        
        self.label.setStyleSheet(f"""
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: {font_size}px;
            font-weight: {weight};
            color: {color};
        """)
        
        layout.addWidget(self.label)

    def animate(self, start_rect, end_rect):
        self.show()
        self.setGeometry(start_rect)
        
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()
        
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()


class CharacterStatsPanel(QFrame):
    def __init__(self, is_player=True):
        super().__init__()
        self.is_player = is_player
        self.setObjectName("characterPanel" if is_player else "enemyPanel")
        self.setFixedWidth(280)
        self._setup_ui()

    def _setup_ui(self):
        from PySide6.QtWidgets import QProgressBar
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        self.name_label = QLabel()
        self.name_label.setObjectName("playerNameLabel" if self.is_player else "enemyNameLabel")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)

        self.portrait = QLabel()
        self.portrait.setFixedSize(120, 120)
        self.portrait.setAlignment(Qt.AlignCenter)
        self.portrait.setStyleSheet("""
            background: rgba(0, 0, 0, 0.3);
            border-radius: 60px;
            border: 2px solid rgba(90, 79, 255, 0.4);
        """)
        portrait_layout = QHBoxLayout()
        portrait_layout.addStretch()
        portrait_layout.addWidget(self.portrait)
        portrait_layout.addStretch()
        layout.addLayout(portrait_layout)

        hp_layout = QHBoxLayout()
        hp_label = QLabel("HP")
        hp_label.setObjectName("statLabel")
        hp_layout.addWidget(hp_label)
        hp_layout.addStretch()
        self.hp_value = QLabel("100/100")
        self.hp_value.setObjectName("valueLabel")
        hp_layout.addWidget(self.hp_value)
        layout.addLayout(hp_layout)

        self.hp_bar = QProgressBar()
        self.hp_bar.setObjectName("hpBar" if self.is_player else "enemyHpBar")
        self.hp_bar.setTextVisible(self.is_player)
        self.hp_bar.setFormat("%v/%m" if self.is_player else "")
        self.hp_bar.setFixedHeight(18 if self.is_player else 14)
        layout.addWidget(self.hp_bar)

        if self.is_player:
            mana_layout = QHBoxLayout()
            mana_label = QLabel("MANA")
            mana_label.setObjectName("statLabel")
            mana_layout.addWidget(mana_label)
            mana_layout.addStretch()
            self.mana_value = QLabel("50/50")
            self.mana_value.setObjectName("valueLabel")
            mana_layout.addWidget(self.mana_value)
            layout.addLayout(mana_layout)

            self.mana_bar = QProgressBar()
            self.mana_bar.setObjectName("manaBar")
            self.mana_bar.setTextVisible(True)
            self.mana_bar.setFormat("%v/%m")
            self.mana_bar.setFixedHeight(14)
            layout.addWidget(self.mana_bar)

            xp_label = QLabel("XP")
            xp_label.setObjectName("statLabel")
            layout.addWidget(xp_label)
            self.xp_bar = QProgressBar()
            self.xp_bar.setObjectName("xpBar")
            self.xp_bar.setTextVisible(False)
            self.xp_bar.setFixedHeight(6)
            layout.addWidget(self.xp_bar)

    def update_stats(self, stats: dict):
        self.name_label.setText(stats.get("name", "Unknown"))
        
        hp = stats.get("hp", 0)
        max_hp = stats.get("max_hp", 100)
        self.hp_value.setText(f"{hp}/{max_hp}")
        self.hp_bar.setMaximum(max_hp)
        self.hp_bar.setValue(hp)

        if self.is_player:
            mana = stats.get("mana", 0)
            max_mana = stats.get("max_mana", 50)
            self.mana_value.setText(f"{mana}/{max_mana}")
            self.mana_bar.setMaximum(max_mana)
            self.mana_bar.setValue(mana)

            xp = stats.get("xp", 0)
            xp_to_next = stats.get("xp_to_next", 100)
            self.xp_bar.setMaximum(xp_to_next)
            self.xp_bar.setValue(xp)