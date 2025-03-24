from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QFont


class RemoteControllerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("remote controller")
        self.setGeometry(100, 100, 1150, 600)
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setFont(QFont("Cascadia Mono", 10))
        self.log_output.setReadOnly(True)
        self.log_output.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
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
