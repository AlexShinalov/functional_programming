import os
import threading
import cv2
import numpy as np

#резкость
def blure_filter(input_path, output_path):
    image = cv2.imread(input_path)
    blurred = cv2.blur(image, (5, 5))
    cv2.imwrite(output_path, blurred)

#степень
def sepia_filter(input_path, output_path):
    image = cv2.imread(input_path)
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_toned = cv2.transform(image, kernel)
    cv2.imwrite(output_path, sepia_toned)

#уменьшение размера
def bandw_image(input_path, output_path, width, height):
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, gray)


def process_images(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            input_path = os.path.join(input_folder, filename)


            blure_output_path = os.path.join(output_folder, f'sharpened_{filename}')
            sepia_output_path = os.path.join(output_folder, f'sepia_{filename}')
            bandw_output_path = os.path.join(output_folder, f'resized_{filename}')

            blure_thread = threading.Thread(target=blure_filter, args=(input_path, blure_output_path))
            sepia_thread = threading.Thread(target=sepia_filter, args=(input_path, sepia_output_path))
            bandw_thread = threading.Thread(target=bandw_image, args=(input_path, bandw_output_path, 800, 600))

            blure_thread.start()
            sepia_thread.start()
            bandw_thread.start()

            blure_thread.join()
            sepia_thread.join()
            bandw_thread.join()


input_folder = 'C:/Users/snw12/PycharmProjects/FP-1/foto'
output_folder = ('C:/Users/snw12/PycharmProjects/FP-1/1')
process_images(input_folder, output_folder)
