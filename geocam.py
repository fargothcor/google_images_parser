from PIL import Image
import io
import os
from requests import get
from selenium import webdriver
import json
from yaml import load
from os import mkdir
from pixellib.instance import instance_segmentation
from time import sleep

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


class ImageParser:
    def __init__(self, file):
        f = open(file, 'r', encoding='utf-8')
        self.config = load(f)
        print(self.config)
        DRIVER_PATH = self.config['driver_path']
        self.SCREENS_LIMIT = int(self.config['screens_limit'])
        self.wd = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.SCREENS_PATH = self.config['screens_path']
        self.MODEL_PATH = self.config['model_path']

    def make_screen(self, num, play):
        play[0].screenshot(self.SCREENS_PATH + f'{num}\\{num}_source.jpg')

    def parse(self):
        self.wd.get('https://www.geocam.ru/online/entuziastov/')
        play = self.wd.find_elements_by_css_selector('div#player')
        print(play)
        play[0].click()
        sleep(1)
        segment_image = instance_segmentation()
        segment_image.load_model(self.MODEL_PATH)
        target_class = segment_image.select_target_classes(car=True)
        ppath = self.SCREENS_PATH
        for num in range(self.SCREENS_LIMIT):
            try:
                mkdir(ppath + str(num))
            except FileExistsError:
                pass
            self.make_screen(num, play)
            segment_image.segmentImage(
                image_path=ppath + f"{num}\\{num}_source.jpg",
                show_bboxes=True,
                segment_target_classes=target_class,
                extract_segmented_objects=True,
                save_extracted_objects=True,
                output_image_name=ppath + f"{num}\\{num}_out.jpg",
                path=ppath + str(num) + '\\'
            )


config_file = 'conf.yaml'
process = ImageParser(config_file)
process.parse()
