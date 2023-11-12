from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sqlite3

from PyQt5.uic import loadUi


class DatabaseViewer(QMainWindow):
    def __init__(self):
        super(DatabaseViewer, self).__init__()
        loadUi('main.ui', self)
        # Инициализация и подключение к базе данных
        self.init_db()

        # Создание виджета таблицы
        self.table_widget = QTableWidget()
        self.populate_table()

        # Размещение виджета таблицы на главном окне
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def init_db(self):
        # Инициализация базы данных SQLite с использованием sqlite3
        self.conn = sqlite3.connect("coffee.sqlite")
        self.cursor = self.conn.cursor()

    def populate_table(self):
        # Выполнение SQL-запроса для выборки данных
        query = "SELECT * FROM coffee"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        # Установка заголовков таблицы
        columns = [desc[0] for desc in self.cursor.description]
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)

        # Заполнение таблицы данными
        self.table_widget.setRowCount(len(data))
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table_widget.setItem(row_num, col_num, item)

    def closeEvent(self, event):
        # Закрытие соединения с базой данных при закрытии приложения
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseViewer()
    window.show()
    sys.exit(app.exec_())
