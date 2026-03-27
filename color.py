from PIL import Image, ImageOps
import argparse

def adjust_rgb(input_path, output_path, r=1.0, g=1.0, b=1.0):
    # Bild laden + EXIF Fix
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    # In RGB sicherstellen
    img = img.convert("RGB")

    # Kanäle splitten
    red, green, blue = img.split()

    # Funktion zum Skalieren + Clamping
    def scale(channel, factor):
        return channel.point(lambda i: max(0, min(255, int(i * factor))))

    # Anwenden
    red = scale(red, r)
    green = scale(green, g)
    blue = scale(blue, b)

    # Wieder zusammenfügen
    img = Image.merge("RGB", (red, green, blue))

    # Speichern
    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":

    # python3 rgb.py input.jpg output.jpg --r 1.3 --b 0.8
    # python3 rgb.py input.jpg output.jpg --b 1.4 --r 0.9
    # python3 rgb.py input.jpg output.jpg --g 0.85

    parser = argparse.ArgumentParser(description="Adjust RGB channels")

    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")

    parser.add_argument("--r", type=float, default=1.0, help="Red factor (default: 1.0)")
    parser.add_argument("--g", type=float, default=1.0, help="Green factor (default: 1.0)")
    parser.add_argument("--b", type=float, default=1.0, help="Blue factor (default: 1.0)")

    args = parser.parse_args()

    adjust_rgb(
        args.input,
        args.output,
        r=args.r,
        g=args.g,
        b=args.b
    )
