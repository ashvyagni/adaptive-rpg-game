DARK_THEME = """
/* ===== MAIN WINDOW ===== */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0d0d1a, stop:0.5 #1a1a3e, stop:1 #0d0d2b);
}

/* ===== SCROLL AREAS ===== */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: rgba(30, 30, 60, 150);
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5a4fff, stop:1 #a855f7);
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c6fff, stop:1 #c084fc);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ===== LABELS ===== */
QLabel {
    color: #e0e0f0;
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
}

QLabel#titleLabel {
    color: #ffffff;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 2px;
}

QLabel#subtitleLabel {
    color: #a855f7;
    font-size: 16px;
    font-weight: 400;
    letter-spacing: 4px;
    text-transform: uppercase;
}

QLabel#sectionTitle {
    color: #c084fc;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 1px;
}

QLabel#statLabel {
    color: #9ca3af;
    font-size: 12px;
    font-weight: 500;
}

QLabel#valueLabel {
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
}

QLabel#enemyNameLabel {
    color: #fca5a5;
    font-size: 24px;
    font-weight: 700;
}

QLabel#playerNameLabel {
    color: #60a5fa;
    font-size: 24px;
    font-weight: 700;
}

QLabel#logLabel {
    color: #d1d5db;
    font-size: 13px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QLabel#damageLabel {
    color: #f87171;
    font-size: 28px;
    font-weight: 800;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QLabel#healLabel {
    color: #4ade80;
    font-size: 28px;
    font-weight: 800;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QLabel#critLabel {
    color: #fbbf24;
    font-size: 32px;
    font-weight: 900;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QLabel#missLabel {
    color: #9ca3af;
    font-size: 24px;
    font-weight: 700;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QLabel#aiMessageLabel {
    color: #fcd34d;
    font-size: 14px;
    font-weight: 600;
    font-style: italic;
    padding: 8px 16px;
    background: rgba(252, 211, 77, 0.1);
    border-radius: 8px;
    border: 1px solid rgba(252, 211, 77, 0.3);
}

/* ===== PANELS / FRAMES ===== */
QFrame#characterPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 26, 62, 220), stop:1 rgba(13, 13, 43, 240));
    border: 1px solid rgba(90, 79, 255, 0.3);
    border-radius: 16px;
    padding: 8px;
}

QFrame#enemyPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(62, 26, 26, 220), stop:1 rgba(43, 13, 13, 240));
    border: 1px solid rgba(248, 113, 113, 0.3);
    border-radius: 16px;
    padding: 8px;
}

QFrame#arenaPanel {
    background: qradialgradient(cx:0.5, cy:0.5, radius:1,
        fx:0.5, fy:0.5, stop:0 rgba(26, 26, 62, 180), stop:1 rgba(13, 13, 43, 240));
    border: 2px solid rgba(90, 79, 255, 0.4);
    border-radius: 20px;
}

QFrame#actionPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 26, 62, 200), stop:1 rgba(13, 13, 43, 220));
    border: 1px solid rgba(90, 79, 255, 0.25);
    border-radius: 16px;
}

QFrame#logPanel {
    background: rgba(13, 13, 43, 200);
    border: 1px solid rgba(90, 79, 255, 0.2);
    border-radius: 12px;
}

QFrame#startPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 26, 62, 240), stop:1 rgba(13, 13, 43, 255));
    border: 2px solid rgba(90, 79, 255, 0.4);
    border-radius: 24px;
    padding: 32px;
}

QFrame#gameOverPanel {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(26, 26, 62, 240), stop:1 rgba(13, 13, 43, 255));
    border: 2px solid rgba(90, 79, 255, 0.4);
    border-radius: 24px;
    padding: 32px;
}

/* ===== BUTTONS ===== */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(90, 79, 255, 0.3), stop:1 rgba(168, 85, 247, 0.2));
    border: 1px solid rgba(90, 79, 255, 0.4);
    border-radius: 10px;
    color: #ffffff;
    font-size: 14px;
    font-weight: 600;
    padding: 12px 24px;
    min-height: 20px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(90, 79, 255, 0.5), stop:1 rgba(168, 85, 247, 0.4));
    border: 1px solid rgba(90, 79, 255, 0.7);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(70, 60, 220, 0.6), stop:1 rgba(140, 70, 220, 0.5));
    border: 1px solid rgba(90, 79, 255, 0.9);
    padding-top: 14px;
    padding-bottom: 10px;
}

QPushButton:disabled {
    background: rgba(30, 30, 60, 150);
    border: 1px solid rgba(90, 79, 255, 0.15);
    color: rgba(156, 163, 175, 0.5);
}

QPushButton#attackButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(248, 113, 113, 0.4), stop:1 rgba(239, 68, 68, 0.3));
    border: 1px solid rgba(248, 113, 113, 0.5);
}

QPushButton#attackButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(248, 113, 113, 0.6), stop:1 rgba(239, 68, 68, 0.5));
    border: 1px solid rgba(248, 113, 113, 0.8);
}

QPushButton#healButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(74, 222, 128, 0.4), stop:1 rgba(34, 197, 94, 0.3));
    border: 1px solid rgba(74, 222, 128, 0.5);
}

QPushButton#healButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(74, 222, 128, 0.6), stop:1 rgba(34, 197, 94, 0.5));
    border: 1px solid rgba(74, 222, 128, 0.8);
}

QPushButton#defendButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(96, 165, 250, 0.4), stop:1 rgba(59, 130, 246, 0.3));
    border: 1px solid rgba(96, 165, 250, 0.5);
}

QPushButton#defendButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(96, 165, 250, 0.6), stop:1 rgba(59, 130, 246, 0.5));
    border: 1px solid rgba(96, 165, 250, 0.8);
}

QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5a4fff, stop:1 #a855f7);
    border: none;
    border-radius: 14px;
    font-size: 20px;
    font-weight: 700;
    padding: 16px 48px;
    color: #ffffff;
    min-width: 200px;
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #7c6fff, stop:1 #c084fc);
}

QPushButton#restartButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5a4fff, stop:1 #a855f7);
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    padding: 14px 40px;
    color: #ffffff;
    min-width: 160px;
}

QPushButton#menuButton {
    background: transparent;
    border: 1px solid rgba(90, 79, 255, 0.4);
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    padding: 14px 40px;
    color: #c084fc;
    min-width: 160px;
}

QPushButton#menuButton:hover {
    background: rgba(90, 79, 255, 0.15);
    border: 1px solid rgba(90, 79, 255, 0.7);
    color: #ffffff;
}

/* ===== LINE EDITS ===== */
QLineEdit {
    background: rgba(13, 13, 43, 200);
    border: 1px solid rgba(90, 79, 255, 0.3);
    border-radius: 10px;
    color: #ffffff;
    font-size: 16px;
    padding: 12px 16px;
    selection-background-color: rgba(90, 79, 255, 0.4);
}

QLineEdit:focus {
    border: 2px solid rgba(90, 79, 255, 0.8);
    background: rgba(20, 20, 55, 220);
}

/* ===== PROGRESS BARS ===== */
QProgressBar {
    border: none;
    border-radius: 8px;
    background: rgba(13, 13, 43, 180);
    text-align: center;
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

QProgressBar::chunk {
    border-radius: 8px;
}

QProgressBar#hpBar {
    background: rgba(43, 13, 13, 180);
}

QProgressBar#hpBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ef4444, stop:0.5 #f87171, stop:1 #ef4444);
}

QProgressBar#manaBar {
    background: rgba(13, 13, 53, 180);
}

QProgressBar#manaBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:0.5 #60a5fa, stop:1 #3b82f6);
}

QProgressBar#xpBar {
    background: rgba(13, 13, 43, 180);
    max-height: 6px;
    border-radius: 3px;
}

QProgressBar#xpBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #fbbf24, stop:1 #f59e0b);
    border-radius: 3px;
}

QProgressBar#enemyHpBar {
    background: rgba(43, 13, 13, 180);
    max-height: 12px;
    border-radius: 6px;
}

QProgressBar#enemyHpBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f87171, stop:0.5 #ef4444, stop:1 #dc2626);
    border-radius: 6px;
}

/* ===== COMBAT LOG ===== */
QTextEdit#combatLog {
    background: transparent;
    border: none;
    color: #d1d5db;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 12px;
    line-height: 1.6;
}

/* ===== TOOLTIPS ===== */
QToolTip {
    background: rgba(13, 13, 43, 240);
    border: 1px solid rgba(90, 79, 255, 0.4);
    border-radius: 8px;
    color: #e0e0f0;
    font-size: 12px;
    padding: 8px 12px;
}

/* ===== GLOW EFFECTS (via QGraphicsDropShadowEffect in code) ===== */
"""

def get_stylesheet():
    return DARK_THEME