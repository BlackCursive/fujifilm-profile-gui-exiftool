'''
GUI to Change the Model Number in the EXIF Data to an X-T4
'''
import os
import subprocess
import sys
import time
import webbrowser

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QPushButton,
    QWidget,
    QListWidget,
    QListWidgetItem,QMessageBox,QSizePolicy
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont
from labels import ImageLabel
from PIL import Image

# Check for which operating system then issue appropriate clear command
def clear_screen():
  if(os.name == 'posix'):
    os.system('clear')
  else:
    os.system('cls')
clear_screen()

# Current directory of where the script resides
home_dir = Path.cwd()

# RAW Files Directory
raf_files = home_dir / 'raf_files'

# String representation of home directory needed for Pandas str replacement - Would not use Path from pathlib
raf_files_str_dir = (f"{home_dir}/raf_files/")

# ExifTool Directory
exiftool = home_dir / "exiftool/exiftool"

# Script will be applied to either all JPG or RAF files
raf = "-ext raf"

#Argument file
args = '-Model'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("background-color: #808A93;")
        self.setWindowTitle("Fujifilm EXIF Model Converter")
        self.setWindowIcon(QIcon("static/img/fuji.png"))
        self.setAcceptDrops(True)

        main_layout = QVBoxLayout(self)

        self.image_label = ImageLabel()
        main_layout.addWidget(self.image_label)

        self.image_list = QListWidget()
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        main_layout.addWidget(self.image_list)

        self.image_list.hide()

        self.total_files_label = QLabel(self)
        self.total_files_label.setStyleSheet("color: white; font-size: 16px;")
        font = QFont("Arial", 16)
        self.total_files_label.setFont(font)
        main_layout.addWidget(
            self.total_files_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.total_files_label.hide()

        self.convert_button = QPushButton()
        self.convert_button.setText("Convert")
        self.convert_button.setStyleSheet(
            "QPushButton { border: 1px; background-color: #CED3D8; width:800px;height:35px;}"
        )
        font = QFont("Arial", 16)
        self.convert_button.setFont(font)
        main_layout.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.convert_action)
        self.convert_button.hide()

        button_layout = QHBoxLayout()

        self.go_back_button = QPushButton()
        self.go_back_button.setText("Go Back")
        font = QFont("Arial", 16)
        self.go_back_button.setFont(font)
        self.go_back_button.setStyleSheet(
            "border: 1px; background-color: #CED3D8; width:600px;height:35px;"
        )
        button_layout.addWidget(
            self.go_back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.go_back_button.clicked.connect(self.go_back_action)
        button_layout.addStretch()
        self.go_back_button.hide()

        self.close_program = QPushButton()
        self.close_program.setText("Quit")
        font = QFont("Arial", 16)
        self.close_program.setFont(font)
        self.close_program.setStyleSheet(
            "border:1px;background-color:#CED3D8;width:200px;height:35px;"
        )
        button_layout.addWidget(self.close_program, alignment=Qt.AlignmentFlag.AlignRight)
        self.close_program.clicked.connect(self.quit_program)
        button_layout.addStretch()
        self.close_program.show()

        main_layout.addLayout(button_layout)

        additional_layout = QHBoxLayout()
        self.additional_label = QLabel("Created By - Black Cursive")
        self.additional_label.setStyleSheet("color: white; font-size: 14px;")
        additional_layout.addWidget(self.additional_label)
        additional_layout.addStretch()
        main_layout.addLayout(additional_layout)

        self.button = QPushButton()
        self.button.setIcon(QIcon("static/img/GithubIcon.png"))
        self.button.setStyleSheet("QPushButton { border: none; padding: 0px; }")
        self.button.clicked.connect(self.open_source_code)
        additional_layout.addStretch()
        additional_layout.addWidget(self.button)

        self.counter = 0
        self.max_files_threshold = 14
        self.scrollbar_added = False

    def quit_program(self):
        self.close()

    def open_source_code(self):
        webbrowser.open("https://github.com/blackcursive")

    def add_scrollbar_to_list(self):
        self.scrollbar_added = True
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def convert_action(self):
        save_directory = raf_files # Change the directory as per your needs
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            file_name = os.path.basename(file_path)

            try:
              # Windows
              if os.name == 'nt':
                arg = ['copy', file_path, save_directory]
              # Unix/Linux or MacOS
              else:
                arg = ['cp', file_path, save_directory]
              # Copy the file
              subprocess.call(arg)

              # Run Subprocess - convert model
              cmd_one = (f"{exiftool} -model=X-T4 {raf} {raf_files}")
              mid_process = subprocess.Popen(cmd_one, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=home_dir)

              # Subprocess PIPE outputs
              stdout_mid_process, stderr_mid_process  = mid_process.communicate()

              # Close standard output
              mid_process.stdout.close()

            except Exception as e:
                # Handle any errors that occur during conversion
                if stderr_mid_process:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Errors!")
                    dlg.setDetailedText(f"{stderr_mid_process}")
                    dlg.exec()

        self.convert_button.hide()
        self.resize(900, 600)
        self.go_back_button.show()
        self.close_program.show()

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Files Converted and Backup Created!")
        dlg.setText(f"{self.image_list.count()} file(s) saved in the raf_files folder and backup file(s) created with the suffix '_original'.")

        def quit(self):
            QApplication.quit()

        dlg.exec()

        self.resize(900, 600)
    def go_back_action(self):
        self.go_back_button.hide()
        self.close_program.show()
        self.convert_button.hide()
        self.image_list.hide()
        self.total_files_label.hide()
        self.image_label.show()
        self.image_label.clear()
        self.image_list.clear()
        self.resize(900, 600)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if (
            event.mimeData().hasUrls()
            and len(event.mimeData().urls()) > 0
            and event.mimeData().urls()[0].isLocalFile()
        ):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if self.go_back_button.isVisible():
            event.ignore()
            return

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith((".RAF", ".raf")):
                self.image_label.set_image(file_path)
                self.image_list.show()

                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.image_list.addItem(item)
                self.image_list.scrollToBottom()
                self.image_list.setGeometry(25, 50, 800, 460)
                self.image_list.setAlternatingRowColors(True)

                # Set stylesheet for each item in the QListWidget
                item_style = "QListWidget::item { padding: 10px; background: #F6F7F8; border: 1px solid #95A1AC; margin: 5px; }"
                self.image_list.setStyleSheet(item_style)

                self.image_label.hide()
                if (
                    not self.scrollbar_added
                    and self.image_list.count() >= self.max_files_threshold
                ):
                    self.add_scrollbar_to_list()

                self.total_files_label.show()
                self.convert_button.show()
                self.total_files_label.setText(
                    f"Total Files: {self.image_list.count()}"
                )
                self.resize(900, 600)
        event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
