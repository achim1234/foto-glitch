from PIL import Image, ImageEnhance, ImageOps
import argparse

def convert_to_black_white(input_path, output_path, contrast=1.2, threshold=None):
    # Bild laden + EXIF Fix
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    # Graustufen
    bw = img.convert("L")

    # Kontrast
    enhancer = ImageEnhance.Contrast(bw)
    bw = enhancer.enhance(contrast)

    # Optional: hartes Schwarz-Weiß
    if threshold is not None:
        bw = bw.point(lambda x: 255 if x > threshold else 0, mode='1')

    # Speichern
    bw.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":

    # python3 bw.py input.jpg output.jpg --contrast 1.5 --threshold 140
    # python3 bw.py input.jpg output.jpg --threshold 130
    # python3 bw.py input.jpg output.jpg --contrast 1.8
    # python3 bw.py input.jpg output.jpg

    parser = argparse.ArgumentParser(description="Convert image to black & white")

    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--contrast", type=float, default=1.2,
                        help="Contrast level (default: 1.2)")
    parser.add_argument("--threshold", type=int,
                        help="Threshold for pure black/white (0-255)")

    args = parser.parse_args()

    convert_to_black_white(
        args.input,
        args.output,
        contrast=args.contrast,
        threshold=args.threshold
    )
