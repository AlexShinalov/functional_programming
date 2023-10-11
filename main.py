import os
import threading
import cv2
import numpy as np

#резкость
def apply_sharpening_filter(input_path, output_path):
    image = cv2.imread(input_path)
    kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    cv2.imwrite(output_path, sharpened)

#степень
def apply_sepia_filter(input_path, output_path):
    image = cv2.imread(input_path)
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_toned = cv2.transform(image, kernel)
    cv2.imwrite(output_path, sepia_toned)

#уменьшение размера
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

            sharpening_thread = threading.Thread(target=apply_sharpening_filter, args=(input_path, sharpened_output_path))
            sepia_thread = threading.Thread(target=apply_sepia_filter, args=(input_path, sepia_output_path))
            resize_thread = threading.Thread(target=resize_image, args=(input_path, resized_output_path, 800, 600))

            sharpening_thread.start()
            sepia_thread.start()
            resize_thread.start()

            sharpening_thread.join()
            sepia_thread.join()
            resize_thread.join()


input_folder = 'C:/Users/snw12/PycharmProjects/FP-1/foto'
output_folder = ('C:/Users/snw12/PycharmProjects/FP-1/1')
process_images(input_folder, output_folder)
