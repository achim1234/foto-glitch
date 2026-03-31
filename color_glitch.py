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
    # Output bestimmen
    output_path = generate_output_path(input_path, output_path)

    # Bild laden + EXIF fix
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            # 🔥 aggressive Farbpalette (rot/gelb/grün)
            rand_r = random.randint(150, 255)
            rand_g = random.randint(120, 255)
            rand_b = random.randint(0, 80)

            # Mix Original + Random
            new_r = int(r * (1 - strength) + rand_r * strength)
            new_g = int(g * (1 - strength) + rand_g * strength)
            new_b = int(b * (1 - strength) + rand_b * strength)

            pixels[x, y] = (new_r, new_g, new_b)

    # 🔥 Extra Punch (sehr wichtig)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Color(img).enhance(1.8)

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extreme color glitch (red/yellow/green focus)")

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
