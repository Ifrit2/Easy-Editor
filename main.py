import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ImageFilter

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = "Modefied/"

    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def show_image(self, path):
        image_label.hide()
        pixmap_image = QPixmap(path)
        w, h = image_label.width(), image_label.height()
        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap_image)
        image_label.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def save_image(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.show_image(image_path)

    def do_rotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(
                workdir, self.save_dir, self.filename
        )
        self.show_image(image_path)
    
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(
                workdir, self.save_dir, self.filename
        )
        self.show_image(image_path)
    
    def do_rotateleft(self):
        self.image = self.image.transpose(Image.ROTATE_180)
        self.save_image()
        image_path = os.path.join(
                workdir, self.save_dir, self.filename
        )
        self.show_image(image_path)

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Пустое окно")
main_win.show()
#1
button_images_pap = QPushButton('Папка')
image_label = QLabel("Картинка")
list_images = QListWidget()
#2
button_images_chb = QPushButton('Ч-Б')
button_images_rotate = QPushButton('Рескость')
button_images_mirrored = QPushButton('Зеркально')
button_images_right = QPushButton('Право')
button_images_left = QPushButton('Лево')
#3


layout_1 = QVBoxLayout()
layout_2 = QHBoxLayout()
layout_3 = QVBoxLayout()
layout_4 = QHBoxLayout()

layout_1.addWidget(button_images_pap)
layout_1.addWidget(list_images)
layout_2.addWidget(button_images_chb)
layout_2.addWidget(button_images_rotate)
layout_2.addWidget(button_images_mirrored)
layout_2.addWidget(button_images_right)
layout_2.addWidget(button_images_left)
layout_3.addWidget(image_label)
layout_3.addLayout(layout_2)
layout_4.addLayout(layout_1)
layout_4.addLayout(layout_3)
main_win.setLayout(layout_4)

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for extension in extensions:                   
            if filename.endswith(extension):
                result.append(filename)
    return result

workdir = " "
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():   
    extensions = ['.jpg', '.png']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_images.clear()
    for filename in filenames:
        list_images.addItem(filename)

def show_chosen_images():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        work_image.load_image(workdir, filename)
        image_path = os.path.join(work_image.dir, work_image.filename)
        work_image.show_image(image_path)


work_image = ImageProcessor()

button_images_pap.clicked.connect(showFilenamesList)
list_images.currentRowChanged.connect(show_chosen_images)
button_images_chb.clicked.connect(work_image.do_bw)
button_images_mirrored.clicked.connect(work_image.do_flip)
button_images_rotate.clicked.connect(work_image.do_sharp)
button_images_right.clicked.connect(work_image.do_rotate)
button_images_left.clicked.connect(work_image.do_rotateleft)

main_win.show()
app.exec_()
