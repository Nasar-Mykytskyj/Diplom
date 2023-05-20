from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os
from tqdm import tqdm

IMAGE_PATH = "101ObjectMore"

def find(label):
    url = f"https://www.google.com/search?q={label}&tbm=isch"
    res = BeautifulSoup(requests.get(url).text, features="html.parser")

    return res

def download(label, amount):
    res = find(label)

    if not os.path.exists(os.path.join(IMAGE_PATH, label)):
        os.makedirs(os.path.join(IMAGE_PATH, label))

    i = 0
    for img in res.find_all("img"):
        if i == amount:
            break
        src = img.get("src")
        ext = "jpg"
        filename = os.path.join(IMAGE_PATH,
                                label,
                                f"{'0' * (2 - len(str(i)))}{str(i)}" + "img_downloaded" + "." + ext)
        try:
            data = urlopen(src).read()
            open(filename, mode='x').close()
            with open(filename, mode='wb') as fl:
                fl.write(data)
        except Exception as e:
            i -= 1
        i += 1

def findMoreImages(amount):
    for root, dirs, files in os.walk(IMAGE_PATH, topdown=False):
        for name in tqdm(dirs):
            images = next(os.walk(os.path.join(root, name)), (None, None, []))[2]
            if len(images) < 200:
                download(name, amount)


findMoreImages(100)