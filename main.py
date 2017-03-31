
import sys
import requests
import re
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from mtgsdk import Card

# TODO
# Card numbers
# Mana Cost
# remember to change parsing in main
# name outfile
# specify font
# Increase length, fade image into to gray w/ gradient

def main():
    # check args
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <infile>")
        sys.exit()
    # Compile regex object
    regObj = re.compile("([0-9]+) (.+)")
    # get cardnames from file and search for card objects from mtgsdk
    cList = []
    with open(str(sys.argv[1])) as f:
        for line in f:
            num, cName = parseLine(line, regObj)
            cList.append((num, Card.where(name = cName).all()[-1]))
    # get card images and send to procCard
    imageList = []
    sliceHeight = 25
    frameWidth = 300
    alpha = alphaGrad(185, sliceHeight, mag = .95)
    for n, c in cList:
        imageList.append(procCard(n, c, frameWidth, sliceHeight, alpha))
    # create final list
    outheight = (len(imageList) * sliceHeight)
    output(imageList, frameWidth, outheight)


# Takes a card, height and width of frame and produces an image slice
def procCard(n, c, frameWidth, sliceHeight, alphaGradient):
    # Get image from url
    response = requests.get(c.image_url)
    image = Image.open(BytesIO(response.content))
    # Crop
    width, height = image.size
    # Original card size 223x310, lr border: 17px, nameslate: 80px
    left = 19
    right = 223 - 19
    top = 80
    bottom = top + sliceHeight
    cropped = image.crop((left, top, right, bottom))
    # Convert to RGBA
    if(cropped.mode != "RGBA"): cropped = cropped.convert("RGBA")
    # apply gradient
    grayimage = Image.new("RGBA", cropped.size, color = 0x262626)
    grayimage.putalpha(alphaGradient)
    cropped = Image.alpha_composite(cropped, grayimage)
    #cropped.putalpha(alphaGradient)
    # Create frame for final list
    frame = Image.new("RGBA", (frameWidth, sliceHeight),
            color = (26,26,26, 255))

    # Place Image in frame
    xPos = frameWidth - cropped.size[0]
    frame.paste(cropped,(xPos, 0))
    # Draw text
    imageText = n + " " + c.name
    fontsize = 20
    draw = ImageDraw.Draw(frame)
    font = ImageFont.truetype("ssp.ttf", fontsize)
    x = 5
    y = 0
    #1px border
    draw.text((x - 1, y - 1), imageText,(0,0,0,255), font = font)
    draw.text((x + 1, y - 1), imageText,(0,0,0,255), font = font)
    draw.text((x - 1, y + 1), imageText,(0,0,0,255), font = font)
    draw.text((x + 1, y + 1), imageText,(0,0,0,255), font = font)
    # Actual text
    draw.text((x, y), imageText,(255,255,255,255), font = font)
    # Output
    print(c.name, ":", image.format, image.size, image.mode)
    return frame

# Apply regex to raw line to get number and card name, returned as (num,cname)
def parseLine(line, regObj):
    pline = line.rstrip("\r\n")
    matchObj = regObj.match(pline)
    if matchObj:
        return (matchObj.group(1), matchObj.group(2))
    else:
        print("Error parsing", pline)
        sys.exit(1)


# Takes list of imageSlices, puts them together and saves an outfile
def output(imageList, width, height):
    imageHeight = imageList[0].size[1]
    outlist = Image.new("RGBA", (width, height), color = (26,26,26))
    for i, item in enumerate(imageList):
        outlist.paste(item, (0, imageHeight * i))
    outlist.save("exampledraft.png")

# Takes an image width, height and returns a gradient that can be applied 
# to an image's alpha with imageobj.putalpha(alphaGradient)
def alphaGrad(width, height, mag = 1):
    grad = Image.new("L", (width, 1), color=0x00)

    for x in range(width - 10):
        grad.putpixel((x, 0), int(255 * (1 - mag * float(x) / width)))
    for x in range(width - 10, width):
        grad.putpixel((x, 0), 0)
    alpha = grad.resize((width, height))
    return alpha

if __name__ == "__main__":
    main()

