from PIL import Image
from collections import Counter
import sys


def get_dominant_color(image_path):
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
        # resize to speed up
        image = image.resize((50, 50))
        pixels = list(image.getdata())
        counts = Counter(pixels)
        # ignore white and near-white, black and near-black if possible, but let's just get the top 5
        most_common = counts.most_common(5)
        for color, count in most_common:
            hex_color = "#{:02x}{:02x}{:02x}".format(*color)
            print(f"Color: {hex_color}, Count: {count}")
    except Exception as e:
        print(f"Error: {e}")


print("flop logo.jpg:")
get_dominant_color("flop logo.jpg")
print("\nflop.jpeg:")
get_dominant_color("flop.jpeg")
