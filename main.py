import os
import threading
import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog





input_folder = 'C:/Users/snw12/PycharmProjects/FP-1/foto'
output_folder = ('C:/Users/snw12/PycharmProjects/FP-1/1')


class ImageProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Image Processor')

        self.input_label = QLabel(self)
        self.input_label.setText("Выберите папку с изображениями:")
        self.input_label.move(50, 20)

        self.output_label = QLabel(self)
        self.output_label.setText("Выберите папку для сохранения обработанных изображений:")
        self.output_label.move(50, 60)

        self.input_btn = QPushButton('Выбрать', self)
        self.input_btn.move(300, 15)
        self.input_btn.clicked.connect(self.selectInputFolder)

        self.output_btn = QPushButton('Выбрать', self)
        self.output_btn.move(300, 55)
        self.output_btn.clicked.connect(self.selectOutputFolder)

        self.process_btn = QPushButton('Обработать изображения', self)
        self.process_btn.move(125, 120)
        self.process_btn.clicked.connect(self.processImages)

        self.input_folder = None
        self.output_folder = None

    def selectInputFolder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, "Выберите папку с изображениями")
        self.input_label.setText(f"Выбрана папка: {self.input_folder}")

    def selectOutputFolder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения изображений")
        self.output_label.setText(f"Выбрана папка: {self.output_folder}")

    def processImages(self):
        if self.input_folder and self.output_folder:
            process_images(self.input_folder, self.output_folder)
            self.input_label.setText("Выберите папку с изображениями:")
            self.output_label.setText("Выберите папку для сохранения обработанных изображений:")

def process_images(input_folder, output_folder):
    # резкость
    def apply_sharpening_filter(input_path, output_path):
        image = cv2.imread(input_path)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        cv2.imwrite(output_path, sharpened)

    # степень
    def apply_sepia_filter(input_path, output_path):
        image = cv2.imread(input_path)
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia_toned = cv2.transform(image, kernel)
        cv2.imwrite(output_path, sepia_toned)

    # уменьшение размера
    def resize_image(input_path, output_path, width, height):
        image = cv2.imread(input_path)
        resized = cv2.resize(image, (width, height))
        cv2.imwrite(output_path, resized)

    def process_images(input_folder, output_folder):
        for filename in os.listdir(input_folder):
            if filename.endswith('.jpg') or filename.endswith('.JPG'):
                input_path = os.path.join(input_folder, filename)

                sharpened_output_path = os.path.join(output_folder, f'sharpened_{filename}')
                sepia_output_path = os.path.join(output_folder, f'sepia_{filename}')
                resized_output_path = os.path.join(output_folder, f'resized_{filename}')

                sharpening_thread = threading.Thread(target=apply_sharpening_filter,
                                                     args=(input_path, sharpened_output_path))
                sepia_thread = threading.Thread(target=apply_sepia_filter, args=(input_path, sepia_output_path))
                resize_thread = threading.Thread(target=resize_image, args=(input_path, resized_output_path, 800, 600))

                sharpening_thread.start()
                sepia_thread.start()
                resize_thread.start()

                sharpening_thread.join()
                sepia_thread.join()
                resize_thread.join()
    # Ваш код для обработки изображений

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessorApp()
    ex.show()
    sys.exit(app.exec_())

process_images(input_folder, output_folder)
