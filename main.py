
import sys
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from mtgsdk import Card

# TODO
# Increase length, fade image into to gray w/ gradient
# Card numbers
# increase Legibility

def main():
    cList = []
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <infile>")
        sys.exit()
    with open(str(sys.argv[1])) as f:
        for line in f:
            try:
                cName = line.rstrip("\r\n")
                cList.append(Card.where(name = cName).all()[-1])
            except:
                print(cName, "not found")
                pass
    imageList = []
    for c in cList:
        imageList.append(procCard(c))
    height = (len(imageList) * 21)
    width = 189
    outlist = Image.new("RGBA", (width, height), (26,26,26, 255))
    for i, item in enumerate(imageList):
        outlist.paste(item, (0, 21 * i))
    outlist.save("outlist.png")


def procCard(c):
    # Get image from url
    response = requests.get(c.image_url)
    image = Image.open(BytesIO(response.content))
    # Crop
    width, height = image.size
    # Original card size 223x310, lr border: 17px, nameslate: 80px
    left = 17
    right = 223 - 17
    top = 80
    bottom = 100
    cropped = image.crop((left, top, right, bottom))
    # Draw text
    fontsize = 16
    draw = ImageDraw.Draw(cropped)
    font = ImageFont.truetype("ssp.ttf", fontsize)
    x = 1
    y = 1
    #Background text
    draw.text((x - 1, y - 1), c.name,(0,0,0,255), font = font)
    draw.text((x + 1, y - 1), c.name,(0,0,0,255), font = font)
    draw.text((x - 1, y + 1), c.name,(0,0,0,255), font = font)
    draw.text((x + 1, y + 1), c.name,(0,0,0,255), font = font)
    # Actual text
    draw.text((x, y), c.name,(255,255,255,255), font = font)
    # Output
    print(c.name, ":", cropped.format, cropped.size, cropped.mode)
    #outname = c.name + ".png"
    #cropped.save(outname)
    return cropped



if __name__ == "__main__":
    main()

