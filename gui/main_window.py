from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QIcon, QAction, QFont

from gui.config_window import ConfigWindow
from gui.bot_thread import BotThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("remote controller")
        self.setMinimumSize(700, 400)
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Создаем горизонтальный лэйаут для кнопок
        button_layout = QHBoxLayout()

        # Создаем кнопки
        self.start_bot_btn = QPushButton("▶️ Start Bot")
        self.stop_bot_btn = QPushButton("⏹ Stop Bot")
        self.open_config_btn = QPushButton("⚙️ Config")

        self.start_bot_btn.clicked.connect(self.start_bot)
        self.stop_bot_btn.clicked.connect(self.stop_bot)
        self.open_config_btn.clicked.connect(self.open_config_window)

        # Добавляем кнопки в горизонтальный лэйаут
        button_layout.addWidget(self.start_bot_btn)
        button_layout.addWidget(self.stop_bot_btn)
        button_layout.addWidget(self.open_config_btn)

        font = QFont("Segoe UI", 10)  # чуть крупнее стандартного

        for btn in [self.start_bot_btn, self.stop_bot_btn, self.open_config_btn]:
            btn.setFont(font)
            btn.setFixedHeight(40)  # кнопки выше

        # Добавляем горизонтальный лэйаут в основной вертикальный
        layout.addLayout(button_layout)
        self.log_output = QTextEdit()
        self.log_output.setFont(QFont("Cascadia Mono", 9))
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.central_widget.setLayout(layout)

        self.tray_icon = QSystemTrayIcon(QIcon("assets/icon.png"), self)
        self.tray_menu = QMenu(title="remote controller")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.show_window)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)

        self.tray_menu.addAction(open_action)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

        # Окно конфигурации
        self.config_window = ConfigWindow()

        self.bot_thread = None

    def start_bot_thread(self):
        self.bot_thread = BotThread()
        # Подключаем сигналы
        self.bot_thread.log_signal.connect(self.update_log)  # Обновление логов

        self.start_bot()

    def start_bot(self):
        if self.bot_thread.is_bot_running():
            self.bot_thread.stop_bot()
            self.bot_thread.wait()  # Ожидаем завершения потока

        self.bot_thread.start()  # Запускаем поток с ботом

    def stop_bot(self):
        """Асинхронно останавливаем бота."""
        if self.bot_thread.is_bot_running():
            self.bot_thread.stop_bot()  # Завершаем поток бота

    def update_log(self, log):
        self.log_output.append(log)

    def open_config_window(self):
        self.config_window.show()
        self.config_window.raise_()
        self.config_window.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide_to_tray()

    def hide_to_tray(self):
        self.hide()

    def show_window(self):
        self.showNormal()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # ЛКМ по иконке в трее
            self.show_window()

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
