# Pygame image functions for the Yet Another Image Processor project
# Do not modfiy this file

import pygame
import numpy

def getImage(filename):
  """
  Input: filename - string containing image filename to open
  Returns: 2d array of RGB values
  """
  image = pygame.image.load(filename)
  return pygame.surfarray.array3d(image).tolist()

def saveImage(pixels, filename):
  """
  Input:  pixels - 2d array of RGB values
          filename - string containing filename to save image
  Output: Saves a file containing pixels
  """
  nparray = numpy.asarray(pixels)
  surf = pygame.surfarray.make_surface(nparray)
  (width, height, colours) = nparray.shape
  surf = pygame.display.set_mode((width, height))
  pygame.surfarray.blit_array(surf, nparray)
  pygame.image.save(surf, filename)

def showInterface(pixels, title, textList):
    """
    Input:  pixels - 2d array of RGB values
            title - title of the window
            text - list of strings to be displayed at the bottom of the window
    Output: show the image in a window
    """
    nparray = numpy.asarray(pixels)
    surf = pygame.surfarray.make_surface(nparray)
    (width, height, colours) = nparray.shape
    # set up the text to be displayed
    fontObj = pygame.font.Font("freesansbold.ttf", 16)
    textObjs = []
    for line in textList:
        textObjs += [fontObj.render(line, False, (0, 0, 0), (225, 225, 225))]
    # find out the largest width within the lines
    maxLineWidth = textObjs[0].get_width()
    for lo in textObjs:
        if maxLineWidth < lo.get_width():
            maxLineWidth = lo.get_width()
    # find out the width of the screen
    width = max(width, maxLineWidth)
    # set up the display
    pygame.display.set_caption(title + " (" + str(width) + "x" + str(height) + ")")
    screen = pygame.display.set_mode((width, height + textObjs[0].get_height()*len(textObjs)))
    screen.fill((225, 225, 225))
    # add the image to the display
    screen.blit(surf, (0, 0))
    # add the texts to the display
    textHeight = height
    for textObj in textObjs:
        screen.blit(textObj, (0, textHeight))
        textHeight += textObj.get_height()
    # display everything
    pygame.display.update()

def createBlackImage(width, height):
    """
    Input:  width - width of the filled image in pixels
            height - height of the filled image in pixels
    Output: 2d array of RGB values all set to zero
    """
    return numpy.zeros((width, height, 3)).tolist()
