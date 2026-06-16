import sys

from PySide6.QtWidgets import QApplication

from studio.ui.main_window import MainWindow


def main():
    print("1. Creating QApplication")
    app = QApplication(sys.argv)

    print("2. Creating MainWindow")
    window = MainWindow()

    print("3. Showing window")
    window.show()

    print("4. Entering event loop")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
