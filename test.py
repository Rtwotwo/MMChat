import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie

class GifViewer(QWidget):
    def __init__(self, gif_path):
        super().__init__()
        self.setWindowTitle("GIF Viewer")
        self.setGeometry(100, 100, 400, 400)

        # 创建一个 QLabel 来显示 GIF
        self.label = QLabel(self)

        # 创建一个 QMovie 对象并加载 GIF 文件
        self.movie = QMovie(gif_path)
        self.label.setMovie(self.movie)

        # 创建一个布局并将 QLabel 添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 启动动画
        self.movie.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gif_path = r"assets\audio_gif\dynamic1.gif"  # 替换为你的GIF文件路径
    viewer = GifViewer(gif_path)
    viewer.show()
    sys.exit(app.exec_())