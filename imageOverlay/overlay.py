# Adam Friesz, Husky Robotics
# Last Updated 1/30/24

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
    else:
        text = inputtext
    height = int((numlines + 0.5) * fontsize) # this gives a bit of extra space at the bottom
    img = Image.new('RGBA', (width,height), (255, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", fontsize)
    draw = ImageDraw.Draw(img)
    if (color == 1):
        color = WHITE
    else: 
        color = BLACK
    draw.text((0, 0), text, font = font, fill = color) 
    return img

# color must be either 0 for black or 1 for white
# creates a white or black image of given size.
def create_rectangle(dims, color):
    newdims = [dims[1], dims[0]]
    newdims.append(3)
    arr = 255 * color * numpy.ones(newdims, numpy.uint8)
    return Image.fromarray(arr)
    
# over image is pasted on top of under image in bottom right corner, new composite Image is returned.
# over image must have alpha channel
def overlay_text_bottom_right(under, txt):
    width = int(RELATIVE_TEXT_SIZE * under.size[0])
    area = [under.size[0] - width, int(under.size[1] * 0.66), under.size[0], under.size[1]]
    color = shade(under, area) 
    textimage = create_text_image(txt, width, color)
    coords = [under.size[0] - textimage.size[0], under.size[1] - textimage.size[1]]
    return overlay(under, textimage, coords, True)


def overlay_top_left(under, over, alpha):
    return overlay(under, over, (50,50), alpha)

# coords should be a tuple of form (x,y)
def overlay(under, over, coords, alpha):
    width1, height1 = under.size
    width2, height2 = over.size

    if width2 >= width1 or height2 >= height1:
        raise Exception("Overlay image must be smaller than the background image")
    if coords[0] > width1 or coords[1] > height1:
        raise Exception("Coordinates to place image are out of bounds")
    
    composite = under
    if alpha:
        composite.paste(over, coords, mask = over)
    else:
        composite.paste(over, coords)
    return composite


# overlays the given txt on the given image in the starting at the given (x,y) value
def overlay_text(image, txt, coords):
    width = int(RELATIVE_TEXT_SIZE * image.size[0])
    scancoords = coords[:]
    scancoords.append(coords[0] + width)
    scancoords.append(int(coords[1] + image.size[1] * 0.3))
    color = shade(image, scancoords) 

    textimage = create_text_image(txt, width, color)
    return overlay(image, textimage, coords, True)

# dims = [x,y]
def overlay_rectangle(image, dims):
    coords = [0, 0, dims[0], dims[1]]
    color = shade(image, coords)

    rect = create_rectangle(dims, color)
    return overlay_top_left(image, rect, False)

def overlay_scalebar(image):
    width, height = image.size
    dims = [int(width * 0.3), 100]

    img1 = overlay_rectangle(image, dims)
    img1.convert("RGB")
    text = "100 cm" # this will change to str(dims[0] * actualPixelSize(image))
    return overlay_text(img1, text, [int(50 + 0.5 * dims[0] - len(text) * 25), 50 + dims[1] + 50])

# returns the rgb value of either black or white, whichever is LESS prevalent in the dim[0] x dim[1]
# in the given coordinates.
# coords should be a list with 4 elements formatted x0,y0,x1,y1
# relatively fast - takes average of 0.155 seconds to execute.
def shade(image, coords):
    whiteCount = 0;
    blackCount = 0;
    
    datas = numpy.asarray(ImageOps.grayscale(image)) # grayscale image value of black is 0, white is 255
    if coords[0] > image.size[0] or coords[1] > image.size[1]:
        raise Exception("coordinates are out of bounds for given image")
    for y in range(coords[1], coords[3]): # only analyze images in bottom right dimension
        for x in range(coords[0], coords[2]):
            if datas[y][x] >= 150: #closer to white 
                whiteCount += 1
            else:
                blackCount += 1

    if blackCount > whiteCount:
        return 1
    else:
        return 0
