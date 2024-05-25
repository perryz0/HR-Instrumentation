# Perry Chien, Adam Friesz, Husky Robotics
# Last Updated 2/2/24

# This package includes functions related to creating and displaying text over existing image files
# overlay_text combines the functionality of most of the other functions to make the user experience
# as easy as possible.

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy

RELATIVE_TEXT_SIZE = 0.3  # determines size of text overlay compared to background image range 0.3 - 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# overlays the given txt on the given image at the specified position
def overlayText(image, txt, coords):
    if isinstance(coords, str):
        mode = coords
        if mode == 'tl':
            coords = [75,75]
        elif mode == 'tr':
            coords = [int(0.7 * image.size[0] - 75), 75]
        elif mode == 'bl':
            coords = [75, int(0.9 * image.size[1] - 75)]
        elif mode == 'br':
            coords = [int(0.7 * image.size[0] - 75), int(0.9 * image.size[1] - 75)]
        else:
            raise Exception("Unknown mode param given. Check documentation for valid inputs.")
    
    width = int(RELATIVE_TEXT_SIZE * image.size[0])
    color = shade(image, coords) 

    textimage = create_text_image(txt, width, color)
    return overlay(image, textimage, coords, True)

def overlayRectangle(image, dims, coords):
    if isinstance(coords, str):
        mode = coords
        if mode == 'tl':
            coords = [75, 75]
        elif mode == 'tr':
            coords = [int(0.7 * image.size[0] - 75), 75]
        elif mode == 'bl':
            coords = [75, int(0.9 * image.size[1] - 75)]
        elif mode == 'br':
            coords = [int(0.7 * image.size[0] - 75), int(0.9 * image.size[1] - 75)]
        else:
            raise Exception("Unknown mode param given. Check documentation for valid inputs.")
    
    color = shade(image, coords)
    rect = create_rectangle(dims, color)

    return overlay(image, rect, coords, False)

def overlayScalebar(image, coords):
    if isinstance(coords, str):
        mode = coords
        if mode == 'tl':
            coords = [75, 75]
        elif mode == 'tr':
            coords = [int(0.7 * image.size[0] - 75), 75]
        elif mode == 'bl':
            coords = [75, int(0.9 * image.size[1] - 75)]
        elif mode == 'br':
            coords = [int(0.7 * image.size[0] - 75), int(0.9 * image.size[1] - 75)]
        else:
            raise Exception("Unknown mode param given. Check documentation for valid inputs.")
    
    width, height = image.size
    rectdims = [int(width * 0.3), int(height * 0.05)]

    img1 = overlayRectangle(image, rectdims, coords).convert("RGB")
    text = "100 cm"
    txtcoords = [int(coords[0] + 0.5 * rectdims[0] - len(text) * 25), 
                    int(coords[1] + 1.25 * rectdims[1])]

    return overlayText(img1, text, txtcoords)

def create_text_image(inputtext, width, color):
    fontsize = int(width * 1 / 10)
    numlines = 1
    if len(inputtext) * fontsize >= width:
        text = ""
        count = 0
        for word in inputtext.split():
            count += len(word) + 1
            if -1 + count * fontsize * 0.5 > width:
                text += '\n'
                count = len(word) + 1
                numlines += 1
            text += word + " "
    else:
        text = inputtext
    height = int((numlines + 0.5) * fontsize)
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", fontsize)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), text, font=font, fill=color)
    return img

def create_rectangle(dims, color):
    newdims = [dims[1], dims[0]]
    newdims.append(3)
    arr = color[0] * numpy.ones(newdims, numpy.uint8)
    return Image.fromarray(arr)

def overlay(image, over, coords, alpha):
    width1, height1 = image.size
    width2, height2 = over.size

    if width2 >= width1 or height2 >= height1:
        raise Exception("Overlay image must be smaller than the background image")
    if coords[0] > width1 or coords[1] > height1:
        raise Exception("Coordinates to place image are out of bounds")
    
    composite = image
    if alpha:
        composite.paste(over, coords, mask=over)
    else:
        composite.paste(over, coords)
    return composite

def shade(image, coords):
    whiteCount = 0
    blackCount = 0
    
    data = numpy.asarray(ImageOps.grayscale(image))
    if coords[0] + 500 > image.size[0] or coords[1] + 500 > image.size[1]:
        largecoords = [image.size[0], image.size[1]]
    else:
        largecoords = [coords[0] + 500, coords[1] + 500]
    average = numpy.sum(data[coords[0]: largecoords[0], coords[1]: largecoords[1]]) / data.size
    if average >= 150:
        return BLACK
    else:
        return WHITE