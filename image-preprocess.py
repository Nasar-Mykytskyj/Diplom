import os
import random
import argparse
import cv2
import numpy as np
from tqdm import tqdm
import albumentations as A
from PIL import Image

#ROW_DATA = "101Object"
#PREPROCESD_DATA = "ImageData"
ROW_DATA = "101ObjectMore"
PREPROCESD_DATA = "ImageDataMore"

image_width, image_height = 100, 100

def resizeImages():
    for root, dirs, files in os.walk(ROW_DATA, topdown=False):
        for name in tqdm(dirs):
            images = next(os.walk(os.path.join(root, name)), (None, None, []))[2]

            if not os.path.exists(os.path.join(PREPROCESD_DATA, name)):
                os.makedirs(os.path.join(PREPROCESD_DATA, name))

            for image in tqdm(images):
                img = Image.open(os.path.join(root, name, image))

                resized_image = img.resize((image_width, image_height))

                try:
                    resized_image.save(os.path.join(PREPROCESD_DATA, name, image))
                except Exception as e:
                    print(e)


def augumentImages():
    transform = A.Compose([
        A.RandomCrop(width=image_width, height=image_height),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
    ])

    for root, dirs, files in os.walk(PREPROCESD_DATA, topdown=False):
        for subDir in tqdm(dirs):
            images = next(os.walk(os.path.join(root, subDir)), (None, None, []))[2]

            if len(images) < 200:
                for imageName in tqdm(images):
                    pillow_image = Image.open(os.path.join(root, subDir, imageName))
                    image = np.array(pillow_image)

                    for i in range(0,3):
                        random.seed(42)
                        np.random.seed(42)
                        transformed_image = transform(image=image)["image"]

                        img = Image.fromarray(transformed_image)
                        img.save(os.path.join(root, subDir, format("au-{}-{}.jpg".format(i, imageName))))


def checkAmounts():
    rowAmount = 0
    prepAmount = 0

    for root, dirs, files in os.walk(ROW_DATA, topdown=False):
        for name in tqdm(dirs):
            images = next(os.walk(os.path.join(root, name)), (None, None, []))[2]
            rowAmount += len(images)

    for root, dirs, files in os.walk(PREPROCESD_DATA, topdown=False):
        for name in tqdm(dirs):
            images = next(os.walk(os.path.join(root, name)), (None, None, []))[2]
            prepAmount += len(images)

    print("rowAmount: {}, prepAmount {}".format(rowAmount,prepAmount))

parser = argparse.ArgumentParser()
parser.add_argument("-in", "--input", help="Input Image folder")
parser.add_argument("-out", "--output", help="Output Image folder")

def run():
    args = parser.parse_args()

    if args.input != "":
        ROW_DATA = args.input
    if args.output != "":
        PREPROCESD_DATA = args.output

    resizeImages()
    augumentImages()
    checkAmounts()

run()







