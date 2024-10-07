import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # 윈도우 설정
        self.setWindowTitle('간단한 PyQt5 GUI 예제')
        self.setGeometry(100, 100, 280, 80)

        # 레이블 및 버튼 생성
        self.label = QLabel('클릭해 보세요!', self)
        self.button = QPushButton('클릭', self)
        self.button.clicked.connect(self.change_text)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)

    def change_text(self):
        self.label.setText('안녕하세요, PyQt5!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec_())