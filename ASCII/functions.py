from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os


def convert(img: Image, reduce: float) -> str:
    shades = " .:-=+*#%@"
    img = img.convert("L")
    asciiImage = []
    img = img.resize((img.size[0] // reduce, img.size[1] // reduce))
    img_width, img_height = img.size
    for y in range(img_height):
        for x in range(img_width):
            pix = img.getpixel((x, y))
            asciiImage.append(shades[round((pix / 255) * (len(shades) - 1))] + " ")
        asciiImage.append("\n")
    return "".join(asciiImage)


def toImage(asciiImage: str, name=None) -> None:
    img = Image.new(
        "RGB",
        (len(asciiImage.split("\n")[0] * 6), len(asciiImage.split("\n")) * 12),
        "black",
    )
    folderPath = os.path.join(os.path.dirname(__file__), "output")
    d1 = ImageDraw.Draw(img)
    font = ImageFont.truetype("Consolas.ttf", 10)
    d1.text((0, 0), asciiImage, font=font, fill=(255, 255, 255))
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = name if name else date
    img.save(folderPath + f"/{name}.png")
    # open(folderPath + f"/ascii ({date}).txt", "w").write(asciiImage)