import random
import numpy as np
import os
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ExifTags


def open_image_fixed(path):
    img = Image.open(path)

    # EXIF Orientation korrigieren
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif is not None:
            ori = exif.get(orientation)
            if ori == 3:
                img = img.rotate(180, expand=True)
            elif ori == 6:
                img = img.rotate(270, expand=True)
            elif ori == 8:
                img = img.rotate(90, expand=True)
    except Exception:
        pass

    return img


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
    
    
    
def pixel_shift_glitch(img, max_shift=20):
    """Verschiebt zufällige horizontale Pixelblöcke"""
    arr = np.array(img)
    h, w, c = arr.shape
    for _ in range(random.randint(3, 10)):
        y = random.randint(0, h-1)
        shift = random.randint(-max_shift, max_shift)
        arr[y] = np.roll(arr[y], shift, axis=0)
    return Image.fromarray(arr)

def color_channel_split(img, intensity=1.0):
    arr = np.array(img)
    h, w, c = arr.shape
    new_arr = np.zeros_like(arr)

    max_shift = int(30 * intensity)

    for i in range(3):
        shift_x = random.randint(-max_shift, max_shift)
        shift_y = random.randint(-max_shift, max_shift)
        new_arr[:,:,i] = np.roll(arr[:,:,i], shift=(shift_y, shift_x), axis=(0,1))

    return Image.fromarray(new_arr)

def scanline_noise(img, intensity=30):
    """Fügt horizontale Scanlines / Noise hinzu"""
    arr = np.array(img)
    h, w, c = arr.shape
    for y in range(0, h, 2):
        arr[y] = np.clip(arr[y] + np.random.randint(-intensity, intensity, (w, c)), 0, 255)
    return Image.fromarray(arr)
    
def pixel_block_glitch(img, intensity=1.0):
    arr = np.array(img)
    h, w, c = arr.shape

    blocks = int(10 * intensity)

    for _ in range(blocks):
        y = random.randint(0, h-20)
        height = random.randint(5, int(40 * intensity))
        shift = random.randint(-int(100 * intensity), int(100 * intensity))

        arr[y:y+height] = np.roll(arr[y:y+height], shift, axis=1)

    return Image.fromarray(arr)

def scanline_glitch(img, intensity=1.0):
    arr = np.array(img)
    h, w, c = arr.shape

    for y in range(0, h, random.randint(1,3)):
        noise = np.random.randint(
            -int(80 * intensity),
            int(80 * intensity),
            (w, c)
        )
        arr[y] = np.clip(arr[y] + noise, 0, 255)

    return Image.fromarray(arr)

def process_image(path):
    os.makedirs("output", exist_ok=True)

    img = open_image_fixed(path).convert("RGB")
    
    glitch_intensity = 4.8  # <- hier kannst du eskalieren 😈

    effects = [
        random_color_shift,
        random_contrast,
        random_brightness,
        random_blur,
        random_noise,
        lambda img: pixel_block_glitch(img, glitch_intensity),
        lambda img: color_channel_split(img, glitch_intensity),
        lambda img: scanline_glitch(img, glitch_intensity)
    ]

    random.shuffle(effects)

    for effect in effects:
        if random.random() > 0.4:
            img = effect(img)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/output_artsy_{timestamp}.jpg"

    img.save(output_path)
    print(f"Gespeichert als {output_path}")


if __name__ == "__main__":
    process_image("input.jpg")

