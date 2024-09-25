# Adam Friesz, Husky Robotics
# Last Updated 2/2/24

# This package includes functions related to creating and displaying text over existing image files
# overlay_text combines the functionality of most of the other functions to make the user experience
# as easy as possible.

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy

RELATIVE_TEXT_SIZE = 0.3 # determines size of text overlay compared to background image range 0.3 - 0.5
WHITE = (255,255,255) 
BLACK = (0,0,0)

# overlays the given txt on the given image with text starting at the given [x,y] coordinates
# and going downwards and to the right.
# in place of the coordinates coords can also be a string with value: tl , tr, bl , or br 
# where tl stands for top left and br stands for bottom right. The scalebar will be 
# overlayed at the given position.
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

# overlays a rectangle the given [x,y] dimensions on the given image at the given [x,y] coordinates.
# in place of the coordinates coords can also be a string with value: tl , tr, bl , or br 
# where tl stands for top left and br stands for bottom right. The scalebar will be 
# overlayed at the given position.
def overlayRectangle(image, dims, coords):
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
    
    color = shade(image, coords)
    rect = create_rectangle(dims, color)

    return overlay(image, rect, coords, False)

# overlays a scalebar on the image at the given [x,y] coordinates. 
# in place of the coordinates coords can also be a string with value: tl , tr, bl , or br 
# where tl stands for top left and br stands for bottom right. The scalebar will be 
# overlayed at the given position.
def overlayScalebar(image, coords):
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
    
    width, height = image.size
    rectdims = [int(width * 0.3), int(height * 0.05)]

    img1 = overlayRectangle(image, rectdims, coords).convert("RGB")
    text = "100 cm" # this will change to str(dims[0] * actualPixelSize(image))
    txtcoords = [int(coords[0] + 0.5 * rectdims[0] - len(text) * 25), 
                    int(coords[1] + 1.25 * rectdims[1])]

    return overlayText(img1, text, txtcoords)

# returns a Image object with a transparent background displaying the given text in the
# size and color. image is in 'RGBa' format. 
def create_text_image(inputtext, width, color):
    fontsize = int(width * 1/10)
    numlines = 1
    if (len(inputtext) * fontsize >= width):
        text = ""
        count = 0
        for word in inputtext.split(): # this iterates through each WORD, recognized by spaces
            count += len(word) + 1
            if (-1 + count * fontsize * 0.5) > width: #subtract one to remove space at end
                text += '\n'
                count = len(word) + 1
                numlines += 1
            text += word + " "   
    else:
        text = inputtext
    height = int((numlines + 0.5) * fontsize) # this gives a bit of extra space at the bottom
    img = Image.new('RGBA', (width,height), (255, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", fontsize)
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), text, font = font, fill = color) 
    return img

# creates a red, green, blue, black, or white Image object of given [x,y] dim
def create_rectangle(dims, color):
    newdims = [dims[1], dims[0]]
    newdims.append(3)
    arr =  color[0] * numpy.ones(newdims, numpy.uint8)
    return Image.fromarray(arr)

# overlays the over Image object over the image Image object. 
# the upper left border of over is overlayed starting at the [x,y] coords
# alpha is a boolean value, should be true if the over image is type 'RGBa'
# otherwise should be false.
def overlay(image, over, coords, alpha):
    width1, height1 = image.size
    width2, height2 = over.size

    if width2 >= width1 or height2 >= height1:
        raise Exception("Overlay image must be smaller than the background image")
    if coords[0] > width1 or coords[1] > height1:
        raise Exception("Coordinates to place image are out of bounds")
    
    composite = image
    if alpha:
        composite.paste(over, coords, mask = over)
    else:
        composite.paste(over, coords)
    return composite

# returns the RGB value of either black or white, whichever is LESS prevalent in image
# 255 is white, 0 is black
def shade (image, coords):
    whiteCount = 0;
    blackCount = 0;
    
    data = numpy.asarray(ImageOps.grayscale(image)) # grayscale image value of black is 0, white is 255
    if coords[0] + 500 > image.size[0] or coords[1] + 500 > image.size[1]:
        largecoords = [image.size[0], image.size[1]]
    else:
        largecoords = [coords[0] + 500, coords[1] + 500]
    average = numpy.sum(data[coords[0]: largecoords[0], coords[1]: largecoords[1]])/data.size
    if average >= 150:
        return BLACK
    else: 
        return WHITE