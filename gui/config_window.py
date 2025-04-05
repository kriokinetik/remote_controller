import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont

CONFIG_FILE = "config.json"


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration")
        self.setMinimumSize(700, 230)
        self.setMaximumSize(700, 230)
        self.setGeometry(200, 200, 700, 230)

        self.token_input = QLineEdit()
        self.admin_input = QLineEdit()
        self.yandex_token_input = QLineEdit()
        self.yandex_id_input = QLineEdit()
        self.yandex_secret_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("TOKEN:", self.token_input)
        form_layout.addRow("ADMIN (comma-separated):", self.admin_input)
        form_layout.addRow("YANDEX_TOKEN:", self.yandex_token_input)
        form_layout.addRow("YANDEX_ID:", self.yandex_id_input)
        form_layout.addRow("YANDEX_SECRET:", self.yandex_secret_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)

        font = QFont("Segoe UI", 10)

        for widget in [
            self.token_input,
            self.admin_input,
            self.yandex_token_input,
            self.yandex_id_input,
            self.yandex_secret_input,
            self.save_button
        ]:
            widget.setFont(font)

        self.save_button.setFixedHeight(40)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)

                # Получаем данные
                self.token_input.setText(config.get("TOKEN", ""))

                # Получаем список ADMIN, если он есть, и преобразуем в строку через запятую
                self.admin_input.setText(",".join(map(str, config.get("ADMIN", []))))

                # Для Yandex настроек
                yandex_config = config.get("YANDEX", {})
                self.yandex_token_input.setText(yandex_config.get("TOKEN", ""))
                self.yandex_id_input.setText(yandex_config.get("ID", ""))
                self.yandex_secret_input.setText(yandex_config.get("SECRET", ""))

    def save_config(self):
        try:
            config = {
                "TOKEN": self.token_input.text(),
                "ADMIN": [int(a.strip()) for a in self.admin_input.text().split(",") if a.strip()],
                "YANDEX": {
                    "TOKEN": self.yandex_token_input.text(),
                    "ID": self.yandex_id_input.text(),
                    "SECRET": self.yandex_secret_input.text(),
                }
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(self, "Success", "Configuration saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{e}")
