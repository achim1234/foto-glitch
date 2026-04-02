from datetime import datetime
import os
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

    # --- Timestamp in output_path einbauen ---
    directory, filename = os.path.split(output_path)
    name, ext = os.path.splitext(filename)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{name}_{timestamp}{ext}"
    new_output_path = os.path.join(directory, new_filename)

    # Speichern
    img.save(new_output_path)
    print(f"Saved: {new_output_path}")


if __name__ == "__main__":

    #python3 color.py input/6.jpg output/output1.jpg --r 1.3 --g 1.2 --b 0.8 && \
    #python3 color.py input/6.jpg output/output2.jpg --r 0.8 --g 1.5 --b 1.2 && \
    #python3 color.py input/6.jpg output/output3.jpg --r 1.6 --g 0.9 --b 0.7 && \
    #python3 color.py input/6.jpg output/output4.jpg --r 0.7 --g 1.1 --b 1.6 && \
    #python3 color.py input/6.jpg output/output5.jpg --r 1.8 --g 1.0 --b 0.6 && \
    #python3 color.py input/6.jpg output/output6.jpg --r 0.6 --g 1.7 --b 1.1 && \
    #python3 color.py input/6.jpg output/output7.jpg --r 1.4 --g 0.7 --b 1.5 && \
    #python3 color.py input/6.jpg output/output8.jpg --r 0.9 --g 1.8 --b 0.5 && \
    #python3 color.py input/6.jpg output/output9.jpg --r 1.7 --g 0.8 --b 1.2 && \
    #python3 color.py input/6.jpg output/output10.jpg --r 0.5 --g 1.3 --b 1.9 && \
    #python3 color.py input/6.jpg output/output11.jpg --r 1.2 --g 1.6 --b 0.7 && \
    #python3 color.py input/6.jpg output/output12.jpg --r 0.7 --g 0.9 --b 1.8 && \
    #python3 color.py input/6.jpg output/output13.jpg --r 1.9 --g 0.6 --b 1.0 && \
    #python3 color.py input/6.jpg output/output14.jpg --r 0.8 --g 1.4 --b 1.7 && \
    #python3 color.py input/6.jpg output/output15.jpg --r 1.5 --g 0.5 --b 1.4 && \
    #python3 color.py input/6.jpg output/output16.jpg --r 0.6 --g 1.9 --b 0.9 && \
    #python3 color.py input/6.jpg output/output17.jpg --r 1.3 --g 0.8 --b 1.7 && \
    #python3 color.py input/6.jpg output/output18.jpg --r 0.9 --g 1.6 --b 1.3 && \
    #python3 color.py input/6.jpg output/output19.jpg --r 1.8 --g 0.7 --b 0.9 && \
    #python3 color.py input/6.jpg output/output20.jpg --r 0.5 --g 1.2 --b 1.8 && \
    #python3 color.py input/6.jpg output/output21.jpg --r 1.6 --g 1.1 --b 0.5 && \
    #python3 color.py input/6.jpg output/output22.jpg --r 0.7 --g 1.8 --b 1.0 && \
    #python3 color.py input/6.jpg output/output23.jpg --r 1.4 --g 0.6 --b 1.9 && \
    #python3 color.py input/6.jpg output/output24.jpg --r 0.8 --g 1.7 --b 1.4 && \
    #python3 color.py input/6.jpg output/output25.jpg --r 1.9 --g 0.9 --b 0.6 && \
    #python3 color.py input/6.jpg output/output26.jpg --r 0.6 --g 1.5 --b 1.8 && \
    #python3 color.py input/6.jpg output/output27.jpg --r 1.7 --g 0.5 --b 1.3 && \
    #python3 color.py input/6.jpg output/output28.jpg --r 0.9 --g 1.9 --b 0.7 && \
    #python3 color.py input/6.jpg output/output29.jpg --r 1.2 --g 0.7 --b 1.9 && \
    #python3 color.py input/6.jpg output/output30.jpg --r 1.8 --g 1.3 --b 0.5

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
