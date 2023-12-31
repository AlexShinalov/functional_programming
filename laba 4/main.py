

import os
import cv2
import time
import timeit
import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class ImageAnalysis:
    def __init__(self, image_path: str):
        self.stars_count = 0
        self.planets_count = 0
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.images = [self.image]

        if self.image is None:
            raise ValueError("Failed to upload image!")

        if self.image.shape[0] > 4000 and self.image.shape[1] > 4000:
            self.images = []
            height, width = self.image.shape[0],  self.image.shape[1]

            for i in range(0, height, 4000):
                for j in range(0, width, 4000):
                    if height - i < 4000 or width - j < 4000:
                        continue
                    HEIGHT = i + 4000 if height - i - 4000 >= 4000 else height
                    WIDTH = j + 4000 if width - j - 4000 >= 4000 else width
                    self.images.append(self.image[i:HEIGHT, j:WIDTH])

    def analyze_cropped(self, image_chunk: cv2, number: int) -> None:
        """ Grayscale conversion, binarization, and contour search for a cropped image chunk """
        start_time = timeit.default_timer()
        gray_image = cv2.cvtColor(image_chunk, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 211, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        planets_count, stars_count = 0, 0

        """ Classification objects """
        for _, contour in enumerate(contours):
            if cv2.contourArea(contour) < 1:
                """ Planets are circled in red """
                cv2.drawContours(image_chunk, [contour], -1, (0, 255, 0), 2)
                planets_count += 1
            else:
                """ Stars are circled in green """
                cv2.drawContours(image_chunk, [contour], -1, (0, 0, 255), 2)
                stars_count += 1

        cv2.imwrite(os.path.join("processed_images", os.path.basename(self.image_path.replace(".jpg", f" (out)_{number}.jpg"))), image_chunk)
        self.stars_count += stars_count
        self.planets_count += planets_count
        processing_time = timeit.default_timer() - start_time

        """ output"""
        statistics = (
            f"{self.image_path.replace('.jpg', f' (out)_{number}.jpg')}\n"
            f"Resolution: {image_chunk.shape[1]}x{image_chunk.shape[0]}\n"
            f"Total stars: {stars_count}\n"
            f"Total planets: {planets_count}\n"
            f"Total objects: {stars_count + planets_count}\n"
            f"Processing time: {processing_time:.2f} seconds\n"
        )

        """ Logging statistics """
        log_file_path = self.image_path.replace("images", "logs")[:-4] + f"_{number}.log"
        logger = logging.getLogger(log_file_path)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file_path, mode="w")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug(statistics)

    def analyze_cropped_parallel(self) -> None:
        threads = []

        for i, image_file in enumerate(self.images):
            thread = threading.Thread(target=self.analyze_cropped, args=(image_file, i + 1))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        cv2.destroyAllWindows()

    def analyze(self) -> None:
        """ Grayscale conversion, binarization, and contour search """
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 211, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        """ Classification of objects and allocation """
        for _, contour in enumerate(contours):
            if cv2.contourArea(contour) < 1:
                """ Planets red """
                cv2.drawContours(self.image, [contour], -1, (0, 255, 0), 2)
                self.planets_count += 1
            else:
                """ Stars green """
                cv2.drawContours(self.image, [contour], -1, (0, 0, 255), 2)
                self.stars_count += 1

        cv2.imwrite(os.path.join("processed_images", os.path.basename(self.image_path.replace(".jpg", " (out).jpg"))), self.image)
        cv2.destroyAllWindows()

    def print_statistics(self, processing_time: float) -> None:
        """ Output statistics """
        statistics = (
            f"{self.image_path}\n"
            f"Resolution: {self.image.shape[1]}x{self.image.shape[0]}\n"
            f"Total stars: {self.stars_count}\n"
            f"Total planets: {self.planets_count}\n"
            f"Total objects: {self.stars_count + self.planets_count}\n"
            f"Processing time: {processing_time:.2f} seconds\n"
        )

        """ Logging statistics """
        log_file_path = self.image_path.replace("images", "logs")[:-3] + "log"
        logger = logging.getLogger(log_file_path)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file_path, mode="w")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug(statistics)


class ImageAnalysisApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Image Analysis App")

        self.images_count = 0
        self.input_folder = ""
        self.output_folder = ""
        self.progress_bar = None
        self.analysis_thread = None
        self.process_button = None
        self.output_folder_button = None
        self.output_folder_label = None
        self.input_folder_button = None
        self.input_folder_label = None

        self.create_interface()

    def create_interface(self) -> None:
        self.input_folder_label = tk.Label(self.root, text="Input folder: Not Selected")
        self.input_folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_folder_button = tk.Button(self.root, text="Select", command=self.select_input_folder)
        self.input_folder_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.output_folder_label = tk.Label(self.root, text="Output folder: Not Selected")
        self.output_folder_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.output_folder_button = tk.Button(self.root, text="Select", command=self.select_output_folder)
        self.output_folder_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.process_button = tk.Button(self.root, text="Process Images", command=self.start_threading)
        self.process_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.root, length=300, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_input_folder(self) -> None:
        self.input_folder = filedialog.askdirectory()
        if self.input_folder:
            self.input_folder_label.configure(text=f"Input folder: {self.input_folder}")

    def select_output_folder(self) -> None:
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.output_folder_label.configure(text=f"Output folder: {self.output_folder}")

    def start_threading(self) -> None:
        if self.analysis_thread and self.analysis_thread.is_alive():
            return

        self.analysis_thread = threading.Thread(target=self.process_images)
        self.progress_bar["value"] = 0
        self.analysis_thread.start()

    def process_images(self) -> None:
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders!")
            self.progress_bar["value"] = 0
            return

        image_files = [file for file in os.listdir(self.input_folder)]
        self.images_count = len(image_files)
        threads = []

        for i, image_file in enumerate(image_files):
            thread = threading.Thread(target=self.process_image, args=(image_file,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.progress_bar["value"] = 100

    def process_image(self, file: str) -> None:
        start_time = time.time()
        full_path = os.path.normpath(os.path.join(self.input_folder, file))
        image = ImageAnalysis(full_path)
        if len(image.images) > 1:
            image.analyze_cropped_parallel()
        else:
            image.analyze()
        end_time = time.time()
        image.print_statistics(end_time - start_time)
        self.progress_bar["value"] += 1 / self.images_count * 100
        self.root.update_idletasks()


if __name__ == "__main__":
    window = tk.Tk()
    ImageAnalysisApp(window)
    window.mainloop()