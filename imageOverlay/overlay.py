# Adam Friesz, Husky Robotics
# Last Updated 1/20/24

# This package includes functions related to creating and displaying text over existing image files
# overlay_text combines the functionality of most of the other functions to make the user experience
# as easy as possible.

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy

RELATIVE_TEXT_SIZE = 0.3 # determines size of text overlay compared to background image range 0.3 - 0.5
WHITE = (255,255,255) 
BLACK = (0,0,0)

# returns a new png image with a transparent background displaying the given text in the size.
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
            
    height = int((numlines + 0.5) * fontsize) # this gives a bit of extra space at the bottom
    img = Image.new('RGBA', (width,height), (255, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", fontsize)
    draw = ImageDraw.Draw(img)
    
    draw.text((0, 0), text, font = font, fill = color) 
    return img

# over image is pasted on top of under image, new composite Image is returned.
# over image must have alpha channel
def overlay_bottom_right(under, over):
    width1, height1 = under.size
    width2, height2 = over.size

    if width2 >= width1 or height2 >= height1:
        raise Exception("Overlay image must be smaller than the background image")

    composite = under
    x = width1 - width2
    y = height1 - height2

    composite.paste(over, (x,y), mask = over)
    return composite

# overlays the given txt on the given image in the bottom right corner
def overlay_text(image, txt):
    width = int(RELATIVE_TEXT_SIZE * image.size[0])
    color = shade(image, (width, int(image.size[1] * 0.33))) # samples bottom half of image 
    over = create_text_image(txt, width, color)
    return overlay_bottom_right(image, over)

# returns the rgb value of either black or white, whichever is LESS prevalent in the dim[0] x dim[1]
# rectangle in the bottom right corner of image
# relatively fast - takes average of 0.155 seconds to execute.
def shade(image, dim):
    whiteCount = 0;
    blackCount = 0;
    
    datas = numpy.asarray(ImageOps.grayscale(image)) # grayscale image value of black is 0, white is 255
    for y in range(len(datas) - dim[1], len(datas)): # only analyze images in bottom right dimension
        for x in range(len(datas[y]) - dim[0], len(datas[y])):
            if datas[y][x] >= 150: #closer to white 
                whiteCount += 1
            else:
                blackCount += 1

    if blackCount > whiteCount:
        return WHITE
    else:
        return BLACK
