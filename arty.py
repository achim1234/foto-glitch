import random
import numpy as np
import os
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def random_color_shift(img):
    r, g, b = img.split()

    r_factor = random.uniform(0.8, 1.2)
    g_factor = random.uniform(0.8, 1.2)
    b_factor = random.uniform(0.8, 1.2)

    r = r.point(lambda i: int(min(255, i * r_factor)))
    g = g.point(lambda i: int(min(255, i * g_factor)))
    b = b.point(lambda i: int(min(255, i * b_factor)))

    return Image.merge("RGB", (r, g, b))


def random_contrast(img):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(random.uniform(0.7, 1.5))


def random_brightness(img):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(random.uniform(0.8, 1.3))


def random_blur(img):
    if random.random() > 0.5:
        return img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 2)))
    return img


def random_noise(img):
    arr = np.array(img)
    noise = np.random.randint(0, 50, arr.shape, dtype='uint8')
    arr = np.clip(arr + noise, 0, 255)
    return Image.fromarray(arr)




def process_image(path):
    img = Image.open(path).convert("RGB")

    # Zufällige Effekt-Reihenfolge
    effects = [
        random_color_shift,
        random_contrast,
        random_brightness,
        random_blur,
        random_noise
    ]

    random.shuffle(effects)

    for effect in effects:
        if random.random() > 0.4:  # Nicht jeder Effekt immer
            img = effect(img)

    #output_path = "output/output_artsy.jpg"
    
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/output_artsy_{timestamp}.jpg"
    
    
    img.save(output_path)
    print(f"Gespeichert als {output_path}")


if __name__ == "__main__":
    process_image("input/input.jpg")

