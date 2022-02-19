# CMPT 120 Yet Another Image Processer
# Starter code for main.py
# Author(s): Jared Tweed
# Date: December 7th, 2020
# Description: Image Manipulation Interface.



"""
I think in the project description paper there’s a tk dialog option you can copy/paste into your code.
to save and upload the image with file explorer.
CHECK DISCUSION FORUM!
"""



import cmpt120imageProj
import cmpt120imageManip
import tkinter.filedialog
import pygame
pygame.init()

# list of system options
system = [
            "Q: Quit",
            "O: Open Image",
            "S: Save Current Image",
            "R: Reload Origional Image"
         ]

# list of basic operation options
basic = [
          "1: Invert",
          "2: Flip Horizontal",
          "3: Flip Vertical",
          "4: Switch to Intermeidate Functions",
          "5: Switch to Advanced Functions"
         ]

# list of intermediate operation options
intermediate = [
                  "1: Remove Red Channel",
                  "2: Remove Green Channel",
                  "3: Remove Blue Channel",
                  "4: Convert to Greyscale",
                  "5: Apply Sapia Filter",
                  "6: Decrease Brightness",
                  "7: Increase Brightness",
                  "8: Switch to Basic Functions",
                  "9: Switch to Advanced Functions"
                 ]

# list of advanced operation options
advanced = [
                "1: Rotate Left",
                "2: Rotate Right",
                "3: Pixelate",
                "4: Binarize",
                "5: Switch to Basic Functions",
                "6: Switch to Intermediate Functions"
             ]

# a helper function that generates a list of strings to be displayed in the interface
def generateMenu(state):
    """
    Input:  state - a dictionary containing the state values of the application
    Returns: a list of strings, each element represets a line in the interface
    """
    menuString = ["Welcome to CMPT 120 Image Processer!"]
    menuString.append("") # an empty line
    menuString.append("Choose the following options:")
    menuString.append("") # an empty line
    menuString += system
    menuString.append("") # an empty line

    # build the list differently depending on the mode attribute
    if state["mode"] == "basic":
        menuString.append("--Basic Mode--")
        menuString += basic
        menuString.append("")
        menuString.append("***Update this line to show the proper information***")
    elif state["mode"] == "intermediate":
        menuString.append("--Intermediate Mode--")
        menuString += intermediate
        menuString.append("")
        menuString.append("***Update this line to show the proper information***")
    elif state["mode"] == "advanced":
        menuString.append("--Advanced Mode--")
        menuString += advanced
        menuString.append("")
        menuString.append("***Update this line to show the proper information***")
    else:
        menuString.append("Error: Unknown mode!")

    return menuString

# a helper function that returns the result image as a result of the operation chosen by the user
# it also updates the state values when necessary (e.g, the mode attribute if the user switches mode)
def handleUserInput(state, img):
    """
        Input:  state - a dictionary containing the state values of the application
                img - the 2d array of RGB values to be operated on
        Returns: the 2d array of RGB vales of the result image of an operation chosen by the user
    """
    userInput = state["lastUserInput"].upper()
    # handle the system functionalities
    if userInput.isalpha(): # check if the input is an alphabet
        print("Log: Doing system functionalities " + userInput)
        if userInput == "Q": # this case actually won't happen, it's here as an example
            print("Log: Quitting...")
        # ***add the rest to handle other system functionalities***

    # or handle the manipulation functionalities based on which mode the application is in
    elif userInput.isdigit(): # has to be a digit for manipulation options
        print("Log: Doing manipulation functionalities " + userInput)
        # ***add the rest to handle other manipulation functionalities***

    else: # unrecognized user input
            print("Log: Unrecognized user input: " + userInput)

    return img

# use a dictionary to remember several state values of the application
appStateValues = {
                    "mode": "basic",
                    "lastOpenFilename": "",
                    "lastSaveFilename": "",
                    "lastUserInput": ""
                 }

currentImg = cmpt120imageProj.createBlackImage(600, 400) # create a default 600 x 400 black image
cmpt120imageProj.showInterface(currentImg, "No Image", generateMenu(appStateValues)) # note how it is used

# ***this is the event-loop of the application. Keep the remainder of the code unmodified***
NumberOfSaved = 0
keepRunning = True
# a while-loop getting events from pygame
while keepRunning:
    ### use the pygame event handling system ###
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            appStateValues["lastUserInput"] = pygame.key.name(event.key)
            # prepare to quit the loop if user inputs "q" or "Q"
            if appStateValues["lastUserInput"].upper() == "Q":
                keepRunning = False #quits the program.

            if appStateValues["lastUserInput"].upper() == "O":
                ProjectImage = tkinter.filedialog.askopenfilename()
                if ProjectImage not in ["", None]:
                    currentImg = cmpt120imageProj.getImage(ProjectImage) #opens the image selected.
                cmpt120imageProj.showInterface(currentImg, "New Image", generateMenu(appStateValues)) #reloads the UI page.

            if appStateValues["lastUserInput"].upper() == "S":
                saveFilename = tkinter.filedialog.asksaveasfilename()
                if saveFilename not in ["", None]:
                    cmpt120imageProj.saveImage(currentImg, saveFilename + ".jpg") #saves the image if a name is chosen.
##                else: #if no file is chosen, saves the image with a default name.
##                    cmpt120imageProj.saveImage(currentImg, "SavedProjectPhoto" + str(NumberOfSaved) + ".jpg")
##                    NumberOfSaved = NumberOfSaved + 1
                cmpt120imageProj.showInterface(currentImg, "Saved Image", generateMenu(appStateValues)) #reloads the UI page.

            if appStateValues["lastUserInput"].upper() == "R":
                currentImg = cmpt120imageProj.getImage(ProjectImage) #makes the original image the current image.
                cmpt120imageProj.showInterface(currentImg, "Reload Image", generateMenu(appStateValues)) #reloads the UI page.

            if appStateValues["lastUserInput"].upper() == "1": 
                if appStateValues["mode"] == "basic": #for the given mode...
                    currentImg = cmpt120imageManip.invert(currentImg) #applies the invert function.
                    cmpt120imageProj.showInterface(currentImg, "Inverted Image", generateMenu(appStateValues)) #reloads the UI page.
                elif appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.removeRed(currentImg) #applies the remove red function.
                    cmpt120imageProj.showInterface(currentImg, "Remove Red Channel", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    currentImg = cmpt120imageManip.rotateLeft(currentImg) #applies the rotate left function.
                    cmpt120imageProj.showInterface(currentImg, "Rotate Left", generateMenu(appStateValues))

            #When 2 is pressed, the function corrolating to the given mode is applied.
            if appStateValues["lastUserInput"].upper() == "2": 
                if appStateValues["mode"] == "basic":
                    currentImg = cmpt120imageManip.flipHorizontal(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Horizontally Flipped Image", generateMenu(appStateValues))
                elif appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.removeGreen(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Remove Green Channel", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    currentImg = cmpt120imageManip.rotateRight(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Rotate Right", generateMenu(appStateValues))

            #When 3 is pressed, the function corrolating to the given mode is applied.
            if appStateValues["lastUserInput"].upper() == "3":
                if appStateValues["mode"] == "basic":
                    currentImg = cmpt120imageManip.flipVertical(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Vertically Flipped Image", generateMenu(appStateValues))
                elif appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.removeBlue(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Remove Blue Channel", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    currentImg = cmpt120imageManip.pixelate(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Pixelate Image", generateMenu(appStateValues))

            #When 4 is pressed, the function corrolating to the given mode is applied.
            if appStateValues["lastUserInput"].upper() == "4":
                if appStateValues["mode"] == "basic":
                    appStateValues["mode"] = "intermediate" # changes the mode to intermediate instead of applying a function.
                    cmpt120imageProj.showInterface(currentImg, "Intermediate Functions", generateMenu(appStateValues))
                elif appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.greyscale(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Greyscale Image", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    currentImg = cmpt120imageManip.binarize(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Binarize Image", generateMenu(appStateValues))

            #When 5 is pressed, the function corrolating to the given mode is applied.
            if appStateValues["lastUserInput"].upper() == "5":
                if appStateValues["mode"] == "basic":
                    appStateValues["mode"] = "advanced" # changes the mode to advanced instead of applying a function.
                    cmpt120imageProj.showInterface(currentImg, "Advanced Functions", generateMenu(appStateValues))
                elif appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.sapia(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Sapia Image", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    appStateValues["mode"] = "basic" # changes the mode to basic instead of applying a function.
                    cmpt120imageProj.showInterface(currentImg, "Basic Functions", generateMenu(appStateValues))

            if appStateValues["lastUserInput"].upper() == "6":
                if appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.decreaseBrightness(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Darkened Image", generateMenu(appStateValues))
                elif appStateValues["mode"] == "advanced":
                    appStateValues["mode"] = "intermediate"
                    cmpt120imageProj.showInterface(currentImg, "Intermediate Functions", generateMenu(appStateValues))

            if appStateValues["lastUserInput"].upper() == "7":
                if appStateValues["mode"] == "intermediate":
                    currentImg = cmpt120imageManip.increaseBrightness(currentImg)
                    cmpt120imageProj.showInterface(currentImg, "Brightened Image", generateMenu(appStateValues))

            if appStateValues["lastUserInput"].upper() == "8":
                if appStateValues["mode"] == "intermediate":
                    appStateValues["mode"] = "basic"
                    cmpt120imageProj.showInterface(currentImg, "Basic Functions", generateMenu(appStateValues))

            if appStateValues["lastUserInput"].upper() == "9":
                if appStateValues["mode"] == "intermediate":
                    appStateValues["mode"] = "advanced"
                    cmpt120imageProj.showInterface(currentImg, "Advanced Functions", generateMenu(appStateValues))
            
            # otherwise let the helper function handle the input
            else:
                currentImg = handleUserInput(appStateValues, currentImg)
        elif event.type == pygame.QUIT: #another way to quit the program is to click the close botton
            keepRunning = False

# shutdown everything from the pygame package
pygame.quit()

print("Log: Program Quit")
