import logging
from PyQt6.QtWidgets import QTextEdit


class TextHandler(logging.Handler):
    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum())

    def write(self, text):
        self.widget.append(text.strip())
