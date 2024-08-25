import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout,
                             QVBoxLayout)

from PyQt5.QtCore import Qt

from PIL import Image, ImageEnhance, ImageFilter

app = QApplication([])
win = QWidget()
win.resize(700,500)
win.setWindowTitle("Nguyen - Image Editor")
##########################################
btn_folder = QPushButton("Folder")
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_mirror = QPushButton("Mirror")
btn_sharpness = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")
btn_blur = QPushButton("Blur")
##########################################
lb_image = QLabel("Image")
lw_files = QListWidget()
##########################################
layout_h_button = QHBoxLayout()
layout_h_button.addWidget(btn_left)
layout_h_button.addWidget(btn_right)
layout_h_button.addWidget(btn_mirror)
layout_h_button.addWidget(btn_sharpness)
layout_h_button.addWidget(btn_bw)
layout_h_button.addWidget(btn_blur)
###########################################
layout_v_fol_list = QVBoxLayout()
layout_v_fol_list.addWidget(btn_folder)
layout_v_fol_list.addWidget(lw_files)
###########################################
layout_v_img_btn = QVBoxLayout()
layout_v_img_btn.addWidget(lb_image,95)
layout_v_img_btn.addLayout(layout_h_button)
###########################################
layout_main = QHBoxLayout()
layout_main.addLayout(layout_v_fol_list, 20)
layout_main.addLayout(layout_v_img_btn, 80)
###########################################
win.setLayout(layout_main)
win.show()
###########################################
class ImageProcssor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.file_name = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, file_name):
        self.dir = dir
        self.file_name = file_name
        img_path = os.path.join(dir, file_name)
        self.image = Image.open(img_path)
    def showImage(self,path):
        lb_image.hide()
        pixel_image = QPixmap(path)
        w = lb_image.width()
        h = lb_image.height()
        pixel_image = pixel_image.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixel_image)
        lb_image.show()


    def saveImage(self):
        path = os.path.join(work_dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.file_name)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)
    def do_sharpness(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)


    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.file_name)
        self.showImage(image_path)



#####################################################################
def showSelectedImage():
    if lw_files.currentRow() >= 0:
        file_name = lw_files.currentItem().text()
        work_image.loadImage(work_dir, file_name)
        image_path = os.path.join(work_image.dir, work_image.file_name)
        work_image.showImage(image_path)
#######################################################################
def selectedWorkDir():
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()
########################################################################
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
#########################################################################
def showFileNamesList():
    extensions = ['.jpg', '.jpeg' , '.png', '.gif']
    selectedWorkDir()
    files = filter(os.listdir(work_dir), extensions)
    lw_files.clear()
    for file in files:
        lw_files.addItem(file)
##########################################################################
work_dir =''
work_image = ImageProcssor()
lw_files.currentRowChanged.connect(showSelectedImage)
##########################################################################
btn_folder.clicked.connect(showFileNamesList)
btn_bw.clicked.connect(work_image.do_bw)
btn_left.clicked.connect(work_image.do_left)
btn_right.clicked.connect(work_image.do_right)
btn_mirror.clicked.connect(work_image.do_mirror)
btn_sharpness.clicked.connect(work_image.do_sharpness)
btn_blur.clicked.connect(work_image.do_blur)



##########################################################################
app.exec()