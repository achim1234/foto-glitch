import random
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def neon_gradient_overlay(img, intensity=1.0):
    arr = np.asarray(img).copy()
    h, w, c = arr.shape

    gradient = np.zeros_like(arr)

    color1 = np.array([255, 0, 255])  # pink
    color2 = np.array([0, 255, 255])  # cyan

    for y in range(h):
        blend = y / h
        gradient[y, :] = (1 - blend) * color1 + blend * color2

    alpha = 0.2 * intensity
    arr = np.clip(arr * (1 - alpha) + gradient * alpha, 0, 255)

    return Image.fromarray(arr.astype(np.uint8))


def jpeg_crush(img, quality=20):
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer)


def starburst_flare(img, intensity=1.0):
    arr = np.asarray(img).copy()
    h, w, c = arr.shape

    center_x = random.randint(0, w)
    center_y = random.randint(0, h)

    for i in range(20):
        angle = random.uniform(0, np.pi * 2)
        length = int(min(h, w) * 0.5)
        for r in range(length):
            x = int(center_x + r * np.cos(angle))
            y = int(center_y + r * np.sin(angle))
            if 0 <= x < w and 0 <= y < h:
                arr[y, x] = np.clip(arr[y, x] + 200 * intensity, 0, 255)

    return Image.fromarray(arr.astype(np.uint8))


def glossy_bloom(img, intensity=1.0):
    blurred = img.filter(ImageFilter.GaussianBlur(radius=8 * intensity))
    enhancer = ImageEnhance.Brightness(blurred)
    blurred = enhancer.enhance(1.5 * intensity)
    return Image.blend(img, blurred, 0.4)


def apply_2000s_pack(img, intensity=1.0):
    effects = [
        lambda i: neon_gradient_overlay(i, intensity),
        lambda i: glossy_bloom(i, intensity),
        lambda i: starburst_flare(i, intensity),
        lambda i: jpeg_crush(i, quality=random.randint(10, 30))
    ]

    random.shuffle(effects)

    for effect in effects:
        if random.random() > 0.3:
            img = effect(img)

    return img
