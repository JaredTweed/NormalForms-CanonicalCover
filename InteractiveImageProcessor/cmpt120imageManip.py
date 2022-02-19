# CMPT 120 Yet Another Image Processer
# Starter code for cmpt120imageManip.py
# Author(s): Jared Tweed
# Date: December 7th, 2020
# Description: Image Manipulation Functions.

import cmpt120imageProj as c

def invert(imgPixels):
    width = len(imgPixels) #this uses the current width and height of the given image
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):             #the for loops goes through every pixel.
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[0] = 255 - pixel[0]
            pixel[1] = 255 - pixel[1]       #these change red, green, and blue to its opposite intensity, thus inverting each pixel.
            pixel[2] = 255 - pixel[2]
    return imgPixels

"""def cover(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):
            if y >= height//2:              #if the pixel is in the lower half of the image...
                pixel = imgPixels[x][y]     #this assigns the colour of the pixel to a variable.
                pixel[0] = 0
                pixel[1] = 0                #this makes the pixel black by dimming each colour.
                pixel[2] = 0
    return imgPixels"""

def flipHorizontal(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    black = c.createBlackImage(width, height) #this creates a black canvas with the same width and height of the original image.
    for x in range(width):
        black[x] = imgPixels[-(x+1)]        #this places the columns of pixels in opposite order onto the black canvas.
    return black

def flipVertical(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    black = c.createBlackImage(width, height) #this creates a black canvas with the same width and height of the original image.
    for x in range(width):
        for y in range(height):
            black[x][y] = imgPixels[x][-(y+1)]    #this places the rows of pixels in opposite order onto the black canvas.
    return black

def removeRed(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):             #the for loops goes through every pixel.
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[0] = 0                    #this removes all red from the pixels.
    return imgPixels

def removeGreen(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):             #the for loops go through every pixel.
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[1] = 0                    #this removes all green from the pixels.
    return imgPixels

def removeBlue(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):             #the for loops go through every pixel.
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[2] = 0                    #this removes all blue from the pixels.
    return imgPixels

def greyscale(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[0] = (pixel[0]+pixel[1]+pixel[2])//3
            pixel[1] = (pixel[0]+pixel[1]+pixel[2])//3      #these change red, green, and blue to be the average of each other.
            pixel[2] = (pixel[0]+pixel[1]+pixel[2])//3      #Because each pixel has equal values, the pixels are grey.
    return imgPixels

#the following adds a colour filter.
def sapia(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height): 
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            pixel[0] = int(((pixel[0]*0.393)+(pixel[1]*0.769)+(pixel[2]*0.189))*(255/273))
            pixel[1] = int(((pixel[0]*0.349)+(pixel[1]*0.686)+(pixel[2]*0.168))*(255/273)) #these change change the colour values to the desired ratio.
            pixel[2] = int(((pixel[0]*0.272)+(pixel[1]*0.534)+(pixel[2]*0.131))*(255/273))
            if pixel[0] > 255: pixel[0] = 255
            if pixel[1] > 255: pixel[1] = 255 # This prevents pixels from becoming exceding maximum brightness.
            if pixel[2] > 255: pixel[2] = 255
    return imgPixels

def decreaseBrightness(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height):
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            if pixel[0] < 10: pixel[0] = 0
            else: pixel[0] = pixel[0] - 10
            if pixel[1] < 10: pixel[1] = 0
            else: pixel[1] = pixel[1] - 10     #these change all colours to a lower intesity without ever surpassing zero.
            if pixel[2] < 10: pixel[2] = 0
            else: pixel[2] = pixel[2] - 10
    return imgPixels

def increaseBrightness(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    for x in range(width):
        for y in range(height): 
            pixel = imgPixels[x][y]         #the colour of the current pixel that the for loop is on is assigned to the 'pixel' variable.
            if pixel[0] > 245: pixel[0] = 255
            else: pixel[0] = pixel[0] + 10
            if pixel[1] > 245: pixel[1] = 255
            else: pixel[1] = pixel[1] + 10     #these change all colours to a higher intesity without ever surpassing 255.
            if pixel[2] > 245: pixel[2] = 255
            else: pixel[2] = pixel[2] + 10
    return imgPixels

def rotateLeft(imgPixels):
    w = len(imgPixels) 
    h = len(imgPixels[0])
    black = c.createBlackImage(h, w) #this creates a black canvas with the same width and height of the original image.
    for x in range(h):
        for y in range(w):
            black[x][y] = imgPixels[-(y+1)][x]  #this switches x and y, negates y, and assigns that to a new black canvas to rotate the image left.
    return black

def rotateRight(imgPixels):
    w = len(imgPixels) 
    h = len(imgPixels[0])
    black = c.createBlackImage(h, w) #this creates a black canvas with the same width and height of the original image.
    for x in range(h):
        for y in range(w):
            black[x][y] = imgPixels[y][-(x+1)]   #this switches x and y, negates x, and assigns that to a new black canvas to rotate the image right.
    return black



def pixelate(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    black = c.createBlackImage(width, height) #this creates a black canvas with the same width and height of the original image.

    for x in range(0, width, 4):
        for y in range(0, height, 4):             #the for loops goes through every large pixel location.

            #collects colour average data.
            totalRed = 0
            totalGreen = 0
            totalBlue = 0
            if x+4 <= width and y+4 <= height: #if the large pixel is 4x4 pixels, ...
                for X in range(4):
                    for Y in range(4):
                        totalRed += imgPixels[x+X][y+Y][0]
                        totalGreen += imgPixels[x+X][y+Y][1] # retreives total amount of colour within big pixel region so that the average can be calculated.
                        totalBlue += imgPixels[x+X][y+Y][2]
                averageRed = totalRed//16
                averageGreen = totalGreen//16 #This assigns every large pixel to have the average amount of...  
                averageBlue = totalBlue//16   # ...the three colours that of the original smaller pixels of that space.
            else:                               #if the large pixel is on the edge of the image and therefore less than 16 pixels, ...
                for X in range(width - x + 1):
                    for Y in range(height - y + 1):
                        totalRed += imgPixels[x+X][y+Y][0]
                        totalGreen += imgPixels[x+X][y+Y][1] # retreives total amount of colour within big pixel region so that the average can be calculated.
                        totalBlue += imgPixels[x+X][y+Y][2]
                averageRed = totalRed//((width - x + 1)*(height - y + 1))
                averageGreen = totalGreen//((width - x + 1)*(height - y + 1)) #This assigns every large pixel to have the average amount of the...  
                averageBlue = totalBlue//((width - x + 1)*(height - y + 1))   # ...three colours that of the original smaller pixels of that space.

            #assigns every pixel within big pixel region to have the average colour of that region.
            for X in range(4):
                for Y in range(4):
                    black[x+X][y+Y][0] = averageRed
                    black[x+X][y+Y][1] = averageGreen 
                    black[x+X][y+Y][2] = averageBlue
                    
    return black #returns pixelated image.



#This converts the image into only purely black or white pixels.
def binarize(imgPixels):
    width = len(imgPixels) 
    height = len(imgPixels[0])
    imgPixels = greyscale(imgPixels) #1 Converts the image into grayscale.
    pixelTotal = 0
    for x in range(width):
        for y in range(height): 
            pixelTotal += imgPixels[x][y][0]  # Collects sum of pixel colour channel to calculate average.       
    threshold = pixelTotal/(width*height) #2 Calculate the initial threshold value as average of one of the pixel colour channel.

    #shell log
    print("\nFirst Threshold: ", threshold)
    print("\n\nFist Loop:")

    while True:
        
        black = c.createBlackImage(width, height) #3a From a black canvas...
                
        for x in range(width):
            for y in range(height):
                if imgPixels[x][y][0] > threshold: #3b ...converts the pixels that are larger than the threshold to white.
                   black[x][y][0] = 255
                   black[x][y][1] = 255 #all black pixels are background. the rest are foreground & white.
                   black[x][y][2] = 255

        #4 Calculates the average of one of the pixel colour channel of the background image, does the same for the foreground image.
        pixelTotalForeground = 0 
        foregroundCount = 0
        pixelTotalBackground = 0
        backgroundCount = 0
        for x in range(width):
            for y in range(height):             #the for loops go through every pixel.
                if black[x][y][0] == 255:
                    pixelTotalForeground += imgPixels[x][y][0] #sum of foregound to help calculate average.
                    foregroundCount += 1
                elif black[x][y][0] == 0:    
                    pixelTotalBackground += imgPixels[x][y][0] #sum of backgound to help calculate average.
                    backgroundCount += 1
                else: print("ERROR")
        thresholdF = pixelTotalForeground/(foregroundCount) #foreground average
        thresholdB = pixelTotalBackground/(backgroundCount) #background average
        newThreshold = (thresholdF + thresholdB)/2 #5 Calculates a new threshold by averaging the two averages in Step 4.

        #shell log for TA grading simplicity and understanding (save them time).
        print("\nTotal F & B Colour:", pixelTotalForeground, pixelTotalBackground)
        print("Total F & B Pixels:", foregroundCount, backgroundCount)
        print("Thesholds Foreground & Background =", str(thresholdF), str(thresholdB))
        print("New Threshold from F & B Average = " + str(newThreshold))
        
        #6 If the difference between threshold used in Step 3 and this new threshold is less than or equal to 10...
        if threshold - newThreshold <= 10 and newThreshold - threshold <= 10: 
            print("\nLastThreshold = ", newThreshold, "\n") #shell log
            black = c.createBlackImage(width, height)
            for x in range(width):
                for y in range(height):
                    if imgPixels[x][y][0] > newThreshold: #7
                       black[x][y][0] = 255 #all black pixels are background. the rest are foreground.
                       black[x][y][1] = 255 #This part could be within the while loop to be more concise, but the the steps...
                       black[x][y][2] = 255 # ...would be out of order and thus more confusing for the TA to read.
            return black #returns the binarized image with the new threshold.
        else:
           threshold = newThreshold
           print("\n\nNext Loop:") #shell log
           continue #This sends python back to Step 3 to use this new threshold to continue.

"""Function Testing""" 
#binarize(c.getImage("project-photo.jpg"))
