# mtgimg.py
# Copyright(C) 2017 Matt Grant(teamuba@gmail.com)
# Full copyright notice available in LICENSE.txt

import sys
import requests
import re
import getopt
from os import linesep
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from mtgsdk import Card

# TODO
# Mana Cost

def main():
    # Variable default values
    outname = "exampledraft.png"
    fontName = "ssp.ttf"
    fontSize = 20
    verbose = False
    # check args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:f:s:v")
    except getopt.GetoptError as err:
        print(err)
        print("Usage: python3 mtgimg.py [-o outfile] [-f fontfile] [-s fontsize] [-v] infile")
        sys.exit(2)
    if(len(args) != 1):
        print("Usage: python3 mtgimg.py [-o outfile] [-f fontfile] [-s fontsize] [-v] infile")
        sys.exit(3)
    for o,a in opts:
        if o == '-o':
            outname = a
        elif o == '-f':
            fontName = a
        elif o == '-s':
            fontSize = int(a)
        elif o == '-v':
            verbose = True
        else:
            print(o)
            print("Usage: python3 mtgimg.py [-o outfile] [-f fontfile] [-s fontsize] [-v] infile")
            sys.exit(4)
    # Compile regex object
    regObj = re.compile("([0-9]+) (.+)")
    # get cardnames from file and search for card objects from mtgsdk
    cList = []
    print("Downloading card information...")
    with open(args[0]) as f:
        for line in f:
            if(line != linesep):
                num, cName = parseLine(line, regObj)
                cList.append((num, Card.where(name = cName).all()[-1]))
    # get card images and send to procCard
    imageList = []
    sliceHeight = 25
    frameWidth = 300
    alpha = alphaGrad(185, sliceHeight, mag = .95)
    # Prepare font
    font = ImageFont.truetype(fontName, fontSize)
    # Get uniform placement per font
    w, maxHeight = font.getsize("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # User message
    print("Processing cards...")
    end = len(cList)
    for x, (n, c) in enumerate(cList):
        print(x + 1, "/",end, ":", c.name)
        imageList.append(procCard(n, c, frameWidth, sliceHeight, alpha, font, maxHeight, verbose))
    # create final list
    outheight = (len(imageList) * sliceHeight)
    output(imageList, frameWidth, outheight, outname, verbose)


# Takes a card, height and width of frame and produces an image slice
def procCard(n, c, frameWidth, sliceHeight, alphaGradient, font, maxHeight, verbose):
    # Get image from url
    response = requests.get(c.image_url)
    image = Image.open(BytesIO(response.content))
    # Crop
    # Original card size 223x310, lr border: 19px, nameslate ends: 80px
    left = 19
    right = 223 - 19
    top = 80
    bottom = top + sliceHeight
    cropped = image.crop((left, top, right, bottom))
    # Convert to RGBA
    if(cropped.mode != "RGBA"): cropped = cropped.convert("RGBA")
    # apply gradient
    grayimage = Image.new("RGBA", cropped.size, color = (26, 26, 26, 255))
    grayimage.putalpha(alphaGradient)
    cropped = Image.alpha_composite(cropped, grayimage)
    # Create frame for final list
    frame = Image.new("RGBA", (frameWidth, sliceHeight),
            color = (26,26,26, 255))
    # Place Image in frame
    xPos = frameWidth - cropped.size[0]
    frame.paste(cropped,(xPos, 0))
    # Draw text
    imageText = n + " " + c.name
    draw = ImageDraw.Draw(frame)
    # Warning for string too long
    w, h = font.getsize(c.name)
    if(w > frameWidth or h > sliceHeight):
        print("Warning:", c.name, "too large for frame with given font and size")
    # print(c.name, " ", w, " ", h)
    x = 5
    y = int((sliceHeight - maxHeight) / 2)
    # 1px black  border
    draw.text((x - 1, y - 1), imageText,(0,0,0,255), font = font)
    draw.text((x + 1, y - 1), imageText,(0,0,0,255), font = font)
    draw.text((x - 1, y + 1), imageText,(0,0,0,255), font = font)
    draw.text((x + 1, y + 1), imageText,(0,0,0,255), font = font)
    # White text
    draw.text((x, y), imageText,(255,255,255,255), font = font)
    # Verbose output
    if verbose:
        print(image.format, image.size, image.mode)
        print()
    
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
def output(imageList, width, height, outname, verbose):
    # Build image
    imageHeight = imageList[0].size[1]
    outlist = Image.new("RGBA", (width, height), color = (26, 26, 26, 255))
    for i, item in enumerate(imageList):
        outlist.paste(item, (0, imageHeight * i))
    # Verbose output
    if verbose:
        print(outname, ": ", outlist.format, outlist.size, outlist.mode)
    # Save file
    outlist.save(outname)

# Takes an image width, height and returns a gradient that can be applied 
# to an image's alpha with imageobj.putalpha(alphaGradient)
def alphaGrad(width, height, mag = 1):
    grad = Image.new("L", (width, 1), color=0x00)
    for x in range(width):
        if x < 145:
            grad.putpixel((x,0), max(0, 255 - 8 * x))
        else:
            grad.putpixel((x,0), 0)
    alpha = grad.resize((width, height))
    return alpha

if __name__ == "__main__":
    main()

