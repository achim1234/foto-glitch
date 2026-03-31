from PIL import Image, ImageOps, ImageEnhance
import random
import argparse
import os
from datetime import datetime

def generate_output_path(input_path, output_path=None):
    if output_path:
        return output_path

    # output-Ordner sicherstellen
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Dateiname extrahieren
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return os.path.join(output_dir, f"{name}_glitch_{timestamp}{ext}")


def color_glitch(input_path, output_path=None, strength=0.7):
    output_path = generate_output_path(input_path, output_path)

    # Bild laden + EXIF fix
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r_orig, g_orig, b_orig = pixels[x, y]

            # Zufällig dominanter Kanal
            dominant = random.choice(['r','g','b'])

            if dominant == 'r':
                r_rand = random.randint(150, 255)
                g_rand = random.randint(0, 100)
                b_rand = random.randint(0, 100)
            elif dominant == 'g':
                r_rand = random.randint(0, 100)
                g_rand = random.randint(150, 255)
                b_rand = random.randint(0, 100)
            else:  # blue dominant
                r_rand = random.randint(0, 100)
                g_rand = random.randint(0, 100)
                b_rand = random.randint(150, 255)

            # Mix Original + Random
            new_r = int(r_orig * (1 - strength) + r_rand * strength)
            new_g = int(g_orig * (1 - strength) + g_rand * strength)
            new_b = int(b_orig * (1 - strength) + b_rand * strength)

            pixels[x, y] = (new_r, new_g, new_b)

    # Extra Punch
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Color(img).enhance(1.8)

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extreme color glitch (RGB dominant)")

    parser.add_argument("input", help="Input image")
    parser.add_argument("--output", help="Optional output path")
    parser.add_argument("--strength", type=float, default=0.7,
                        help="Effect strength (0.0 - 1.0)")

    args = parser.parse_args()

    color_glitch(
        args.input,
        output_path=args.output,
        strength=args.strength
    )
