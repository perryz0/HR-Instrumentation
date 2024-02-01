# Adam Friesz, Husky Robotics
# Last Updated 1/20/24

# This package includes functions related to creating and displaying text over existing image files
# overlay_text combines the functionality of most of the other functions to make the user experience
# as easy as possible.

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy

class backgroundImage(Image): # use a delegating wrapper instead of trying to make a subclass.
    RELATIVE_TEXT_SIZE = 0.3 # determines size of text overlay compared to background image range 0.3 - 0.5
    WHITE = (255,255,255) 
    BLACK = (0,0,0)

    def __init__(self, file):
        image = Image.open(file)
        size = self.size

    # overlays the given txt on the given image in the starting at the given (x,y) value
    def overlayText(self, txt, coords):
        width = int(self.RELATIVE_TEXT_SIZE * self.size[0])
        color = self.shade(self.image) 

        textimage = self.create_text_image(txt, width, color)
        self.overlay(self.image, textimage, coords, True)

    def overlayRectangle(self, dims, coords):
        color = self.shade(self.image)
        rect = self.create_rectangle(dims, color)

        self.overlay(rect, coords, False)

    def overlayScalebar(self, coords):
        width, height = self.size
        rectdims = [int(width * 0.3), int(height * 0.05)]

        img1 = self.overlay_rectangle(rectdims, coords).convert("RGB")
        text = "100 cm" # this will change to str(dims[0] * actualPixelSize(image))
        txtcoords = [int(coords[0] + 0.5 * rectdims[0] - len(text) * 25), 
                     int(coords[1] + rectdims[1] + 0.5 * rectdims[1])]
        
        self.overlay_text(text, txtcoords)

    # returns a new png image with a transparent background displaying the given text in the size.
    def __create_text_image(self, inputtext, width, color):
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

    # creates a white or black image of given size.
    def create_rectangle(dims, color):
        newdims = [dims[1], dims[0]]
        newdims.append(3)
        arr =  color[0] * numpy.ones(newdims, numpy.uint8)
        return Image.fromarray(arr)

    # coords should be a tuple of form (x,y)
    def overlay(self, over, coords, alpha):
        width1, height1 = self.size
        width2, height2 = over.size

        if width2 >= width1 or height2 >= height1:
            raise Exception("Overlay image must be smaller than the background image")
        if coords[0] > width1 or coords[1] > height1:
            raise Exception("Coordinates to place image are out of bounds")
        
        composite = self.image
        if alpha:
            composite.paste(over, coords, mask = over)
        else:
            composite.paste(over, coords)
        self.image = composite

    # returns the rgb value of either black or white, whichever is LESS prevalent in image
    # 255 is white, 0 is black
    def __shade(self, image):
        whiteCount = 0;
        blackCount = 0;
        
        data = numpy.asarray(ImageOps.grayscale(image)) # grayscale image value of black is 0, white is 255
        average = sum(data[:,:])/data.size
        if average >= 150:
            return self.WHITE
        else: 
            return self.BLACK
