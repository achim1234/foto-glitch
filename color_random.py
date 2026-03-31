from PIL import Image, ImageOps
import random
import argparse
import os
from datetime import datetime

def generate_output_path(input_path, output_path=None):
    if output_path:
        return output_path

    # Dateiname extrahieren
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Output-Ordner
    os.makedirs("output", exist_ok=True)

    return f"output/{name}_{timestamp}{ext}"


def random_colorize(input_path, output_path=None, intensity=1.0):
    # Output automatisch setzen
    output_path = generate_output_path(input_path, output_path)

    # Bild laden + EXIF Fix
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            rand_r = int(r + random.uniform(-255, 255) * intensity)
            rand_g = int(g + random.uniform(-255, 255) * intensity)
            rand_b = int(b + random.uniform(-255, 255) * intensity)

            rand_r = max(0, min(255, rand_r))
            rand_g = max(0, min(255, rand_g))
            rand_b = max(0, min(255, rand_b))

            pixels[x, y] = (rand_r, rand_g, rand_b)

    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random pixel color glitch")

    parser.add_argument("input", help="Input image")
    parser.add_argument("--output", help="Optional output path")
    parser.add_argument("--intensity", type=float, default=1.0,
                        help="Random intensity (0.0 - 2.0 recommended)")

    args = parser.parse_args()

    random_colorize(
        args.input,
        output_path=args.output,
        intensity=args.intensity
    )
